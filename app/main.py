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
    start_time = asyncio.get_event_loop().time()
    print(f"Starting POST request with query: {query.query[:50]}...")
    
    # Create initial record
    create_start = asyncio.get_event_loop().time()
    db_query = await models.ItineraryQuery.create(db, query=query.query)
    create_time = asyncio.get_event_loop().time() - create_start
    print(f"Initial record creation time: {create_time:.2f} seconds")
    
    try:
        # Generate itinerary using Gemini
        gemini_start = asyncio.get_event_loop().time()
        print("Starting Gemini API call...")
        itinerary = await services.generate_itinerary(query.query)
        gemini_time = asyncio.get_event_loop().time() - gemini_start
        print(f"Gemini API call time: {gemini_time:.2f} seconds")
        
        # Update the record with the response
        update_start = asyncio.get_event_loop().time()
        db_query = await db_query.update_response(db, itinerary)
        update_time = asyncio.get_event_loop().time() - update_start
        print(f"Database update time: {update_time:.2f} seconds")
        
        total_time = asyncio.get_event_loop().time() - start_time
        print(f"Total POST request time: {total_time:.2f} seconds")
        return db_query
    except Exception as e:
        print(f"Error in POST request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/itinerary/{query_id}")
async def get_itinerary(
    query_id: str,
    db: AsyncSession = Depends(get_read_db)
):
    start_time = asyncio.get_event_loop().time()
    print(f"Starting GET request for ID: {query_id}")
    
    db_query = await models.ItineraryQuery.get(db, query_id)
    
    query_time = asyncio.get_event_loop().time() - start_time
    print(f"GET query execution time: {query_time:.2f} seconds")
    
    if db_query is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return db_query
