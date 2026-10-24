"""Step 8 - the race: two people book the same room at the same moment."""

import threading
import time
from datetime import date

from hotel_booking import BookingService, Room

class SlowService(BookingService):
    """Same app, but the check is slow (like a real website or database).
    This makes the problem easy to see every time."""

    def _is_free(self, room_id, check_in, check_out):
        free = super()._is_free(room_id, check_in, check_out)
        time.sleep(0.2)          # between "is it free?" and "save the booking"
        return free


service = SlowService([Room("R7", "standard"), Room("R8", "deluxe")])
results = {}


def try_book(guest, check_in, check_out):
    results[guest] = service.book(guest, "R7", check_in, check_out)[0]


maya = threading.Thread(target=try_book, args=("Maya", date(2026, 11, 12), date(2026, 11, 14)))
omar = threading.Thread(target=try_book, args=("Omar", date(2026, 11, 13), date(2026, 11, 15)))

maya.start()
omar.start()
maya.join()
omar.join()

print("Results:", results)
print("Bookings in the list:")
for b in service.bookings.values():
    print(" ", b.booking_id, b.guest, b.room_id, b.check_in, b.check_out)

confirmed = [b for b in service.bookings.values() if b.room_id == "R7"]
if len(confirmed) > 1:
    print("PROBLEM: R7 is booked twice for the night of 13 November!")
else:
    print("OK: only one booking for R7.")
