from sqlalchemy import Column, Integer, BigInteger
from database import Base


class PlayerStats(Base):
    __tablename__ = "player_stats"

    user_id = Column(BigInteger, primary_key=True, index=True)
    time_played = Column(Integer, default=0)
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
