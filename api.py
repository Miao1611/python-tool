from fastapi import FastAPI
from pydantic import BaseModel

from calculator import calculate_statistics


app = FastAPI()


class StatisticsRequest(BaseModel):
    numbers: list[float]


@app.get("/")
def root():
    return {
        "message": "Python Tool API is running"
    }


@app.post("/statistics")
def statistics(request: StatisticsRequest):
    result = calculate_statistics(request.numbers)

    return result