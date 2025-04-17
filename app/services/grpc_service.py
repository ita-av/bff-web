import grpc
from app.proto import booking_pb2, booking_pb2_grpc

from app.config import settings


class GrpcService:
    def __init__(self, auth_token: str = None):
        if auth_token:
            credentials = grpc.access_token_call_credentials(auth_token)
            channel_credentials = grpc.composite_channel_credentials(
                grpc.ssl_channel_credentials(), credentials
            )
            self.channel = grpc.aio.secure_channel(
                f"{settings.GRPC_SERVICE_HOST}:{settings.GRPC_SERVICE_PORT}",
                channel_credentials,
            )
        else:
            # testing insecure channel without auth token
            self.channel = grpc.aio.insecure_channel(
                f"{settings.GRPC_SERVICE_HOST}:{settings.GRPC_SERVICE_PORT}"
            )

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
        # Convert service_type from string to enum value if needed
        service_type = booking_data.get("service_type")
        if isinstance(service_type, str):
            service_type = getattr(booking_pb2.ServiceType, service_type, 0)

        # Create the request message
        request = booking_pb2.CreateBookingRequest(
            user_id=booking_data.get("user_id"),
            barber_id=booking_data.get("barber_id"),
            start_time=booking_data.get("start_time"),
            service_type=service_type,
            notes=booking_data.get("notes", ""),
        )

        # Call the gRPC method
        response = await self.booking_stub.CreateBooking(request)

        # to dict
        return self._booking_to_dict(response)

    async def get_user_bookings(self, user_id: str):
        request = booking_pb2.GetUserBookingsRequest(user_id=user_id)
        response = await self.booking_stub.GetUserBookings(request)

        # Convert the response to a list of dicts
        return [self._booking_to_dict(booking) for booking in response.bookings]

    async def get_barber_bookings(self, barber_id: str, date: str = None):
        request = booking_pb2.GetBarberBookingsRequest(
            barber_id=barber_id, date=date or ""
        )
        response = await self.booking_stub.GetBarberBookings(request)

        # Convert the response to a list of dicts
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
