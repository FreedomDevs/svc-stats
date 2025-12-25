from .health import router as health_router
from .stats import router as stats_router

routers = [health_router, stats_router]
