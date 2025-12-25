from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import PlayerStats
from schemas import StatsUpdate
from responses import success_response, error_response
from codes import Codes
import math

router = APIRouter(prefix="/stats", tags=["stats"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{user_id}")
def create_stats(user_id: int, db: Session = Depends(get_db)):
    if db.query(PlayerStats).filter_by(user_id=user_id).first():
        return error_response(409, "Статистика уже существует", Codes.STATS_ALREADY_EXISTS)

    stats = PlayerStats(user_id=user_id)
    db.add(stats)
    db.commit()

    return success_response(
        message="Статистика создана",
        code=Codes.STATS_CREATED,
        data={"user_id": user_id}
    )


@router.put("/{user_id}")
def update_stats(user_id: int, payload: StatsUpdate, db: Session = Depends(get_db)):
    stats = db.query(PlayerStats).filter_by(user_id=user_id).first()
    if not stats:
        return error_response(404, "Статистика не найдена", Codes.STATS_NOT_FOUND)

    stats.time_played = payload.time_played
    stats.kills = payload.kills
    stats.deaths = payload.deaths
    db.commit()

    return success_response(
        message="Статистика обновлена",
        code=Codes.STATS_UPDATED
    )


@router.get("/{user_id}")
def get_stats(user_id: int, db: Session = Depends(get_db)):
    stats = db.query(PlayerStats).filter_by(user_id=user_id).first()
    if not stats:
        return error_response(404, "Статистика не найдена", Codes.STATS_NOT_FOUND)

    kd = stats.kills / stats.deaths if stats.deaths > 0 else stats.kills

    return success_response(
        message="Статистика получена",
        code=Codes.STATS_FETCHED,
        data={
            "user_id": stats.user_id,
            "time_played": stats.time_played,
            "kills": stats.kills,
            "deaths": stats.deaths,
            "kd_ratio": round(kd, 2)
        }
    )


@router.get("")
def get_top_stats(
    sort: str = Query("kills", enum=["kills", "deaths", "time_played"]),
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    total = db.query(PlayerStats).count()
    total_pages = math.ceil(total / pageSize)

    query = db.query(PlayerStats).order_by(getattr(PlayerStats, sort).desc())
    items = query.offset((page - 1) * pageSize).limit(pageSize).all()

    data = [
        {
            "user_id": s.user_id,
            "time_played": s.time_played,
            "kills": s.kills,
            "deaths": s.deaths
        } for s in items
    ]

    return success_response(
        message="Топ игроков получен",
        code=Codes.STATS_LIST_FETCHED,
        data={
            "items": data,
            "pagination": {
                "page": page,
                "pageSize": pageSize,
                "total": total,
                "totalPages": total_pages,
                "nextPage": page + 1 if page < total_pages else None,
                "prevPage": page - 1 if page > 1 else None
            }
        }
    )
