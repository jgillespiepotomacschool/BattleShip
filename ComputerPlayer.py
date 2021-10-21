from Player import Player
import random

class ComputerPlayer(Player):

    def __init__(self):
        self.shipDictionary = {
            "A": "Aircraft Carrier",
            "B": "Battleship",
            "C": "Cruiser",
            "D": "Destroyer",
            "S": "Submarine"
        }
        super().__init__()

    def takeTurn(self, otherPlayer ):
        while True:
            row = random.randint( 0 , 9 )
            col = random.randint( 0 , 9 )
            if self.gridShots.isSpaceWater( row , col ) :
                if otherPlayer.gridShips.isSpaceWater( row , col ) :
                    otherPlayer.gridShips.changeSingleSpace(row,col,"o")
                    self.gridShots.changeSingleSpace(row, col, "o")
                    print("You missed")
                    break
                else:
                    hitShip = otherPlayer.gridShips.returnLocation( row , col )
                    otherPlayer.gridShips.changeSingleSpace(row, col, "x")
                    self.gridShots.changeSingleSpace(row, col, "x")
                    print("You hit a ship")
                    if self.sinkShip( otherPlayer , hitShip ) :
                        print("You sunk my", self.shipDictionary[hitShip])
                    break
            else:
                continue

    def sinkShip(self , otherPlayer , hitShip ):
        for r in range( 9 ):
            for c in range( 9 ):
                if otherPlayer.gridShips.returnLocation( r , c ) == hitShip :
                    return False
        return True

    def placeShip(self, ship , size ):
        while True:
            isVertical = random.randint(0,1)
            # 1 is vertical, 0 is horizonal
            if isVertical == 1:
                row = random.randint(0,9-size)
                col = random.randint(0,9)
                if self.canBePlaced(isVertical, row, col , size) :
                    self.gridShips.changeCol(col, ship, row, size)
                    break
                else:
                    continue
            else:
                row = random.randint(0, 9)
                col = random.randint(0, 9-size)
                if self.canBePlaced(isVertical, row, col , size):
                    self.gridShips.changeRow( row, ship, col, size)
                    break
                else:
                    continue

    def canBePlaced(self , isVertical , row , col , size ):
        # 1 is vertical, 0 is horizonal
        if isVertical == 1 :
            for r in range( size ):
                if not self.gridShips.isSpaceWater( row + r , col ) :
                    return False
        else:
            for c in range(size):
                if not self.gridShips.isSpaceWater(row, col + c):
                    return False

        return True

