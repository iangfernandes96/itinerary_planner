from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, services
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Itinerary Planner API")


@app.post("/itinerary/", response_model=schemas.ItineraryQueryResponse)
async def create_itinerary(
    query: schemas.ItineraryQueryCreate,
    db: Session = Depends(get_db)
):
    # Create a new query record
    db_query = models.ItineraryQuery(query=query.query)
    db.add(db_query)
    db.commit()
    db.refresh(db_query)

    try:
        # Generate itinerary using Gemini
        itinerary = await services.generate_itinerary(query.query)
        # Update the record with the response
        db_query.itinerary_response = itinerary
        db.commit()
        db.refresh(db_query)
        return db_query
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/itinerary/{query_id}",
         response_model=schemas.ItineraryQueryResponse)
def get_itinerary(query_id: str, db: Session = Depends(get_db)):
    db_query = db.query(models.ItineraryQuery).filter(
        models.ItineraryQuery.id == query_id
    ).first()
    if db_query is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return db_query
