from Player import Player

class HumanPlayer(Player):
    def __init__ (self):
        super().__init__()

    def placeShip(self, ship , size ):
        # over write in the HumanPlayer and ComputerPlayer subclasses
        pass


    def takeTurn(self):
        # over write in the HumanPlayer and ComputerPlayer subclasses
        pass

hp = HumanPlayer()
hp.placeShip("B",4)
hp.printGrids()