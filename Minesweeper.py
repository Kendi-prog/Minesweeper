import random  #importing the random module, which is used to generate random numbers,
import re      # and the re module, which is used for regular expression operations.

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size          #The dimension size of the board.
        self.num_bombs = num_bombs        #The number of bombs on the board.
        self.board = self.make_new_board() #generate a new board 
        self.assign_values_to_board()  # assign values to each cell.
        self.dug = set()               #A set containing the coordinates of cells that have been dug.


#The make_new_board method randomly places bombs on the board by selecting random
# coordinates and marking the corresponding cells as bombs (*).
#It continues this process until the desired number of bombs is planted.
#The remaining cells are initially set to empty spaces (' ').
    def make_new_board(self):
        board = [[' ' for _ in range(self.dim_size)] for _ in range(self.dim_size)]  ##A 2D list representing the current state of the board.

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                continue
            board[row][col] = '*'  
            bombs_planted += 1
        return board

#The assign_values_to_board method iterates over each cell on the board and 
#assigns a value to it based on the number of neighboring bombs. 
#If a cell is already a bomb, it skips the assignment. 
#Otherwise, it calls the get_num_neighbouring_bombs method to count the number of neighboring bombs 
#and assigns the value as a string to the cell.
    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = str(self.get_num_neighbouring_bombs(r, c))

#The get_num_neighbouring_bombs method calculates the number of neighboring bombs for a given cell
# by iterating over its neighboring cells and counting the bombs. 
#It excludes the current cell from the count.
    def get_num_neighbouring_bombs(self, row, col):
        num_neighbouring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs

#The dig method is used to dig a cell on the board. 
#It adds the coordinates of the cell to the dug set. 
#If the cell contains a bomb, it returns False to indicate that the game is over. 
#If the cell contains a number greater than '0', indicating the number of neighboring bombs, 
#it returns True. Otherwise, it recursively calls itself on the neighboring cells, 
#excluding the already dug cells. It returns True if the dig operation was successful.
    def dig(self, row, col):
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > '0':
            return True

        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

#The __str__ method overrides the string representation of the Board class.
# It generates a string representation of the board by iterating over each cell and
# displaying either the cell's value if it has been dug or an empty space if it hasn't.
    def __str__(self):
        board_str = '\n' + '-' * (4 * self.dim_size - 1) + '\n'
        for row in range(self.dim_size):
            board_str += '| ' + ' | '.join([self.get_cell_display(row, col) for col in range(self.dim_size)]) + ' |\n'
            if row < self.dim_size - 1:
                board_str += '|' + '---|' * (self.dim_size - 1) + '---|\n'
        board_str += '-' * (4 * self.dim_size - 1)
        return board_str

#The get_cell_display method is a helper method used by __str__ to determine the display value of a cell.
# If the cell has been dug, it returns the cell's value as a string. Otherwise, it returns an empty space.
    def get_cell_display(self, row, col):
        if (row, col) in self.dug:
            return str(self.board[row][col])
        else:
            return ' '

def play(dim_size=10, num_bombs=10):
    #Inside the play function, a new instance of the Board class is created with the specified dimension size and number of bombs.
    board = Board(dim_size, num_bombs)
    #The game loop continues until all safe cells have been dug or a bomb is hit. 
    #It displays the current state of the board and prompts the user to input the row and column to dig.
    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',\\s*', input('Where would you want to dig? Input as row, col: ')) #The user's input is split using a regular expression to extract the row and column values.
        row, col = int(user_input[0]), int(user_input[1])
        #If the input location is invalid (i.e., outside the board boundaries), an error message is displayed, and the loop continues.
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size: 
            print('Invalid location. Dig again')
            continue

        safe = board.dig(row, col)
        if not safe:
            break
    if safe:
        print('CONGRATULATIONS!!! YOU ARE VICTORIOUS.')
    else:
        print('SORRY 😪 GAME OVER!!!')
        # reveal all the board
        board.dug = {(r, c) for r in range(board.dim_size) for c in range(board.dim_size)}
        print(board)

if __name__ == '__main__':
    play()
