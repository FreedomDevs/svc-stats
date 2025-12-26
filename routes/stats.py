from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID

class StatsResponse(BaseModel):
    user_id: UUID

from database import SessionLocal
from schemas import StatsUpdate
from services.stats_service import StatsService
from responses import (
    success_response,
    error_response,
    success_pagination_response
)
from codes import Codes

router = APIRouter(prefix="/stats", tags=["stats"]) #Все эндпоинты будут начинаться с /stats


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Создание статистики игрока
@router.post("/{user_id}")
def create_stats(user_id: UUID, db: Session = Depends(get_db)):
    try:
        StatsService.create_stats(db, user_id)
        return success_response(
            message="Статистика создана",
            code=Codes.STATS_CREATED,
            data={"user_id": str(user_id)}
        )

    except ValueError: #Ловим доменную ошибку и превращаем её в HTTP
        return error_response(
            409,
            "Статистика уже существует",
            Codes.STATS_ALREADY_EXISTS
        )

#Обновляем статистику
@router.patch("/{user_id}")
def update_stats(user_id: UUID, payload: StatsUpdate, db: Session = Depends(get_db)):
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
def get_stats(user_id: UUID, db: Session = Depends(get_db)):
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
    data, pagination = StatsService.get_top_stats( #Получаем готовые данные из сервиса
        db,
        sort,
        page,
        pageSize
    )
#Route только упаковывает ответ, не считает ничего
    return success_pagination_response(
        message="Топ игроков получен",
        code=Codes.STATS_LIST_FETCHED,
        data={"items": data},
        pagination=pagination
    )
