"""Hotel booking app - version 1 (reservations are kept in memory)."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Room:
    room_id: str      # for example "R7"
    kind: str         # "standard" or "deluxe"


@dataclass
class Booking:
    booking_id: str   # for example "R101"
    guest: str
    room_id: str
    check_in: date
    check_out: date   # the guest leaves on this day, this night is NOT booked
    status: str = "Confirmed"   # "Confirmed" or "Cancelled"

    def overlaps(self, check_in: date, check_out: date) -> bool:
        # Two stays clash if each one starts before the other one ends.
        return self.check_in < check_out and check_in < self.check_out


class BookingService:
    """The ONE place that keeps the bookings and checks for clashes."""

    def __init__(self, rooms):
        self.rooms = list(rooms)
        self.bookings = {}          # booking_id -> Booking
        self._next_number = 101

    # R1 - search free rooms
    def search_free_rooms(self, check_in: date, check_out: date):
        return [room for room in self.rooms
                if self._is_free(room.room_id, check_in, check_out)]

    # R2 + R3 - book a room, or refuse a clash
    def book(self, guest: str, room_id: str, check_in: date, check_out: date):
        if check_out <= check_in:
            return "Unavailable", None
        if not self._is_free(room_id, check_in, check_out):
            return "Unavailable", None           # nothing is created
        booking = Booking(f"R{self._next_number}", guest, room_id,
                          check_in, check_out)
        self._next_number += 1
        self.bookings[booking.booking_id] = booking
        return "Accepted", booking

    # R4 - cancel a booking
    def cancel(self, booking_id: str) -> bool:
        booking = self.bookings.get(booking_id)
        if booking is None:
            return False
        booking.status = "Cancelled"
        return True

    # R5 - view a booking
    def get_booking(self, booking_id: str):
        return self.bookings.get(booking_id)

    def _is_free(self, room_id: str, check_in: date, check_out: date) -> bool:
        for b in self.bookings.values():
            if (b.room_id == room_id and b.status == "Confirmed"
                    and b.overlaps(check_in, check_out)):
                return False
        return True


def show(booking: Booking) -> str:
    return (f"{booking.booking_id}: {booking.guest}, {booking.room_id}, "
            f"{booking.check_in:%d %b}-{booking.check_out:%d %b}, "
            f"{booking.status}")


def main():
    service = BookingService([Room("R7", "standard"), Room("R8", "deluxe")])
    d12, d13, d14, d15 = (date(2026, 11, n) for n in (12, 13, 14, 15))

    free = service.search_free_rooms(d12, d14)
    print("Free 12-14 Nov:", [r.room_id for r in free])           # R7, R8

    result, maya = service.book("Maya", "R7", d12, d14)
    print("Maya books R7 12-14 Nov:", result, maya.booking_id)    # Accepted R101

    result, _ = service.book("Omar", "R7", d13, d15)
    print("Omar asks R7 13-15 Nov:", result)                      # Unavailable

    print("View:", show(service.get_booking("R101")))

    service.cancel("R101")
    print("After cancel:", show(service.get_booking("R101")))
    free = service.search_free_rooms(d12, d14)
    print("Free 12-14 Nov again:", [r.room_id for r in free])     # R7, R8


if __name__ == "__main__":
    main()