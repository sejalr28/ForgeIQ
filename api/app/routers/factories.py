from fastapi import APIRouter
from sqlalchemy import text

from ..database import engine

router = APIRouter(
    prefix="/factories",
    tags=["Factories"]
)


@router.get("/")
def get_factories():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT * FROM factories")
        )

        factories = [
            dict(row._mapping)
            for row in result
        ]

    return factories