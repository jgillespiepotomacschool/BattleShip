import random
from Player import Player


class AdvancedComputerPlayer(Player):

    def __init__(self):
        Player.__init__(self)
        self.hitsA = 0  # the hits on this player's Aircraft Carrier (by the opponent)
        self.hitsB = 0
        self.hitsC = 0
        self.hitsS = 0
        self.hitsD = 0
        self.fireList = []
        self.searching = True
        self.totalHits = 0  # the total number of hits on the player's shot grid
        self.totalSpacesSunk = 0  # the total number of spaces on all sunk ships on the player's shot grid

    def takeTurn(self, otherPlayer):
        """Allows the computer to take a turn, consisting of firing at specific location and checking if a ship
        was hit.

        If a ship was hit, the variable corresponding to the number of hits on that ship is increased by 1.

        :param otherPlayer: an object of the HumanPlayer class
        """
        self.stillSearching()
        fireLoc = self.whereToFire()
        print(fireLoc)
        fireRow = fireLoc[0]
        fireCol = fireLoc[1]

        if otherPlayer.gridShips.returnLocation(fireRow, fireCol) == 'A':  # if shot hits the Aircraft Carrier
            otherPlayer.hitsA += 1
            self.shotHit(otherPlayer, fireRow, fireCol, "A")
        elif otherPlayer.gridShips.returnLocation(fireRow, fireCol) == 'B':  # if shot hits the Battleship
            otherPlayer.hitsB += 1
            self.shotHit(otherPlayer, fireRow, fireCol, "B")
        elif otherPlayer.gridShips.returnLocation(fireRow, fireCol) == 'C':  # if shot hits the Cruiser
            otherPlayer.hitsC += 1
            self.shotHit(otherPlayer, fireRow, fireCol, "C")
        elif otherPlayer.gridShips.returnLocation(fireRow, fireCol) == 'S':  # if shot hits the Submarine
            otherPlayer.hitsS += 1
            self.shotHit(otherPlayer, fireRow, fireCol, "S")
        elif otherPlayer.gridShips.returnLocation(fireRow, fireCol) == 'D':  # if shot hits the Destroyer
            otherPlayer.hitsD += 1
            self.shotHit(otherPlayer, fireRow, fireCol, "D")
        else:  # if the shot misses
            print("The CPU missed.")
            otherPlayer.gridShips.changeSingleSpace(fireRow, fireCol, "O")
            self.gridShots.changeSingleSpace(fireRow, fireCol, "O")
            self.fireList.append((fireRow, fireCol, "O"))
        print(("-" * 40) + "YOUR SHIP GRID" + ("-" * 40))
        otherPlayer.gridShips.printGrid()

    def shotHit(self, otherPlayer, fireRow, fireCol, ship):
        """This function is used to change the grid space where the ship was hit (on the AdvancedComputerPlayer's
        shot grid and the HumanPlayer's ship grid)

        It also gives the user a message if one of there ships was sunk.

        :param otherPlayer: an object of the HumanPlayer class
        :param fireRow: an int that contains the row of the shot fired by the AdvancedComputerPlayer object
        :param fireCol: an int that contains the column of the shot fired by the AdvancedComputerPlayer object
        :param ship: a single-letter String corresponding to the type of ship that was hit
        """
        varLib = {
            "A": otherPlayer.hitsA,
            "B": otherPlayer.hitsB,
            "C": otherPlayer.hitsC,
            "D": otherPlayer.hitsD,
            "S": otherPlayer.hitsS
        }
        nameLib = {
            "A": "Aircraft Carrier",
            "B": "Battleship",
            "C": "Cruiser",
            "D": "Destroyer",
            "S": "Submarine"
        }
        sizeLib = {
            "A": 5,
            "B": 4,
            "C": 3,
            "D": 2,
            "S": 3
        }

        self.searching = False
        self.totalHits += 1
        print("The CPU hit your ship!")
        self.gridShots.changeSingleSpace(fireRow, fireCol, 'X')
        otherPlayer.gridShips.changeSingleSpace(fireRow, fireCol, 'X')
        self.fireList.append((fireRow, fireCol, 'X'))
        if varLib[ship] == sizeLib[ship]:  # if the cpu has hit the ship enough to sink it
            print("The CPU sunk your", nameLib[ship], "!")
            self.totalSpacesSunk += sizeLib[ship]

    def whereToFire(self):
        """Determines which location to fire at next.

        :return: a tuple containing the row and column of the next shot to be fired
        """
        if self.searching:  # if the AdvancedComputerPlayer is searching for a ship to hit
            while True:
                fireRow = random.randint(0, 9)
                fireCol = random.randint(0, 9)

                # if the space is legal and the sum of the row and column of the shot
                # to be fired is evenly numbered (OPTIMIZATION)
                if self.gridShots.isSpaceWater(fireRow, fireCol) and (fireRow + fireCol) % 2 == 0:
                    return fireRow, fireCol
        else:  # if the AdvancedComputerPlayer found a ship to continue firing at

            # traverses fireList in reverse
            for index, current_tuple in enumerate(reversed(self.fireList)):

                optimal_row = current_tuple[0]
                optimal_column = current_tuple[1]

                if self.fireList.__len__() > 1 and \
                        self.fireList[index][2] == 'X' and self.fireList[index - 1][
                    2] == 'X':  # used to check if a ship was hit twice in a row

                    # this outer if-elif-else statement is used to determine the orientation of the hits
                    if abs(current_tuple[1] - self.fireList[index - 1][1]) == 1:

                        # this if-elif-else statement determines if the optimal column is legal (INNERMOST)
                        if (optimal_column + 1 >= 0) and (optimal_column + 1 < 10) \
                                and self.gridShots.isSpaceWater(optimal_row, optimal_column + 1):
                            optimal_column += 1
                            return optimal_row, optimal_column
                        elif (optimal_column - 1 >= 0 and optimal_column - 1 < 10) \
                                and self.gridShots.isSpaceWater(optimal_row, optimal_column - 1):
                            optimal_column -= 1
                            return optimal_row, optimal_column
                    elif abs(current_tuple[0] - self.fireList[index - 1][0]) == 1:

                        # this if-elif-else statement determines if the optimal row is legal (INNERMOST)
                        if (optimal_row + 1 >= 0) and (optimal_row + 1 < 10) \
                                and self.gridShots.isSpaceWater(optimal_row + 1, optimal_column):
                            optimal_row += 1
                            return optimal_row, optimal_column
                        elif (optimal_row - 1 >= 0) and (optimal_row - 1 < 10) \
                                and self.gridShots.isSpaceWater(optimal_row - 1, optimal_column):
                            optimal_row -= 1
                            return optimal_row, optimal_column
                elif current_tuple[2] == 'X':  # used to checks all spaces
                    # around the location where the ship was hit
                    possibleShots = [(current_tuple[0] + 1, current_tuple[1]),
                                     (current_tuple[0] - 1, current_tuple[1]),
                                     (current_tuple[0], current_tuple[1] + 1),
                                     (current_tuple[0], current_tuple[1] - 1)]

                    # traverses the list of tuples "possibleShots"
                    for a in possibleShots:
                        # checks if the current tuple in possibleShots is a valid location to fire a shot
                        if (0 <= a[0] < 10) and (0 <= a[1] < 10) and self.gridShots.isSpaceWater(a[0], a[1]):
                            return a[0], a[1]

                    # FAIL SAFE (if there are no more possible shots around the location of a certain hit)
                    self.searching = True
                    while True:
                        fireRow = random.randint(0, 9)
                        fireCol = random.randint(0, 9)

                        # if the space is legal and the sum of the row and column of the shot
                        # to be fired is evenly numbered (OPTIMIZATION)
                        if self.gridShots.isSpaceWater(fireRow, fireCol) and (fireRow + fireCol) % 2 == 0:
                            return fireRow, fireCol

    def stillSearching(self):
        """checks if the AdvancedComputerPlayer object should still be searching for a ship to hit or if it has
        found one
        """

        # checks if the total number of hits is greater than the total hits on all sunk ships
        if self.totalHits > self.totalSpacesSunk:
            self.searching = False  # not searching for a ship to hit
        else:
            self.searching = True  # searching for a ship to hit

    def placeShip(self, ship, size):
        """Places a ship on the AdvancedComputerPlayer's ship grid.

        :param ship: a single-letter String corresponding to the type of ship to be placed
        :param size: an int containing the value of the size of the ship
        """
        badship = True

        orientation = 0
        startRow = 0
        startCol = 0

        while badship:  # runs until the ship generated is valid
            badship = False
            orientation = random.randint(0, 1)

            # orientation 0 is horizontal, orientation 1 is vertical
            if orientation == 0:  # if the ship is horizontal
                startCol = random.randint(0, 10 - size)
                startRow = random.randint(0, 9)
                for i in range(size):  # runs size amount of times
                    if not self.gridShips.isSpaceWater(startRow, startCol + i):  # if the placement is not legal
                        badship = True
            elif orientation == 1:  # if the ship is vertical
                startCol = random.randint(0, 9)
                startRow = random.randint(0, 10 - size)
                for i in range(size):  # runs size amount of times
                    if not self.gridShips.isSpaceWater(startRow + i, startCol):  # if the placement is not legal
                        badship = True

        if orientation == 0:  # if the ship is horizontal
            self.gridShips.changeRow(startRow, ship, startCol, size)
        if orientation == 1:  # if the ship is vertical
            self.gridShips.changeCol(startCol, ship, startRow, size)

    def stillHasShips(self):
        """Determines if the Player's ship grid still has ships or not

        If they have no ships left, the other player wins.

        :return: True if they still have ships, False if they do not
        """

        # this if-else statement is used to determine whether the game is over (meaning that the player has
        # no more turns left)
        if self.hitsA == 5 and self.hitsB == 4 and self.hitsC == 3 and self.hitsS == 3 and self.hitsD == 2:  # if all
            # the cpu's ships have been sunk
            return False
        else:  # if the cpu still has ships
            return True

