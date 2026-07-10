from fastapi import APIRouter
from sqlalchemy import text

from ..database import engine

router = APIRouter(
    prefix="/machines",
    tags=["Machines"]
)

@router.get("/")
def get_machines():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM machines
                ORDER BY machine_id
            """)
        )

        machines = [
            dict(row._mapping)
            for row in result
        ]

    return machines