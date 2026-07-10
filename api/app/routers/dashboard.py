from fastapi import APIRouter
from sqlalchemy import text

from ..database import engine

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/overview")
def dashboard_overview():

    with engine.connect() as conn:

        factories = conn.execute(
            text("SELECT COUNT(*) FROM factories")
        ).scalar()

        employees = conn.execute(
            text("SELECT COUNT(*) FROM employees")
        ).scalar()

        machines = conn.execute(
            text("SELECT COUNT(*) FROM machines")
        ).scalar()

        production_orders = conn.execute(
            text("SELECT COUNT(*) FROM production_orders")
        ).scalar()

        alerts = conn.execute(
            text("SELECT COUNT(*) FROM alerts")
        ).scalar()

        energy = conn.execute(
            text("""
                SELECT ROUND(SUM(energy_consumed_kwh)::numeric, 2)
FROM energy_usage
            """)
        ).scalar()

    return {
        "factories": factories,
        "employees": employees,
        "machines": machines,
        "production_orders": production_orders,
        "alerts": alerts,
        "total_energy_kwh": energy
    }