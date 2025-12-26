from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import StatsUpdate
from services.stats_service import StatsService
from responses import (
    success_response,
    error_response,
    success_pagination_response
)
from codes import Codes

router = APIRouter(prefix="/stats", tags=["stats"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{user_id}")
def create_stats(user_id: int, db: Session = Depends(get_db)):
    try:
        StatsService.create_stats(db, user_id)
        return success_response(
            message="Статистика создана",
            code=Codes.STATS_CREATED,
            data={"user_id": user_id}
        )
    except ValueError:
        return error_response(
            409,
            "Статистика уже существует",
            Codes.STATS_ALREADY_EXISTS
        )


@router.put("/{user_id}")
def update_stats(user_id: int, payload: StatsUpdate, db: Session = Depends(get_db)):
    try:
        StatsService.update_stats(
            db,
            user_id,
            payload.time_played,
            payload.kills,
            payload.deaths
        )
        return success_response(
            message="Статистика обновлена",
            code=Codes.STATS_UPDATED
        )
    except ValueError:
        return error_response(
            404,
            "Статистика не найдена",
            Codes.STATS_NOT_FOUND
        )


@router.get("/{user_id}")
def get_stats(user_id: int, db: Session = Depends(get_db)):
    try:
        data = StatsService.get_stats(db, user_id)
        return success_response(
            message="Статистика получена",
            code=Codes.STATS_FETCHED,
            data=data
        )
    except ValueError:
        return error_response(
            404,
            "Статистика не найдена",
            Codes.STATS_NOT_FOUND
        )


@router.get("")
def get_top_stats(
    sort: str = Query("kills", enum=["kills", "deaths", "time_played"]),
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    data, pagination = StatsService.get_top_stats(
        db,
        sort,
        page,
        pageSize
    )

    return success_pagination_response(
        message="Топ игроков получен",
        code=Codes.STATS_LIST_FETCHED,
        data={"items": data},
        pagination=pagination
    )
