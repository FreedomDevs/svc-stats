import grpc
from concurrent import futures
from uuid import UUID

from app.database import SessionLocal
from app.services.stats_service import StatsService

import app.grpc.stats_pb2 as pb2
import app.grpc.stats_pb2_grpc as pb2_grpc


class StatsGrpcService(pb2_grpc.StatsServiceServicer):

    def GetStats(self, request, context):
        db = SessionLocal()
        try:
            data = StatsService.get_stats(
                db,
                UUID(request.user_id),
                request.server_name
            )

            return pb2.GetStatsResponse(
                user_id=data["user_id"],
                server_name=data["server_name"],
                time_played=data["time_played"],
                kills=data["kills"],
                deaths=data["deaths"],
                kd_ratio=data["kd_ratio"]
            )

        except ValueError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Stats not found")
            return pb2.GetStatsResponse()

        finally:
            db.close()

    def UpdateStats(self, request, context):
        db = SessionLocal()
        try:
            StatsService.update_stats(
                db,
                UUID(request.user_id),
                request.server_name,
                request.time_played,
                request.kills,
                request.deaths
            )

            return pb2.Empty()

        except ValueError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Stats not found")
            return pb2.Empty()

        finally:
            db.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_StatsServiceServicer_to_server(
        StatsGrpcService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")

    server.wait_for_termination()