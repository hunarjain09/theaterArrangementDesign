import collections
from enum import Enum
import os


class ReservationType(Enum):
    Empty = 1
    Booked = 2
    SafetyBuffer = 3


class Reservation:

    def __init__(self,rows,cols,safetyBuffer=3) -> None:
        ## Initialising the Rows, Cols and Safety Buffer
        self.rows = rows
        self.cols = cols
        self.safteyBuffer = safetyBuffer ## Cannot exceed the cols.

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
        return ','.join(bookingDetails)

    def getAssignment(self,reservationNumber,seatsToBeReserved):

        bookingDetails = 'Not enough seats to accommodate!'

        ## TODO: TreeMap can be used, sortedContainers in python for log(n) --> lookup.
        for i in range(self.rows-1,-1,-1):
            if self.rowAvailability[i]['availableSeats'] >= seatsToBeReserved:
                bookingDetails = self.bookSeats(i,reservationNumber,seatsToBeReserved)
                break

        ## TODO: Recursive calls can be done if seatsToBeReserved can be chunked.

        return reservationNumber+' '+bookingDetails

    def getRowName(self,index):
        return chr(ord('A')+index)

#####################################################################################



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



##TODO: Error Handling to better handle edge cases.
##TODO: If we skip rows then customer satifaction will be compromised. (Idea of filling even rows first and then the odd ones for each half). 
##TODO: Approach using Priority Queues --> Problems of maintaining two of them.
##TODO: Tree Map and Sorted Containers. 
##TODO: Store them in a queue and process them together instead of multiple function calls if the data is not a streaming one. 
##TODO: Filling from centers will cause more gaps that's why initialised from ends. 
##TODO: Multiple IDs after sometime are allowed in the current implementation.
