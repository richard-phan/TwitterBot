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
            

    def turn(self, piece, pos):
        if self.grid[pos] == Piece.EMPTY:
            self.grid[pos] = piece

        self.print_board()

        raw_string = self.board_raw_string()
        url = 'https://stujo-tic-tac-toe-stujo-v1.p.rapidapi.com/' + raw_string + '/O'
        headers = {
            'x-rapidapi-key': os.getenv('X_RAPIDAPI_KEY'),
            'x-rapidapi-host': os.getenv('X_RAPIDAPI_HOST')
        }

        response = requests.request("GET", url, headers=headers)
        print(response.text)

        json_data = json.loads(response.text)
        print(json_data['recommendation'])
        self.grid[json_data['recommendation']] = Piece.CIRCLE

        self.print_board()
