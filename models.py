from sqlalchemy import Column, Integer
from database import Base
from sqlalchemy.dialects.postgresql import UUID

class PlayerStats(Base):
    __tablename__ = "player_stats"

    user_id = Column(UUID, primary_key=True, index=True)
    time_played = Column(Integer, default=0)
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
