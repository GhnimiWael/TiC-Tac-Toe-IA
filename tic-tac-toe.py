#!/usr/bin/env python3
from math import inf as infinity
from random import choice
from os import system
import platform
import time


# Define human and computer choices
HumanChoice = -1
ComputerChoice = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

# Evaluate the state of the board
def evaluate(state):
    if wins(state, ComputerChoice):
        score = +1
    elif wins(state, HumanChoice):
        score = -1
    else:
        score = 0

    return score

# Check the wining possibility
def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def GameOver(state):
    return wins(state, HumanChoice) or wins(state, ComputerChoice)


def EmptyCells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells


def valid_move(x, y):
    if [x, y] in EmptyCells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    if player == ComputerChoice:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or GameOver(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in EmptyCells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == ComputerChoice:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

# clean the console
def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

# print the board 
def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    depth = len(EmptyCells(board))
    if depth == 0 or GameOver(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, ComputerChoice)
        x, y = move[0], move[1]

    set_move(x, y, ComputerChoice)
    time.sleep(1)


def HumanChoice_turn(c_choice, h_choice):
    depth = len(EmptyCells(board))
    if depth == 0 or GameOver(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Your turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            print("For help using the following numbers places:")
            print("1 | 2 | 3")
            print("4 | 5 | 6")
            print("7 | 8 | 9")
            move = int(input('Use (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HumanChoice)

            if not can_move:
                print('Bad move\n')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice\n')

# The main function
def main():
    clean()
    print("""
                                                 
    )              )                )            
 ( /( (         ( /(    )        ( /(        (   
 )\()))\   (    )\())( /(   (    )\()) (    ))\  
(_))/((_)  )\  (_))/ )(_))  )\  (_))/  )\  /((_) 
| |_  (_) ((_) | |_ ((_)_  ((_) | |_  ((_)(_))   
|  _| | |/ _|  |  _|/ _` |/ _|  |  _|/ _ \/ -_)  
 \__| |_|\__|   \__|\__,_|\__|   \__|\___/\___|
 
    - Developed with <3 by @w43L ^^
    - Ppr: Comparative Study of Game Tree Searching Methods
                                                 
    """)
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if HumanChoice is the first

    # HumanChoice chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting ComputerChoiceuter's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # HumanChoice may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    while len(EmptyCells(board)) > 0 and not GameOver(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        HumanChoice_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Game over message
    if wins(board, HumanChoice):
        clean()
        print(f'Your turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, ComputerChoice):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW, No winner! :) ')

    exit()


if __name__ == '__main__':
    main()
    