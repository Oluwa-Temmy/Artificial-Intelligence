"""
This is a connect 4 game
Uses the minimax algorithm
to determine the best move for the bot.


--- Credit ---
Keith Galli 
How does a Board Game AI Work? 
(Connect 4, Othello, Chess, Checkers) - 
Minimax Algorithm Explained
Series

--------------

Name: Osayi Odiase
Course: CPSC 425 01
Assignment: Mod4A1 Minimax Connect 4
Date: 4-7-2025

"""
import numpy as np
import pygame
import sys
import math
import random

# Size of the board
ROW_COUNT = 6
COLUMN_COUNT = 7

# RGB colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player and AI turns
PLAYER = 0
AI = 1

# Player pieces
PLAYER_PIECE = 1
AI_PIECE = 2

# Window length for scoring
WINDOW_LENGTH = 4

# Empty space on the board
EMPTY = 0

turn = random.randint(PLAYER, AI)


def create_board():
    """
    Create the board matric using numpy
    """
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    """
    Drop a piece on the board
    by getting the board row and column
    and setting it to the piece value
    """
    board[row][col] = piece


def get_next_open_row(board, col):
    """
    Get the next open row in the column 
    by diggin down until we find a 0
    """
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r


def is_valid_location(board, col):
    """
    Check that the column is empty
    by checking the last row in the column
    """
    return board[ROW_COUNT-1][col] == EMPTY


def print_board(board):
    """
    FLip the board over to make it look
    like a board
    """
    print(np.flip(board, 0))
    

def winning_move(board, piece):
    # check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positive slop diagnols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negative slop diagnols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def eval_window(window, piece):
    """
    Return a weight to the window based on the number of pieces in a row
    and the number of empty spaces in the window

    Example:
    [1, 1, 0, 0] = 2
    [1, 1, 1, 0] = 4   (Good case)
    [1, 1, 1, 1] = 100 (This is the best case)
    [0, 0, 0, 0] = 0
    [1, 1, 1, 2] = -4 (Bad case)
    [2, 2, 2, 2] = -100 (Worst case)
    """
    score = 0
    inverse_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        inverse_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(inverse_piece) == 3 and window.count(EMPTY) == 1:
        score -= -4

    return score

def score_pos(board, piece):
    """
    Score the position
    based on the number of pieces in a row
    
    The array signifies the row count and any 
    number of columns that are in a row.

    check eval_window for more details

    """
    score = 0

    center_array = [int(i) for i in list(board[:,COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += eval_window(window, piece)

    # Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += score + eval_window(window, piece)

    # Diagonal positive slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += eval_window(window, piece)

    # Diagonal negative slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += eval_window(window, piece)

    return score

def is_terminal_node(board):
    """
    Check if the game is over (win or draw)
    by checking if there are any valid locations left
    """
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maximizing_player, alpha, beta):
    """
    Minimax algorithm to determine the best move for the AI
    When depth is 0 (the AI has no more moves to make)

    maximizing_player means the AI is trying to maximize its score,
    meaning the player is trying to lose

    minimizing_player means the AI is trying to minimize its score, 
    meaning the player is trying to win

    beta is the best score that the minimizing player can guarantee
    alpha is the best score that the maximizing player can guarantee
    """
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    # returns the heuristic score of the position
    if depth == 0 or is_terminal:
        if is_terminal:
            # If AI wins, return a high score
            if winning_move(board, AI_PIECE):
                return (None, 1000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000000000)
            # Game is over
            else:
                return (None, 0)
        else:
            # Depth is 0
            return (None, score_pos(board, AI_PIECE))
        
    # minimizing player (AI)
    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False, alpha, beta)[1]
            if new_score > value:
                value = new_score
                best_col = col

            # Stop searching if the value is greater than the beta value
            # (the best score the minimizing player can guarantee)
            # This is called pruning
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, new_score 

    # maximizing player (Player)
    else:
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, True, alpha, beta)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
            
        return best_col, new_score
            
 
def get_valid_locations(board):
    """
    Get all the valid locations on the board
    by checking if the last row in the column is empty

    Returns a list of valid columns
    """
    valid_location = []
    for col in range(COLUMN_COUNT):
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                valid_location.append(col)
    return valid_location

def pick_best_move(board, piece):
    """
    Pick the best move for the AI 
    based on the score of the position
    """
    valid_locations = get_valid_locations(board)
    best_score = 10000
    best_col = random.choice(valid_locations)

    
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_pos(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col
  
# Initialize size of the board
# and the size of the pieces
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2-5)

# Set the size of the board
# and the size of the pieces
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

def draw_board(board):
    """
    Draw the board using pygame
    """
    # Draw grid background
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    # Draw player pieces (Red and Yellow)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    # Update display
    pygame.display.update()


board = create_board()

# Var for game over
game_over = False

"""
Create the pygame UI
and set all custom themes
"""
pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
pygame.display.set_caption("Connect 4")


while not game_over:
    
    for event in pygame.event.get():
        # in the event the user exits
        if event.type == pygame.QUIT:
            sys.exit()

        # in the event the user moves the mouse
        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == 0:
                if posx < width:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                if posx < width:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        
        pygame.display.update()

        # in the event the user clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # Ask player 1 input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    
                    turn += 1
                    turn = turn % 2
                    draw_board(board)
            
    # Ask player 2 for input   
    if turn == AI and not game_over:
        
        # search for the best move using minimax
        col, minimax_score = minimax(board, 4, True, alpha=-math.inf, beta=math.inf)
        
        # if valid place the piece
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            # winner winner, chicken dinner
            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            #redraw the board after move
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(2000)
        break