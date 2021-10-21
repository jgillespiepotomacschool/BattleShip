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


    def takeTurn(self):
        # over write in the HumanPlayer and ComputerPlayer subclasses
        pass


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

hp = HumanPlayer()
hp.createShipGrid()
hp.printGrids()