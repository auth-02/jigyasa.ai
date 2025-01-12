from fastapi import FastAPI
from app.ingestion.ingest import router as ingestion_router

app = FastAPI()

# router for ingestion APIs
app.include_router(ingestion_router, prefix="/api/v1/ingestion", tags=["Ingestion"])

@app.get("/")
def root():
    """
    Root endpoint.
    Returns:
        JSON message.
    """
    return {"message": "Welcome to the Jigyasa.ai!"}

@app.get("/healthcheck")
def health():
    """
    Health check endpoint.
    Returns:
        JSON message indicating health status.
    """
    return {"message": "Ok!"}
