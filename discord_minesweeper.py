import random
import json
from flask import Flask

emoji_digits = [":zero:", ":one:", ":two:", ":three:",
                ":four:", ":five:", ":six:",
                ":seven:", ":eight:", ":nine:"]

mine_emoji = ":bomb:"

mine = -1

def generate_maze(size, num_mines):
    bomb_pos = [(random.randint(0, size), random.randint(0, size))
            for _ in range(num_mines)]

    # Initialize 2D array to all 0's
    board = [ [0 for _ in range(size)] for _ in range(size)]

    # Set "bomb" squares to -1
    for i in range(size):
        for j in range(size):
            if (i, j) in bomb_pos:
                board[i][j] = mine

    # Count the bomb squares adjacent to each square
    for i in range(size):
        for j in range(size):
            # Skip the mines themselves
            if board[i][j] == mine:
                continue

            # Check adjacent squares
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if j == 0 and l == -1:  # manual checking because the errors are'nt getting thrown i guess
                        continue
                    if i == 0 and k == -1:
                        continue
                    try:
                        if board[i + k][j + l] == mine:
                            board[i][j] += 1
                    except IndexError:
                        continue

    for i in range(size):
        print(board[i])

    return board


def board_to_string(board):
    string_board = ""
    for row in board:
        for square in row:
            if square == mine:
                string_board += mine_emoji
            else:
                string_board += emoji_digits[square]
        string_board += "\n"

    return string_board


def mark_spoiler(string):
    return "||%s||" % string

app = Flask(__name__)

@app.route('/minesweeper', methods=['GET'])
def default_board():
    return json.dumps(board_to_string(generate_maze(5, 3)))


@app.route('/minesweeper/<size>', methods=['GET'])
def custom_size(size):
    size = int(size)
    return json.dumps(board_to_string(generate_maze(size, 3)))


if __name__ == '__main__':
    app.run(debug=True)
