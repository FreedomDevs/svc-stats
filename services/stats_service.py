import math
from sqlalchemy.orm import Session
from models import PlayerStats
from services.constants import KD_RATIO_PRECISION
from codes import Codes
from uuid import UUID


class StatsService:

# Проверяем, что у игрока ещё нет статистики
#Принимает БД-сессию
#Принимает user_id
#Возвращает ORM-объект PlayerStats
    @staticmethod
    def create_stats(db: Session, user_id: UUID) -> PlayerStats:
        if db.query(PlayerStats).filter_by(user_id=user_id).first():
            raise ValueError(Codes.STATS_ALREADY_EXISTS)

        stats = PlayerStats(user_id=user_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
        return stats #Возвращаем ORM-объект сервису/роуту

# Полное обновление статистики игрока
#Передаём поля — сервис не зависит от HTTP-схем.
    @staticmethod
    def update_stats(
        db: Session,
        user_id: UUID,
        time_played: int,
        kills: int,
        deaths: int
    ) -> PlayerStats:
        stats = db.query(PlayerStats).filter_by(user_id=user_id).first()
        if not stats:
            raise ValueError("STATS_NOT_FOUND")

        stats.time_played += time_played
        stats.kills += kills
        stats.deaths += deaths
        db.commit()
        return stats #Возвращаем обновлённую сущность (может быть полезно дальше)

# Метод возвращает не ORM, а DTO (dict) — готовый формат для API
    @staticmethod
    def get_stats(db: Session, user_id: UUID) -> dict:
        stats = db.query(PlayerStats).filter_by(user_id=user_id).first()
        if not stats:
            raise ValueError("STATS_NOT_FOUND")

        kd = stats.kills / stats.deaths if stats.deaths > 0 else stats.kills
#Формируем DTO, который готов к отдаче клиенту
        return {
            "user_id": str(stats.user_id),
            "time_played": stats.time_played,
            "kills": stats.kills,
            "deaths": stats.deaths,
            "kd_ratio": round(kd, KD_RATIO_PRECISION)
        }

# Подсчёт общего количества записей для пагинации
# Сортировка динамически по выбранному полю
#Возвращает объект пагинации
#(разделение удобно для HTTP-слоя)
    @staticmethod
    def get_top_stats(
        db: Session,
        sort: str,
        page: int,
        page_size: int
    ) -> tuple[list[dict], dict]:
        total = db.query(PlayerStats).count()
        total_pages = math.ceil(total / page_size)

        query = db.query(PlayerStats).order_by(getattr(PlayerStats, sort).desc())
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        data = [
            {
                "user_id": s.user_id,
                "time_played": s.time_played,
                "kills": s.kills,
                "deaths": s.deaths
            } for s in items
        ]

        pagination = {
            "page": page,
            "pageSize": page_size,
            "total": total,
            "totalPages": total_pages,
            "nextPage": page + 1 if page < total_pages else None,
            "prevPage": page - 1 if page > 1 else None
        }

        return data, pagination #Возвращаем чистые данные, без HTTP-логики
