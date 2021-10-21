from HumanPlayer import HumanPlayer
from ComputerPlayer import ComputerPlayer


hp = HumanPlayer()
hp.placeShip( "A" , 5)
cp = ComputerPlayer()
cp.placeShip("A" , 5)

for i in range( 100 ):
    #cp.takeTurn( hp )
    hp.takeTurn( cp )
    hp.printGrids()
    cp.printGrids()