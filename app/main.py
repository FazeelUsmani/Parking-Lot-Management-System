from fastapi import FastAPI
from .routers import parking
from .database import client

app = FastAPI()

app.include_router(parking.router, prefix="/parking", tags=["parking"])

@app.on_event("startup")
async def on_startup():
    try:            
        client.admin.command('ping')
        print("Connected to MongoDB")
    except Exception as e:
        print("Failed to connect to MongoDB", e)

@app.on_event("shutdown")
async def on_shutdown():
    client.close()
