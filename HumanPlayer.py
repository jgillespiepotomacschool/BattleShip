from Player import Player

class HumanPlayer(Player):
    def __init__ (self):
        self.shipDictionary = {
            "A": "Aircraft Carrier",
            "B": "Battleship",
            "C": "Cruiser",
            "D": "Destroyer",
            "S": "Submarine"
        }
        super().__init__()

    def placeShip(self, ship , size ):
        self.printGrids()
        while True:
            print("Lets place your " , self.shipDictionary[ship] )
            print("It takes up",size,"Spaces")
            isVertical = int (input("Please input 1 for vertical, and 0 for horitzonal"))
            row = int(input("Please enter in 0 - 9 for the row") )
            col = int(input("Please enter in 0 - 9 for the column"))
            if isVertical < 0 or isVertical > 1 or row > 9 or row < 0 or col > 9 or col < 0 :
                continue

            # 1 is vertical, 0 is horizonal
            if isVertical == 1 :
                if self.canBePlaced(isVertical, row, col, size):
                    self.gridShips.changeCol(col, ship, row, size)
                    break
                else:
                    print("Your entry was invalid, please try again")
                    continue
            else:
                if self.canBePlaced(isVertical, row, col, size):
                    self.gridShips.changeRow(row, ship, col, size)
                    break
                else:
                    print("Your entry was invalid, please try again")
                    continue


    def takeTurn(self , otherPlayer):
        while True:
            print("Its time to take your shot")
            row = int(input("Please enter in 0 - 9 for the row"))
            col = int(input("Please enter in 0 - 9 for the column"))
            if row > 9 or row < 0 or col > 9 or col < 0:
                continue
            if self.gridShots.isSpaceWater(row, col):
                if otherPlayer.gridShips.isSpaceWater(row, col):
                    otherPlayer.gridShips.changeSingleSpace(row, col, "o")
                    self.gridShots.changeSingleSpace(row, col, "o")
                    print("You missed")
                    break
                else:
                    hitShip = otherPlayer.gridShips.returnLocation(row, col)
                    otherPlayer.gridShips.changeSingleSpace(row, col, "x")
                    self.gridShots.changeSingleSpace(row, col, "x")
                    print("You hit a ship")
                    if self.sinkShip(otherPlayer, hitShip):
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

