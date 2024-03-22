from fastapi import FastAPI
from .routers import parking
from .database import client

app = FastAPI()

app.include_router(parking.router, prefix="/parking", tags=["parking"])

@app.on_event("startup")
async def startup_event():
    @app.on_event("startup")
    async def startup_db_client():
        try:            
            client.admin.command('ping')
            print("Connected to MongoDB")
        except Exception as e:
            print("Failed to connect to MongoDB", e)
    pass

@app.on_event("shutdown")
async def shutdown_event():
    client.close()
