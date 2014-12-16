#!/usr/bin/env python

# Place-in exam script.py for INFO 206 by  Brian Carlo, Aug. 30, 2014

import random

board = []

long_ship_boundary = 3
short_ship_boundary = 4

"""
The  ship boundary variables are based on the idea that to place 
a 3x1 or 2x1 ship on a board, you start with an anchor point and put the ship
either to the left of that point for a horizontal ship or downward for a vertical ship.

The boundaries indicate where the anchor point can be placed while ensuring
that the ship won't end up off the grid.

O O O O O
O O O X X X  <-- e.g, a 3x1 ship can't have an origin point of row 2, col 4:
O O O O O            ... it would stretch off the board.
O O O O O
O O O O O

Therefore, for a 3x1 horizontal ship, the "boundary" for picking an anchor column is 3.
i.e., if the ship is anchored within the first three columns, it can't stretch off the board.

"""

# create the board
for i in range(0,5):
    board.append(["O"]*5)

# iterates through the board and print its rows
def print_board(board):
    for row in board:
        print " ".join(row)

# sets a random anchor point within bounds, adds the rows and columns affected to ship list objects
def make_horizontal_ship(ship_col, ship_row, boundary):
    anchor_x = random.randint(1,boundary)
    anchor_y = random.randint(1,5)
    ship_col.append(anchor_x)
    ship_col.append(anchor_x+1)
    if boundary == 3:                    # only triggers for 3x1 ships
        ship_col.append(anchor_x+2)
    ship_row.append(anchor_y)

def make_vertical_ship(ship_col, ship_row, boundary):
    anchor_x = random.randint(1,5)
    anchor_y = random.randint(1,boundary)
    ship_row.append(anchor_y)
    ship_row.append(anchor_y+1)
    if boundary == 3:
        ship_row.append(anchor_y+2) 
    ship_col.append(anchor_y)

# simple iteration to see if ship1 and ship2 overlap
# basic logic is that if ship1_col in ship2col AND ship1_row in ship2_row, there's an overlap
def test_overlap(ship1, ship2):
    for num in ship2:
        if num in ship1:
            return True
        else:
            return False
  
# helper function for big_print below.         
def map_coordinates(rows, cols, board, char):
    if len(rows) > len(cols):
        for row in rows:
            board[row-1][cols[0]-1] = char
    else:
        for col in cols:
            board[rows[0]-1][col-1] = char

# prints out the location of the two ships
def big_print(ship1_row, ship1_col, ship2_row, ship2_col):

    board = []
    for i in range(0,5):
        board.append(["O"]*5)
    
    map_coordinates(ship1_row, ship1_col, board, "#")
    map_coordinates(ship2_row, ship2_col, board, "@")
    
    print_board(board)
        
        
        
# MAKE THE FIRST SHIP   

ship1_col = []
ship1_row = []

coin_1 = random.randint(0,1)    # arbitrarily picked True result to == horizontal

if coin_1:
    make_horizontal_ship(ship1_col, ship1_row, long_ship_boundary)
else:
    make_vertical_ship(ship1_col, ship1_row, long_ship_boundary)
    
    
# MAKE THE SECOND SHIP. 
# Probably should have made a Ship class here that automatically tests for overlap, etc.

ship2_col = []
ship2_row = []

coin_2 = random.randint(0,1)

if coin_2:
    make_horizontal_ship(ship2_col, ship2_row, short_ship_boundary)
else:
    make_vertical_ship(ship2_col, ship2_row, short_ship_boundary)
    
    
# TEST FOR OVERLAP. IF OVERLAP, REDO SHIP2 UNTIL NO OVERLAP

while test_overlap(ship1_col, ship2_col) and test_overlap(ship1_row, ship2_row):
    ship2_col = []
    ship2_row = []

    coin_2 = random.randint(0,1)

    if coin_2:
        make_horizontal_ship(ship2_col, ship2_row, short_ship_boundary)
    else:
        make_vertical_ship(ship2_col, ship2_row, short_ship_boundary)

        
# GAME LOGIC
# Mostly transposed from Codecademy, with some adjustments

print "Let's play Battleship!"
print_board(board)

turns = 24
while turns:                         # Chose a while loop here to account for the 17,17 guess

    guess_row = input("Guess Row: ")
    guess_col = input("Guess Col: ")
    
    # "Debug log" printout
    if guess_row == 17 and guess_col == 17:
        big_print(ship1_row, ship1_col, ship2_row, ship2_col)
        turns +=1
        print ""
    elif guess_row in ship1_row and guess_col in ship1_col:    # Could have combined these two statements
        print("You win!")                                      # ... but wanted to be clear what's going on.
        print ""
        big_print(ship1_row, ship1_col, ship2_row, ship2_col)
        break
    elif guess_row in ship2_row and guess_col in ship2_col:
        print("You win!")
        print""
        big_print(ship1_row, ship1_col, ship2_row, ship2_col)
        break
    else:
        if guess_row < 1 or guess_row > 5 or guess_col < 1 or guess_col > 5:
            print "Oops, that's not even in the ocean."
        elif board[guess_row - 1][guess_col - 1] == "X":
            print "You guessed that one already."
        else:
            print "You missed my battleship!"
            print ""
            board[guess_row - 1][guess_col - 1] = "X"
            print_board(board)
            print ""
            print "Turns taken:", 25 - turns
            print ""
            if turns == 0:
                print "Game Over."
                break
    turns -= 1


