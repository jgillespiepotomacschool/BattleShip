import random
from Shot import Shot
from Player import Player
class ComputerPlayer(Player):
   def __init__(self):
       self.ships = {
           "A" : "Aircraft Carrier" ,
           "B" : "BattleShip" ,
           "C" : "Cruiser" ,
           "S" : "Submarine" ,
           "D" : "Destroyer"
       }
       Player.__init__(self)
       self.shotList = []
       self.guessList = []


   def isInGuessList(self,r,c):#checks if location is already in the guess list
       for x in self.guessList:
           if x.getRow() == r and x.getCol() == c:
               return True
       return False

   def addToGuessList(self,r,c,s):#makes sure a guess is legal before adding it to the guess list returns tru if the guess is a hit
       if -1 <  r < 10 and -1 <  c < 10 and self.gridShots.returnLocation(r, c) == "~" and not self.isInGuessList(r, c):
           if s:
               self.guessList.insert(0,Shot("g", r, c))
           else:
               self.guessList.append(Shot("g", r, c))





   def takeTurn(self, otherPlayer):
       for row in range(10):
           hitCount = 0
           for col in range(10):
               if self.gridShots.returnLocation(row, col) == "h" :
                   hitCount += 1
               if self.gridShots.returnLocation(row, col) != "h" or col == 9:
                   if hitCount >= 2:
                       self.addToGuessList(row, col, True)
                       self.addToGuessList(row, col-(hitCount+1), True)
                       #for x in range(hitCount):
                           #self.addToGuessList(row + 1, col - x, False)
                       #for x in range(hitCount):
                           #self.addToGuessList(row - 1, col - x, False)
                   hitCount = 0
       for col in range(10):
           hitCount = 0
           for row in range(10):
               if self.gridShots.returnLocation(row,col) == "h":
                   hitCount += 1
               if self.gridShots.returnLocation(row, col) != "h" or row == 9:
                   if hitCount>=2:
                       self.addToGuessList(row ,col,True)
                       self.addToGuessList(row - (hitCount+1), col,True)
                       #for x in range(hitCount):
                           #self.addToGuessList(row - x, col + 1, False)
                       #for x in range(hitCount):
                           #self.addToGuessList(row - x, col - 1, False)
                       hitCount = 0
       if not bool(self.guessList):
           for row in range(10):
               for col in range(10):
                   if self.loneHit(row,col) :
                       if row < 9:
                           if self.gridShots.returnLocation(row + 1, col) == "~":
                               return self.Turn(otherPlayer,row+1,col)
                       if row > 0:
                           if self.gridShots.returnLocation(row - 1, col) == "~":
                               return self.Turn(otherPlayer,row-1,col)
                       if col < 9:
                           if self.gridShots.returnLocation(row, col + 1) == "~":
                               return self.Turn(otherPlayer,row,col+1)
                       if col > 0:
                           if self.gridShots.returnLocation(row, col - 1) == "~":
                               return self.Turn(otherPlayer,row,col-1)
       if not bool(self.guessList):
           return self.randTurn(otherPlayer)
       else:
           return self.Turn(otherPlayer,self.guessList[0].getRow(),self.guessList[0].getCol())


   def loneHit(self,row,col):
       if self.gridShots.returnLocation(row, col) == "h" :
           if row < 9:
               if self.gridShots.returnLocation(row + 1, col) == "h":
                   return False
           if row > 0:
               if self.gridShots.returnLocation(row - 1, col) == "h":
                   return False
           if col < 9 :
               if self.gridShots.returnLocation(row, col+1) == "h":
                   return False
           if col > 0:
               if self.gridShots.returnLocation(row, col-1) == "h":
                   return False
           return True
       else:
           return False






   def Turn(self, otherPlayer, r, c):
       if bool(self.guessList):
           self.guessList.pop(0)
       if otherPlayer.gridShips.returnLocation(r,c) != "~":#if guess is not water
           print("hit")
           self.gridShots.changeSingleSpace(r,c,"h")
           shipHit = otherPlayer.gridShips.returnLocation(r, c)
           otherPlayer.gridShips.changeSingleSpace(r, c, "h")
           for row in range(10):#traverses grid
               for col in range(10):#traverses grid
                   if otherPlayer.gridShips.returnLocation(row,col) == shipHit:#if any spaces a left of the ship that was hit ends turn
                       self.shotList.append(Shot(shipHit, r, c))
                       return otherPlayer.stillHasShips()
           print("you sunk the opponents " + self.ships[shipHit])
           self.updateShotList(otherPlayer,shipHit)
       else:#miss
           print("miss")
           self.gridShots.changeSingleSpace(r, c, "m")
           otherPlayer.gridShips.changeSingleSpace(r, c, "m" )
           self.shotList.append(Shot("m", r, c))
       return otherPlayer.stillHasShips()
   #takes the players turn
   # otherPLayer param the opponent who's ship grid will be checked and updated
   def randTurn(self,otherPlayer):
       guess = random.randrange(0,100)
       while (not self.gridShots.isSpaceWater(guess//10,guess%10)):#makes sure guess is not one previously guessed
           guess = random.randrange(0, 100)
       return self.Turn(otherPlayer, guess//10, guess%10)
   #places a ship in the Computer Players shipGrid
   #ship param a letter representing what ship is being placed
   #size param the number of spaces that the ship takes up
   def placeShip(self, ship, size):
       if(random.randrange(0,2)==1):#picks horizontal or vertical
           startColumn = random.randrange(0,11-size)
           startRow = random.randrange(0,10)
           for a in range(size):#checks every space that the ship will take up
               if(not self.gridShips.isSpaceWater(startRow,startColumn+a)):#checks for enough open spaces
                   return self.placeShip(ship,size)
           for b in range(size):#places ship
               self.gridShips.changeSingleSpace(startRow, startColumn+b, ship)
       else:#Vertical
           startColumn = random.randrange(0, 10)
           startRow = random.randrange(0, 11 - size)
           for a in range(size):#checks every space that the ship will take up
               if (not self.gridShips.isSpaceWater(startRow+a, startColumn)):#checks for enough open spaces
                   return self.placeShip(ship, size)
           for b in range(size):#places ship
               self.gridShips.changeSingleSpace(startRow + b, startColumn, ship)

   # this method will determine if the Player's ship grid still
   # has ships or not
   # If they have no ships left, the other player wins
   # This method returns true if they still have ships
   # This method returns false if they don't have ships
   def stillHasShips(self):
       for row in range(10):#traverses grid
           for col in range(10):#traverses grid
               if self.gridShips.returnLocation(row,col) != "~" and self.gridShips.returnLocation(row,col) != "h" and self.gridShips.returnLocation(row,col) != "m":#if a ship is found returns true
                   return True
       return False

   def updateShotList(self,otherPlayer,ship):
       for row in range(10):
           for col in range(10):
               if otherPlayer.gridShips.returnLocation(row,col) == ship:
                   leng = len(self.shotList)
                   for x in self.shotList:
                       if row == x.getRow() and col == x.getCol():
                           self.shotList.remove(x)


       for y in range(len(self.shotList)):
           if self.shotList[y].getResult() == "h":
               return
       self.shotList = []
       self.guessList = []



class Shot():
   def __init__(self,res,ro,co):
       self.result = res
       self.row = ro
       self.col = co

   def getResult(self):
       return self.result

   def getRow(self):
       return self.row

   def getCol(self):
       return self.col

