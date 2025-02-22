from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, services
from .database import sessionmanager, get_write_db, get_read_db
import asyncio

app = FastAPI(title="Itinerary Planner API")


@app.on_event("startup")
async def startup():
    # Create tables on startup using write connection
    async with sessionmanager.connect(mode="write") as connection:
        await sessionmanager.create_all(connection)


@app.on_event("shutdown")
async def shutdown():
    await sessionmanager.close()


@app.post("/itinerary/", response_model=schemas.ItineraryQueryResponse)
async def create_itinerary(
    query: schemas.ItineraryQueryCreate,
    db: AsyncSession = Depends(get_write_db)
):
    # Create initial record
    create_start = asyncio.get_event_loop().time()
    db_query = await models.ItineraryQuery.create(db, query=query.query)
    create_time = asyncio.get_event_loop().time() - create_start
    print(f"Initial record creation time: {create_time:.2f} seconds")

    try:
        # Generate itinerary using Gemini
        itinerary = await services.generate_itinerary(query.query)
        # Update the record with the response
        db_query = await db_query.update_response(db, itinerary)
        return db_query
    except Exception as e:
        print(f"Error in POST request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/itinerary/{query_id}",
         response_model=schemas.ItineraryQueryResponse)
async def get_itinerary(
    query_id: str,
    db: AsyncSession = Depends(get_read_db)
):
    db_query = await models.ItineraryQuery.get(db, query_id)
    if db_query is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return db_query
