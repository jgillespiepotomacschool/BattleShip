from Player import Player
import random

class smartComputerPlayer(Player):

    def __init__(self):
        super().__init__()
        self.firstHit = False

        self.shotXTemp = -1
        self.shotYTemp = -1
        self.shotXReverse = 10
        self.shotYReverse = -1
    #finds the first hit
    def findFirstX(self):
        while True and self.firstHit: #while there has been a hit, find it
            col = random.randint(0, 9)
            row = random.randint(0, 9)
            if(self.gridShots.returnLocation(row, col) == "X"):
                return [row, col]
        return [-1, -1]

    def checkOverlapping(self, size, vOrH, rowStart, colStart):
        if vOrH == 0:  # if vertical, check veritcaly for overlaps
            for i in range(size):  # traverse grid based on ship size
                if not self.gridShips.isSpaceWater(i + rowStart - 1,
                                                   colStart - 1):  # if there is an overlap, return false
                    return False
        elif vOrH == 1:  # if horozontal, check for overlaps.
            for k in range(size):  # traverse grid based on ship size
                if not self.gridShips.isSpaceWater(rowStart - 1,
                                                   k + colStart - 1):  # if there is an overlap return false
                    return False
        return True

    def shootRandom(self): #shooting random algorithm
        if self.shotXTemp < 9: #adjust shots
            self.shotXTemp +=1
            self.shotYTemp +=1
            print("shooting at", self.shotXTemp, ", ", self.shotYTemp)
            return [self.shotXTemp, self.shotYTemp] #returns randomx and randomy
        if self.shotXReverse > 0: #adjust shots
            self.shotXReverse -= 1
            self.shotYReverse += 1
            return [self.shotXReverse, self.shotYReverse] #returns randomx and randomy

        return [random.randrange(0, 10), random.randrange(0, 10)]



    def takeTurn(self, otherPlayer):
        direction = random.randint(1, 4)
        startx = -1
        starty = -1

        smartShotInvalid = False

        if not self.firstHit: #if there isnt a hit, go random
            self.shootSpot = self.shootRandom()
            startx = self.shootSpot[0]
            starty = self.shootSpot[1]
        else:
            target = self.findFirstX()

            try:
                self.gridShots.isSpaceWater(target[0], target[1] - 1)
                self.gridShots.isSpaceWater(target[0], target[1] + 1)
                self.gridShots.isSpaceWater(target[0] - 1, target[1])
                self.gridShots.isSpaceWater(target[0] + 1, target[1])
            except:
                smartShotInvalid = True
            # this if statement shoots around a hit to try to hit the same ship
            if smartShotInvalid or (self.gridShots.isSpaceWater(target[0], target[1] - 1) == False) and (self.gridShots.isSpaceWater(target[0], target[1] + 1) == False) and (self.gridShots.isSpaceWater(target[0] - 1, target[1]) == False) and (self.gridShots.isSpaceWater(target[0] + 1, target[1])  == False):
                self.shootSpot = self.shootRandom()
                startx = self.shootSpot[0]
                starty = self.shootSpot[1]
            elif(direction == 1): #up
                startx = target[0]
                starty = target[1] - 1
            elif (direction == 2):  # down
                startx = target[0]
                starty = target[1] + 1
            elif (direction == 3):  # left
                startx = target[0] - 1
                starty = target[1]
            elif (direction == 4):  # right
                startx = target[0] + 1
                starty = target[1]
        #recursion to shoot if shot is invalid
        if (not self.gridShots.isSpaceWater(startx, starty)) or (0 > startx > 9 or 0 > starty > 9):
            self.takeTurn(otherPlayer)
        if not otherPlayer.gridShips.isSpaceWater(startx, starty) and not otherPlayer.gridShips.returnLocation(startx, starty) == "O":
            self.gridShots.changeSingleSpace(startx, starty, "X")
            otherPlayer.gridShips.changeSingleSpace(startx, starty, "X")
            self.firstHit = True
        else:
            self.gridShots.changeSingleSpace(startx, starty, "O")
            otherPlayer.gridShips.changeSingleSpace(startx, starty, "O")

    def placeShip(self, ship, size):
        count = 1
        while count > 0:
            vOrH = random.randint(0, 1)
            colStart = random.randint(1, 10)
            rowStart = random.randint(1, 10)

            if 10 >= colStart >= 1 and 10 >= rowStart >= 1 and self.gridShips.isSpaceWater(rowStart - 1, colStart - 1):
                if vOrH == 0:
                    if rowStart - 1 + size <= 9 and self.checkOverlapping(size, vOrH, rowStart, colStart):
                        self.gridShips.changeCol(colStart - 1, ship, rowStart - 1, size)
                        self.printGrids()
                    else:
                        count += 1
                elif vOrH == 1:
                    if colStart - 1 + size <= 9 and self.checkOverlapping(size, vOrH, rowStart, colStart):
                        self.gridShips.changeRow(rowStart - 1, ship, colStart - 1, size)
                        self.printGrids()
                    else:
                        count += 1
                else:
                    count += 1
            else:
                count += 1
            count -= 1

        # this method will determine if the Player's ship grid still
        # has ships or not
        # If they have no ships left, the other player wins
        # This method returns true if they still have ships
        # This method returns false if they don't have ships

    def stillHasShips(self):
        for j in range(10):
            for k in range(10):
                if not self.gridShips.returnLocation(j, k) == "~" and not self.gridShips.returnLocation(j,k) == "X" and not self.gridShips.returnLocation(j, k) == "O":
                    return True
        return False

