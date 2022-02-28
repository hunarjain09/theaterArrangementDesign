import logging
import random
import unittest as ut
from assignment import Reservation, ReservationType


'''
TODO: Disable logging for test

'''

class TestReservation(ut.TestCase):
    def testBookSeats(self):
        ## Data Preparation
        rows = 10
        seats = 20
        safetyBuffer = 3
        reservationNumber = "Rxxx"
        reservation = Reservation(rows,seats,safetyBuffer)
        
        rowNum = random.randint(0,rows-1)
        seatsToBeReserved = random.randint(1,seats)
        
        logging.log(logging.INFO,f'Inside TestReservation: rowNum:{rowNum} and seatsToBeReserved:{seatsToBeReserved}')

        reservation.bookSeats(rowNum,reservationNumber,seatsToBeReserved)

        if reservation.rowAvailability[rowNum]['startFromLeft']:
            for i in range(seatsToBeReserved):
                self.assertEqual((ReservationType.Booked,reservationNumber),reservation.reservationMatrix[rowNum][i])
            while seatsToBeReserved < seats:
                if safetyBuffer > 0:
                    self.assertEqual((ReservationType.SafetyBuffer,None),reservation.reservationMatrix[rowNum][seatsToBeReserved])
                    safetyBuffer -= 1
                else:
                    self.assertEqual((ReservationType.Empty,None),reservation.reservationMatrix[rowNum][seatsToBeReserved])
                seatsToBeReserved += 1

        else:
            for i in range(seats-1,seats-seatsToBeReserved-1,-1):
                self.assertEqual((ReservationType.Booked,reservationNumber),reservation.reservationMatrix[rowNum][i])

            seatsToBeReserved = seats-seatsToBeReserved-1

            while seatsToBeReserved >= 0:
                if safetyBuffer > 0:
                    self.assertEqual((ReservationType.SafetyBuffer,None),reservation.reservationMatrix[rowNum][seatsToBeReserved])
                    safetyBuffer -= 1
                else:
                    self.assertEqual((ReservationType.Empty,None),reservation.reservationMatrix[rowNum][seatsToBeReserved])
                seatsToBeReserved -= 1

        

if __name__ == '__main__':
    ut.main()