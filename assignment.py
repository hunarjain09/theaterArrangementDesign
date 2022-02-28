import collections
from enum import Enum
import os
import logging

class ReservationException(Exception):
    def __init__(self, reason, details, stdout=None, stderr=None, retcode=None):
        self.reason = reason
        self.details = details
        self.stdout = stdout
        self.stderr = stderr
        self.retcode = retcode

class ReservationType(Enum):
    Empty = 1
    Booked = 2
    SafetyBuffer = 3


class Reservation:

    def __init__(self,rows,cols,safetyBuffer=3) -> None:
        ## Setting up the logger
        logging.basicConfig(filename='assignment.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)

        ## Initialising the Rows, Cols and Safety Buffer
        self.rows = rows
        self.cols = cols
        self.safteyBuffer = safetyBuffer ## Cannot exceed the cols.

        ## Total Available Seats (To avoid sum from the map)
        self.totalAvailableSeats = self.rows * self.cols 

        ## For Quick Access to Last Index
        self.rowAvailability = collections.defaultdict(dict)

        ## For Printing Purposes
        self.reservationMatrix = []

        ## Creating Matrix for Visualization
        self.createReservationMatrix()

        return

    def createReservationMatrix(self):
        for i in range(self.rows):
            temp = []
            for _ in range(self.cols):
                temp.append((ReservationType.Empty,None))
            self.reservationMatrix.append(temp)

            ## Initialising default values in the map corresponding to each row
            self.rowAvailability[i]['availableSeats'] = self.cols
            self.rowAvailability[i]['startFromLeft'] = True if i%2 == 0 else False
            self.rowAvailability[i]['lastAvailableSeat'] = 0 if self.rowAvailability[i]['startFromLeft'] else self.cols-1
        logging.info("Created Reservation Matrix")
        return
     
    def bookSeats(self,rowNum,reservationNumber,seatsToBeReserved):
        
        bookingDetails = []

        rowName = self.getRowName(rowNum)

        startIndex = self.rowAvailability[rowNum]['lastAvailableSeat']
        buffer = self.safteyBuffer
        if self.rowAvailability[rowNum]['startFromLeft']:

            while startIndex < self.cols and seatsToBeReserved > 0:
                bookingDetails.append(rowName+str(startIndex+1))
                self.reservationMatrix[rowNum][startIndex] = (ReservationType.Booked,reservationNumber)
                self.rowAvailability[rowNum]['availableSeats'] -= 1
                startIndex += 1
                seatsToBeReserved -= 1
                          
            while startIndex < self.cols and buffer > 0:
                self.reservationMatrix[rowNum][startIndex] = (ReservationType.SafetyBuffer,None)
                self.rowAvailability[rowNum]['availableSeats'] -= 1
                startIndex += 1
                buffer -= 1
        else:

            while startIndex >= 0 and seatsToBeReserved > 0:
                bookingDetails.append(rowName+str(startIndex+1))
                self.reservationMatrix[rowNum][startIndex] = (ReservationType.Booked,reservationNumber)
                self.rowAvailability[rowNum]['availableSeats'] -= 1
                startIndex -= 1
                seatsToBeReserved -= 1
                
            while startIndex >=0 and buffer > 0:
                self.reservationMatrix[rowNum][startIndex] = (ReservationType.SafetyBuffer,None)
                self.rowAvailability[rowNum]['availableSeats'] -= 1
                startIndex -= 1
                buffer -= 1

        self.rowAvailability[rowNum]['lastAvailableSeat'] = startIndex

        logging.info("Booked Seats for Reservation Number: "+reservationNumber)

        return ','.join(bookingDetails)

    def getAssignment(self,reservationNumber,seatsToBeReserved,separateRowAssignment=False):
        try:
            bookingDetails = 'Not enough seats to accommodate!'
            allAccommodatedTogether = False

            if seatsToBeReserved > self.totalAvailableSeats:
                raise ReservationException("Unavailable Seat Count",{"Reservation Number":reservationNumber,"SeatsToBeReserved":seatsToBeReserved})
 
        ## TODO: TreeMap can be used, sortedContainers in python for log(n) --> lookup.
            for i in range(self.rows-1,-1,-1):
                if self.rowAvailability[i]['availableSeats'] >= seatsToBeReserved:
                    bookingDetails = self.bookSeats(i,reservationNumber,seatsToBeReserved)
                    allAccommodatedTogether = True
                    break

        ## Accommodating greedily by allocating as my possible in a given row.
            if separateRowAssignment and not allAccommodatedTogether:
                row = self.rows - 1
                bookingDetails = ''

                while seatsToBeReserved > 0:
                    if row > 0 and self.rowAvailability[row]['availableSeats'] > 0:
                        seatsInRow = min(seatsToBeReserved, self.rowAvailability[row]['availableSeats'])
                        bookingDetails += self.bookSeats(row, reservationNumber, seatsInRow) + " "
                        seatsToBeReserved -= seatsInRow
                    row -= 1
                bookingDetails.strip()
            
            elif not allAccommodatedTogether:
                logging.info(f'Cannot Accomodate Together in {seatsToBeReserved} seats in a single row for Reservation Number: {reservationNumber}')

        except ReservationException as e:
            logging.exception("Exception Ocurred")
            return reservationNumber+' '+bookingDetails

        return reservationNumber+' '+bookingDetails

    def getRowName(self,index):
        return chr(ord('A')+index)

#####################################################################################


if __name__ == '__main__':
    rows = 10
    seats = 20
    outputFile = open("arrangementFile.txt",'w')

    reservation = Reservation(rows,seats)

    inputFileName = input("Please input the path of the file\n")

    with open(inputFileName,'r') as inputFile:
        while True:

            line  = inputFile.readline()
            if not line:
                break

            line = line.split(' ')

            reservationNumber = line[0]
            seatsToBeReserved = int(line[1])

            outputFile.write(reservation.getAssignment(reservationNumber,seatsToBeReserved)+'\n')

    print('Path of the output file:')
    print(os.path.realpath(outputFile.name))

