class Grid:
    def __init__(self):
        self.grid = [["~","~","~","~","~","~","~","~","~","~"],
                          ["~","~","~","~","~","~","~","~","~","~"],
                          ["~","~","~","~","~","~","~","~","~","~"],
                          ["~","~","~","~","~","~","~","~","~","~"],
                          ["~","~","~","~","~","~","~","~","~","~"],
                          ["~","~","~","~","~","~","~","~","~","~"],
                          ["~","~","~","~","~","~","~","~","~","~"],
                          ["~","~","~","~","~","~","~","~","~","~"],
                          ["~","~","~","~","~","~","~","~","~","~"],
                          ["~","~","~","~","~","~","~","~","~","~"] ]
    # Change a single position
    def changeSingleSpace(self, row, col , value):
        self.grid[row][col] = value

    # Row = the row to change
    # Value = the string to put into the list
    # colStart = the start of the column to be changed
    # size = number of spaces in the column to change
    def changeRow(self , row , value , colStart , size ):
        for col in range( colStart , colStart + size ) :
            self.grid[row][col] = value

    # Col = the col to change
    # Value = the string to put into the list
    # rowStart = the start of the row to be changed
    # size = number of spaces in the row to change
    def changeCol(self , col , value , rowStart , size ):
        for row in range( rowStart , rowStart + size ) :
            self.grid[row][col] = value

    def returnLocation(self , row , col ):
        return self.grid[row][col]

    def printGrid(self):
        for row in self.grid :
            print( row )

    # This is a useful method to determine if the space is "~" or something else
    # Send it the grid you want to check, so ship or shot
    def isSpaceWater(self, row, col):
        if self.grid[row][col] == "~":
            return True
        else:
            return False

