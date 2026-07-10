from fastapi import FastAPI
from sqlalchemy import text

from .database import engine
from .routers import factories ,machines , dashboard,predict 



app = FastAPI(
    title="ForgeIQ API",
    version="1.0.0"
)

app.include_router(
    factories.router
)

app.include_router(
    machines.router
)

app.include_router(
    dashboard.router
)

app.include_router(
    predict.router
)

@app.get("/")
def home():
    return {
        "message": "ForgeIQ API Running"
    }

@app.get("/health")
def health():

    with engine.connect() as connection:

        connection.execute(
            text("SELECT 1")
        )

    return {
        "status": "healthy",
        "database": "connected"
    }