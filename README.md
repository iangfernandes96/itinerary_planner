# Itinerary Planner API

A FastAPI-based backend application that generates travel itineraries using Google's Gemini AI.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Make

## Setup

1. Clone the repository
2. Copy the `.env.example` file to `.env` and fill in your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_key_here
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. Start the PostgreSQL database:
   ```bash
   make up
   ```

2. Run database migrations:
   ```bash
   make migrate-up
   ```

## Available Make Commands

- `make up`: Start the PostgreSQL database
- `make down`: Stop the PostgreSQL database
- `make recreate-db`: Recreate the database from scratch
- `make psql`: Open PostgreSQL shell
- `make migrate-up`: Run database migrations
- `make migrate-down`: Rollback database migrations
- `make run`: Start the FastAPI application

## API Endpoints

### Create Itinerary
```http
POST /itinerary/
```
Request body:
```json
{
    "query": "Plan a 3-day trip to Paris"
}
```

### Get Itinerary
```http
GET /itinerary/{query_id}
```

## Development

The application uses:
- FastAPI for the web framework
- PostgreSQL for the database
- Alembic for database migrations
- Google Gemini AI for itinerary generation
- UUID7 for time-sortable unique identifiers 