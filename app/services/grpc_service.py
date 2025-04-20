import grpc

from app.config import settings
from app.proto import booking_pb2, booking_pb2_grpc


class GrpcService:
    def __init__(self, auth_token: str = None):
        self.channel = grpc.insecure_channel(
            f"{settings.GRPC_SERVICE_HOST}:{settings.GRPC_SERVICE_PORT}"
        )
        if auth_token:
            self.metadata = [("authorization", f"Bearer {auth_token}")]
        else:
            self.metadata = None

        self.booking_stub = booking_pb2_grpc.BookingServiceStub(self.channel)

    async def close(self):
        await self.channel.close()

    async def create_booking(self, booking_data: dict):
        """
        booking_data: Dict
            - user_id
            - barber_id
            - start_time:
            - service_type: Enum
            - notes
        """
        if not self.metadata:
            raise Exception("No auth token provided")

        request = booking_pb2.CreateBookingRequest(
            user_id=booking_data.get("user_id"),
            barber_id=booking_data.get("barber_id"),
            start_time=booking_data.get("start_time"),
            service_type=booking_data.get("service_type"),
            notes=booking_data.get("notes", ""),
        )

        response = self.booking_stub.CreateBooking(request, metadata=self.metadata)
        return self._booking_to_dict(response)

    async def get_user_bookings(self, query: dict):
        if not self.metadata:
            raise Exception("No auth token provided")

        request = booking_pb2.GetUserBookingsRequest(user_id=query.get("user_id", 0))
        response = self.booking_stub.GetUserBookings(
            request, metadata=self.metadata
        )
        return [self._booking_to_dict(booking) for booking in response.bookings]

    async def get_barber_bookings(self, query: dict):
        if not self.metadata:
            raise Exception("No auth token provided")

        request = booking_pb2.GetBarberBookingsRequest(
            barber_id=query.get("barber_id", 0)
        )
        response = self.booking_stub.GetBarberBookings(request, metadata=self.metadata)
        return [self._booking_to_dict(booking) for booking in response.bookings]

    def _booking_to_dict(self, booking):
        return {
            "id": booking.id,
            "user_id": booking.user_id,
            "barber_id": booking.barber_id,
            "start_time": booking.start_time,
            "end_time": booking.end_time,
            "service_type": booking_pb2.ServiceType.Name(booking.service_type),
            "status": booking_pb2.BookingStatus.Name(booking.status),
            "notes": booking.notes,
            "created_at": booking.created_at,
            "updated_at": booking.updated_at,
        }
