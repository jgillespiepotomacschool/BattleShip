from HumanPlayer import HumanPlayer
from ComputerPlayer import ComputerPlayer


hp = HumanPlayer()
hp.placeShip( "A" , 5)
cp = ComputerPlayer()
cp.placeShip("A" , 5)

while True:
    #cp.takeTurn( hp )
    hp.takeTurn( cp )
    hp.printGrids()
    cp.printGrids()