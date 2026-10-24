# Requirements

## R1 · Search free rooms
The app shows which rooms are free for a given check-in and check-out date.
Example: free rooms from 12 to 14 November -> R7, R8.
Proof: after a booking exists, its room no longer appears in the search for those nights.

## R2 · Book a room
The app books a free room for a guest and gives back a booking id.
Example: Maya books R7 for 12-14 November -> Accepted, id R101.
Proof: the new booking can be found by its id.

## R3 · Refuse a clash
One room, one night, at most one guest. If any night is already taken, the app answers Unavailable and creates nothing.
Example: Omar asks for R7 on 13-15 November -> Unavailable (13 November is taken).
Proof: after the refusal, the list of bookings has not changed.

## R4 · Cancel a booking
The app cancels a booking by its id, and the room becomes free again for those nights.
Example: Maya cancels R101 -> R7 is free again for 12-14 November.
Proof: the same room can now be booked again for those nights.

## R5 · View a booking
The app shows one booking by its id: guest, room, dates and status.
Example: R101 -> Maya, R7, 12-14 November, Confirmed.
Proof: after cancelling, the status shows Cancelled.