from pydantic import BaseModel


class PredictionRequest(BaseModel):
    runtime_minutes: float
    utilization_percent: float
    health_score: float
    temperature_c: float
    vibration_mm_s: float
    power_consumption_kw: float
    avg_energy_kwh: float
    avg_efficiency: float
    avg_rejects: float
    avg_downtime: float


class PredictionResponse(BaseModel):
    prediction: str
    probability: float