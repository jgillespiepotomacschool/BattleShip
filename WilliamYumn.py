from computer_player import ComputerPlayer
import random


class SmartComputerPlayer(ComputerPlayer):

    def __init__(self):
        super().__init__()
        self.lastShot = [0, 0]
        self.activeTarget = False
        self.previousHit = False
        self.directionOfNextShot = 0
        self.firstShipHit = [-1, -1]
        self.evenCheckerboardSpaces = 0

    def takeTurn(self, otherPlayer):
        if self.firstShipHit[0] != -1 or self.firstShipHit[1] != -1: #runs lateral movement code if it is targeting a ship
            cannotMoveUp = True # assumes by default that lateral movement in each direction is false
            cannotMoveLeft = True
            cannotMoveRight = True
            cannotMoveDown = True
            if not self.previousHit: # returns to initial hit when it passes the eddge of the ship
                r = self.firstShipHit[0]
                c = self.firstShipHit[1]
                self.directionOfNextShot += 2 # changes direction of movement
                if self.directionOfNextShot >= 4:
                    self.directionOfNextShot -= 4
            else: # continues moving toward the next ship space
                r = self.lastShot[0]
                c = self.lastShot[1]
            try:
                cannotMoveUp = not self.gridShots.isSpaceWater(r - 1, c) # checks if the space above has not been checked yet
            except IndexError: # moving up is prevented by default if the index does not exist
                pass
            try:
                cannotMoveRight = not self.gridShots.isSpaceWater(r, c + 1) # checks if the space to the right has not been checked yet
            except IndexError: # moving right is prevented by default if the index does not exist
                pass
            try:
                cannotMoveDown = not self.gridShots.isSpaceWater(r + 1, c) # checks if the space below has not been checked yet
            except IndexError: # moving down is prevented by default if the index does not exist
                pass
            try:
                cannotMoveLeft = not self.gridShots.isSpaceWater(r, c - 1) # checks if the space to the left has not been checked yet
            except IndexError: # moving left is prevented by default if the index does not exist
                pass

            originalDirection = self.directionOfNextShot
            while True: # does a strategic lateral movement shot based on points surrounding the first hit on the ship
                if self.directionOfNextShot == 0 and not cannotMoveUp: # runs when moving up from the last point as long as the coordinate is a legal shot
                    self.shoot(otherPlayer, r - 1, c)
                    self.lastShot = [r - 1, c]
                    if (r-1 + c) % 2 == 0: # keeps track of the "even" spaces
                        self.evenCheckerboardSpaces += 1
                    return
                elif self.directionOfNextShot == 1 and not cannotMoveRight: # runs when moving right from the last point as long as the coordinate is a legal shot
                    self.shoot(otherPlayer, r, c + 1)
                    self.lastShot = [r, c + 1]
                    if (r + c+1) % 2 == 0: # keeps track of the "even" spaces
                        self.evenCheckerboardSpaces += 1
                    return
                elif self.directionOfNextShot == 2 and not cannotMoveDown: # runs when moving down from the last point as long as the coordinate is a legal shot
                    self.shoot(otherPlayer, r + 1, c)
                    self.lastShot = [r + 1, c]
                    if (r+1 + c) % 2 == 0: # keeps track of the "even" spaces
                        self.evenCheckerboardSpaces += 1
                    return
                elif self.directionOfNextShot == 3 and not cannotMoveLeft: # runs when moving left from the last point as long as the coordinate is a legal shot
                    self.shoot(otherPlayer, r, c - 1)
                    self.lastShot = [r, c - 1]
                    if (r + c-1) % 2 == 0: # keeps track of the "even" spaces
                        self.evenCheckerboardSpaces += 1
                    return
                else: # rotates to a different direction if the currently set direction is illegal
                    self.directionOfNextShot += 1
                    if self.directionOfNextShot == 4: # resets the 4 direction to 0
                        self.directionOfNextShot = 0
                    if self.directionOfNextShot == originalDirection: # if all surrounding points are illegal, it resorts to random ship placement
                        self.firstShipHit = [-1, -1]
                        break

        while True: # runs until a legal shot is taken
            r = random.randint(0, 9)
            # c = random.randint(0, 9)
            if self.evenCheckerboardSpaces < 50: # exhausts "even" spaces before "odd" spaces
                if r%2 == 0: # matches even row with even column
                    c = random.randint(0, 4)*2
                else: # matches odd row with odd column
                    c = random.randint(0, 4)*2+1
            else:
                if r%2 == 0: # matches even row with odd column
                    c = random.randint(0, 4)*2+1
                else: # matches odd row with even column
                    c = random.randint(0, 4) * 2
            print(r, c)
            print('generate random number')
            #if (r + c) % 2 == 0:
                #continue
            if self.gridShots.isSpaceWater(r, c):  # repeats previous step if it has already shot in that space
                print("random move")
                if not otherPlayer.gridShips.isSpaceWater(r, c): # recognizes the existence of a ship at that point
                    self.firstShipHit = [r, c]
                self.shoot(otherPlayer, r, c)
                self.lastShot = [r, c]
                if (r + c) % 2 == 0: # keeps track of the "even" spaces shot at
                    self.evenCheckerboardSpaces += 1
                return

    def shoot(self, otherPlayer, r, c):
        print("shoot")
        if otherPlayer.gridShips.isSpaceWater(r, c):  # the shot is a miss
            self.gridShots.changeSingleSpace(r, c, "0")
            otherPlayer.gridShips.changeSingleSpace(r, c, "0")
            print("Miss")
            self.previousHit = False
        else:  # the shot is a hit
            destroyedShip = otherPlayer.gridShips.returnLocation(r, c)  # store ship type for later
            self.gridShots.changeSingleSpace(r, c, "X")
            otherPlayer.gridShips.changeSingleSpace(r, c, "X")
            isDestroyed = True
            for r in range(10):  # traverses 2D grid
                for c in range(10):
                    if otherPlayer.gridShips.returnLocation(r,
                                                            c) is destroyedShip:  # checks each space if any parts of the ship aren't sunk
                        isDestroyed = False
                        break
                if not isDestroyed:
                    break
            if isDestroyed:
                print("You sank the", destroyedShip, "battleship")
                self.firstShipHit = [-1, -1]
                self.previousHit = False
            else:
                print("Hit!")
                self.previousHit = True
                print(r, c)
