import numpy as np
import math
import pygame
import sys
import random

rows = 6
columns = 7

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE =(255, 255, 255)

PLAYER = 0
AI = 1
WINDOW_SIZE = 4


def create_board():
    board = np.zeros((rows, columns))
    return board


def valid_location(board, col):
    return board[rows - 1][col] == 0


def drop(board, row, col, piece):
    board[row][col] = piece


def next_row(board, col):
    for r in range(rows):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def get_valid_locations(board):
    valid_locations = []
    for col in range(columns):
        if valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def winner(board, piece):
    for c in range(columns - 3):
        for r in range(rows):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    for c in range(columns):
        for r in range(rows - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    for c in range(columns - 3):
        for r in range(rows - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    for c in range(columns - 3):
        for r in range(3, rows):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def evaluate_score(window, piece):
    score = 0
    opponent = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent = AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 20
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5
    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score += -10
    return score


def scoring_val(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, columns // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(rows):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(columns - 3):
            window = row_array[c:c + WINDOW_SIZE]
            score += evaluate_score(window, piece)
    for c in range(columns):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rows - 3):
            window = col_array[r:r + WINDOW_SIZE]
            score += evaluate_score(window, piece)
    for r in range(rows - 3):
        for c in range(columns - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_SIZE)]
            score += evaluate_score(window, piece)
    for r in range(rows - 3):
        for c in range(columns - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_SIZE)]
            score += evaluate_score(window, piece)
    return score


def terminal_node(board):
    return winner(board, PLAYER_PIECE) or winner(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def alphabeta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winner(board, AI_PIECE):
                return (None, 100000000000000)
            elif winner(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, scoring_val(board, AI_PIECE))
    if maximizingPlayer:
        val = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_row(board, col)
            bcopy = board.copy()
            drop(bcopy, row, col, AI_PIECE)
            new_score = alphabeta(bcopy, depth - 1, alpha, beta, False)[1]
            if new_score > val:
                val = new_score
                column = col
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return column, val
    else:
        val = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_row(board, col)
            bcopy = board.copy()
            drop(bcopy, row, col, PLAYER_PIECE)
            new_score = alphabeta(bcopy, depth - 1, alpha, beta, True)[1]
            if new_score < val:
                val = new_score
                column = col
            beta = min(beta, val)
            if alpha >= beta:
                break
        return column, val


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = next_row(board, col)
        temporary_board = board.copy()
        drop(temporary_board, row, col, piece)
        score = scoring_val(temporary_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


SQUARESIZE = 100


def draw_board(board):
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(columns):
        for r in range(rows):
            if board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False

pygame.init()

width = columns * SQUARESIZE
height = (rows + 1) * SQUARESIZE
size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font_style = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER and not game_over:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if valid_location(board, col):
                    row = next_row(board, col)
                    drop(board, row, col, PLAYER_PIECE)

                    if winner(board, PLAYER_PIECE):
                        label = font_style.render("YOU WON!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    if turn == AI and not game_over:
        col, alphabeta_score = alphabeta(board, 5, -math.inf, math.inf, True)
        if valid_location(board, col):
            row = next_row(board, col)
            drop(board, row, col, AI_PIECE)
            if winner(board, AI_PIECE):
                label = font_style.render("AI won!!", 1, RED)
                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(6000)
