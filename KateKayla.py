import random
from Player import Player

class AdvancedComputerPlayer(Player):
   def __init__(self):
       Player.__init__(self)
       self.aCount = 5
       self.bCount = 4
       self.cCount = 3
       self.sCount = 3
       self.dCount = 2
       self.col = 1
       self.row = 0

   def takeTurn(self,otherPlayer):#chooses a spot to shoot
       if self.col < 8 : # if not the last column of the set
           self.shoot(otherPlayer, self.row, self.col)
           self.col = self.col+2
       elif self.col == 9 or self.col == 8  : # if last column of the set (9 first time, 8 second)
           self.shoot(otherPlayer, self.row, self.col)
           self.col = 1
           self.row = self.row+1
       if self.row > 9 : # got to last row
           self.col = 0
           self.row = 0
           self.shoot(otherPlayer, self.row, self.col)

   def placeShip(self, ship, size):# places ships
       while True:
           isVert = random.randint(0, 1)
           if (isVert == 0): # if vertical
               col = random.randint(0, 9)
               row = random.randint(0, (9 - size)) # so it fits
               if self.canBePlaced(1,row,col,size) :
                   self.gridShips.changeCol(col, ship, row, size)
                   break
               else :
                   continue
           else: # if horizontal
               col = random.randint(0, (9 - size))  # so it fits
               row = random.randint(0, 9)
               if self.canBePlaced(0, row, col, size):
                   self.gridShips.changeRow(row, ship, col, size)
                   break
               else:
                   continue

   def stillHasShips(self): # checks if game is still going
       if self.aCount == 0 and self.bCount == 0 and self.cCount == 0 and self.sCount == 0 and self.dCount == 0: # if no ships left
           return False
       else: # ships left
           return True

   def canBePlaced(self, isVertical, row, col, size): # checks if a ship can be placed in desired spot
       if isVertical == 1 :#if it is vertical
           for r in range (size) :#for loop
               if not self.gridShips.isSpaceWater(row+r, col) :#is it is not water
                   return False
       else :#if horizontal
           for c in range(size):#for loop
               if not self.gridShips.isSpaceWater(row, col+c) :#if the column is not in water
                   return False
       return True

   def shoot(self, otherPlayer, row, col):
       if otherPlayer.gridShips.isSpaceWater(row, col):  # if space is water
           print("You hit water")
           self.gridShots.changeSingleSpace(row, col, "X")
       else:
           print("You hit a ship")
           if otherPlayer.gridShots.returnLocation(col, row) == "A":  # a ship hit
               self.aCount = self.aCount - 1
               if self.aCount == 0:  # all as hit
                   print("You sunk the A ship")
           elif otherPlayer.gridShots.returnLocation(row, col) == "B":  # b ship hit
               self.bCount = self.bCount - 1
               if self.bCount == 0:  # all bs hit
                   print("You sunk the B ship")
           elif otherPlayer.gridShots.returnLocation(row, col) == "C":  # c ship hit
               self.cCount = self.cCount - 1
               if self.cCount == 0:  # all cs hit
                   print("You sunk the C ship")
           elif otherPlayer.gridShots.returnLocation(row, col) == "S":  # s ship hit
               self.sCount = self.sCount - 1
               if self.sCount == 0:  # all ss hit
                   print("You sunk the S ship")
           else:  # d ship hit
               self.dCount = self.dCount - 1
               if self.dCount == 0:  # all ds hit
                   print("You sunk the D ship")
           self.gridShots.changeSingleSpace(x, y, "0")
