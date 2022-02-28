import random
import unittest as ut
from assignment import Reservation, ReservationType


'''
TODO: Disable logging for test
TODO: Check for empty spaces along with safety buffer

'''

class TestReservation(ut.TestCase):
    def testBookSeats(self):
        rows = 10
        seats = 20

        reservationNumber = "Rxxx"
        reservation = Reservation(rows,seats)

        rowNum = random.randint(0,rows-1)
        seatsToBeReserved = random.randint(1,seats)

        reservation.bookSeats(rowNum,reservationNumber,seatsToBeReserved)

        if reservation.rowAvailability[rowNum]['startFromLeft']:
            for i in range(seatsToBeReserved):
                self.assertEqual((ReservationType.Booked,reservationNumber),reservation.reservationMatrix[rowNum][i])
        else:
            for i in range(seats-1,seats-seatsToBeReserved,-1):
                self.assertEqual((ReservationType.Booked,reservationNumber),reservation.reservationMatrix[rowNum][i])

        

if __name__ == '__main__':
    ut.main()