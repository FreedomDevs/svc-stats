from pydantic import BaseModel, Field


class StatsUpdate(BaseModel):
    time_played: int = Field(ge=0)
    kills: int = Field(ge=0)
    deaths: int = Field(ge=0)
