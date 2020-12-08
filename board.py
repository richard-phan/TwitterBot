from enum import Enum
import requests
import os
import json

class Piece(Enum):
    EMPTY = '-'
    CROSS = 'X'
    CIRCLE = 'O'

class Board():
    def __init__(self):
        self.grid = []

        for x in range(9):
            self.grid.append(Piece.EMPTY)

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.grid[row][col] = Piece.EMPTY

    def print_board(self):
        i = 1
        for pos in range(9):
            piece = self.grid[pos]
            print(piece.value if piece != Piece.EMPTY else i, end='')

            if pos != 2 or pos != 5 or pos != 8:
                print(' ', end='')
            if pos == 2 or pos == 5 or pos == 8:
                print()

            i += 1

    def board_string(self):
        i = 1
        string = ''
        for pos in range(9):
            piece = self.grid[pos]
            string += piece.value if piece != Piece.EMPTY else str(i)

            if pos != 2 or pos != 5 or pos != 8:
                string += ' '
            if pos == 2 or pos == 5 or pos == 8:
                string += '\n'

            i += 1

        return string

    def board_raw_string(self):
        string = ''
        for piece in self.grid:
            string += piece.value
        
        return string
            
    def check_win(self, piece, position):
        stalemate = 0

        board = []
        row = []
        
        # creates 2D array
        for p in self.grid:
            if p != Piece.EMPTY:
                stalemate += 1

            row.append(p)

            if len(row) == 3:
                board.append(row)
                row = []

        # convert 1D index to 2D index
        col = int(position / 3)
        row = position % 3

        # check vertical win
        if board[0][row] == board[1][row] == board[2][row] and board[1][row] != Piece.EMPTY:
            return piece

        # check horizontal win
        if board[col][0] == board[col][1] == board [col][2] and board[col][1] != Piece.EMPTY:
            return piece

        # check diagonal win
        if col == row and board[0][0] == board[1][1] == board [2][2] and board[1][1] != Piece.EMPTY:
            return piece

        # check diagonal2 win
        if col + row == 2 and board[0][2] == board[1][1] == board [2][0] and board[1][1] != Piece.EMPTY:
            return piece

        if stalemate == 9:
            return '-1'

        return False

    # a turn on the board
    def turn(self, piece, pos):
        if pos > 8:
            return

        # places a piece on the board
        if self.grid[pos] == Piece.EMPTY:
            self.grid[pos] = piece

        self.print_board()

        # checks for a win
        win = self.check_win(piece, pos)
        if win:
            return Piece.CROSS

        # ai turn
        raw_string = self.board_raw_string()
        url = 'https://stujo-tic-tac-toe-stujo-v1.p.rapidapi.com/' + raw_string + '/O'
        headers = {
            'x-rapidapi-key': os.getenv('X_RAPIDAPI_KEY'),
            'x-rapidapi-host': os.getenv('X_RAPIDAPI_HOST')
        }

        response = requests.request("GET", url, headers=headers)
        print(response.text)

        # ai places a piece onthe board
        json_data = json.loads(response.text)
        print(json_data['recommendation'])
        self.grid[json_data['recommendation']] = Piece.CIRCLE
        
        self.print_board()

        # checks for a win
        win = self.check_win(Piece.CIRCLE, json_data['recommendation'])
        if win:
            return Piece.CIRCLE

        return None