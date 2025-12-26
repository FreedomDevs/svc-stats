import math
from sqlalchemy.orm import Session
from models import PlayerStats


class StatsService:

    @staticmethod
    def create_stats(db: Session, user_id: int) -> PlayerStats:
        if db.query(PlayerStats).filter_by(user_id=user_id).first():
            raise ValueError("STATS_ALREADY_EXISTS")

        stats = PlayerStats(user_id=user_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
        return stats

    @staticmethod
    def update_stats(
        db: Session,
        user_id: int,
        time_played: int,
        kills: int,
        deaths: int
    ) -> PlayerStats:
        stats = db.query(PlayerStats).filter_by(user_id=user_id).first()
        if not stats:
            raise ValueError("STATS_NOT_FOUND")

        stats.time_played = time_played
        stats.kills = kills
        stats.deaths = deaths
        db.commit()
        return stats

    @staticmethod
    def get_stats(db: Session, user_id: int) -> dict:
        stats = db.query(PlayerStats).filter_by(user_id=user_id).first()
        if not stats:
            raise ValueError("STATS_NOT_FOUND")

        kd = stats.kills / stats.deaths if stats.deaths > 0 else stats.kills

        return {
            "user_id": stats.user_id,
            "time_played": stats.time_played,
            "kills": stats.kills,
            "deaths": stats.deaths,
            "kd_ratio": round(kd, 2)
        }

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

        return data, pagination
