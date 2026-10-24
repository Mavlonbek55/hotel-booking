# Design notes

## Step 1 · Why design first

If the developers had started coding without a plan, nobody would have
decided who checks the rule "one room, one night, at most one guest".
The website and the reception desk would each use their own copy of the
bookings (the spreadsheet), so both could see R7 as free and book it for
the same nights. Maya and Omar would both arrive on the 13th with a
booking for R7. A design makes us decide first that there is ONE shared
list of bookings and ONE place that checks for clashes. Fixing this
before coding is much cheaper than fixing it after the guests arrive.

## Step 3 · Use cases

Two actors, Guest and Receptionist, use the same four use cases.
Both go through the same app, so there is one shared list of bookings.

## Step 4 · Classes

BookingService is the only class that keeps the list of bookings and
checks clashes, so the website and reception use the same answer.

## Step 5 · Sequences

In both requests the caller talks only to BookingService.

## Step 6 · Activity

A booking is refused if the dates are wrong or any night is taken.

## Step 8 · The race

What I saw: Maya and Omar both got "Accepted" for R7, and the list
contains two bookings that share the night of 13 November.

What went wrong: book() first checks "is the room free?" and then
saves the booking. Two requests at the same moment both passed the check
before either one saved, so the rule "one room, one night, at most one
guest" was broken.

Not fixed yet: version 1 only shows the problem. A real fix comes in P09.