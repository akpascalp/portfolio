from fastapi import APIRouter
from app.models.sir_model import sir_step, get_R_value

router = APIRouter()

@router.get("/")
async def step_simulation(S: float, I: float, beta: float, gamma: float, day: int, population: int, R: float | None = None):
    if R is None:
        R = get_R_value(S, I)
    S, I, R = sir_step(S, I, R, beta, gamma)
    day += 1
    S = round(S, 3)
    I = round(I, 3)
    R = round(R, 3)
    S = max(0, min(S, 1))
    I = max(0, min(I, 1))
    R = max(0, min(R, 1))
    return {"S": S, "I": I, "R": R, "beta": beta, "gamma": gamma, "day": day, "population": population}
