from fastapi import FastAPI
from .routers import parking
from .database import client

app = FastAPI()

app.include_router(parking.router, prefix="/parking", tags=["parking"])

@app.on_event("startup")
async def startup_event():
    # Perform startup tasks, such as verifying database connectivity
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Perform shutdown tasks, such as closing database connections
    client.close()
