"""Main FastAPI application module."""

from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from .database import get_read_db, get_write_db, sessionmanager
from .services import ItineraryService
from .services.itinerary import ItineraryServiceError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle startup and shutdown events."""
    try:
        # Startup: Initialize services
        async with sessionmanager.connect(mode="write") as connection:
            await sessionmanager.create_all(connection)
        await itinerary_service.initialize()
        yield
    finally:
        # Shutdown: Cleanup services
        await sessionmanager.close()


# Initialize services
itinerary_service = ItineraryService()

# Type annotations for dependencies
DBSession = Annotated[AsyncSession, Depends(get_write_db)]
ReadDBSession = Annotated[AsyncSession, Depends(get_read_db)]

# Create router with typed routes
router = APIRouter()


# mypy: disable-error-code="misc"
@router.post(
    "/itinerary/",
    response_model=schemas.ItineraryQueryResponse,
    status_code=201,
    responses={
        500: {"description": "Internal server error"},
    },
)
async def create_itinerary(
    query: schemas.ItineraryQueryCreate, db: DBSession
) -> models.ItineraryQuery:
    """Create a new itinerary."""
    try:
        # Create initial record
        db_query = await models.ItineraryQuery.create(db, query=query.query)

        # Generate itinerary using configured LLM
        itinerary = await itinerary_service.generate_itinerary(query.query)

        # Update the record with the response
        return await db_query.update_response(db, itinerary)
    except ItineraryServiceError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate itinerary: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# mypy: disable-error-code="misc"
@router.get(
    "/itinerary/{query_id}",
    response_model=schemas.ItineraryQueryResponse,
    responses={
        404: {"description": "Itinerary not found"},
    },
)
async def get_itinerary(query_id: str, db: ReadDBSession) -> models.ItineraryQuery:
    """Get an existing itinerary by ID."""
    db_query = await models.ItineraryQuery.get(db, query_id)
    if db_query is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return db_query


# Create FastAPI app with router
app = FastAPI(
    title="Itinerary Planner API",
    lifespan=lifespan,
    openapi_url="/openapi.json",
    docs_url="/docs",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
