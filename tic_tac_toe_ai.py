import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (242, 85, 96)
CROSS_COLOR = (28, 170, 156)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe AI')
screen.fill(WHITE)

# Board
board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Functions


def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                          int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


def check_win(player):
    # Vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    # Horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # Ascending diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True

    # Descending diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True

    return False


def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH)


def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), LINE_WIDTH)


def draw_asc_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), LINE_WIDTH)


def draw_desc_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), LINE_WIDTH)


def restart():
    screen.fill(WHITE)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


def ai_move():
    empty_squares = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == 0]
    if len(empty_squares) > 0:
        row, col = random.choice(empty_squares)
        mark_square(row, col, 2)


# Main loop
draw_lines()
player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                player = 2  # Switch to AI's turn

        # AI move
        if player == 2 and not game_over:
            ai_move()
            if check_win(2):
                game_over = True
            player = 1  # Switch back to human player

        if game_over:
            time.sleep(2)
            restart()
            player = 1
            game_over = False

    draw_figures()
    pygame.display.update()
