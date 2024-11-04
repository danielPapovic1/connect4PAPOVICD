import numpy as np

import pygame

import sys
import math
import random

pygame.init()

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 2) * SQUARESIZE
size = (width, height)

BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 139)
BLUE = (0, 0, 255)
DARKER_BLUE = (0, 0, 150)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)
GREEN = (0, 200, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 255, 255)
GRAY = (100, 100, 100)

title_font = pygame.font.SysFont("Segoe UI", 60, bold=True)
tagline_font = pygame.font.SysFont("Segoe UI", 30)
button_font = pygame.font.SysFont("Segoe UI", 40)
myfont = pygame.font.SysFont("monospace", 75)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("CONNECT $ BY PAPOVIC")

icon = pygame.image.load("papovicsig.png")
pygame.display.set_icon(icon)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (board[r][c] == piece and board[r][c + 1] == piece and
                board[r][c + 2] == piece and board[r][c + 3] == piece):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and board[r + 1][c] == piece and
                board[r + 2][c] == piece and board[r + 3][c] == piece):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and board[r + 1][c + 1] == piece and
                board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == piece and board[r - 1][c + 1] == piece and
                board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece):
                return True

def draw_chip(screen, color, center, symbol="$", symbol_color=None, shine=True, highlight=False):
    num_segments = 20
    outline_color = color
    outline_radius = RADIUS + 5
    angle_step = 2 * math.pi / num_segments
    outline_points = []
    for i in range(num_segments):
        angle = i * angle_step
        x = center[0] + outline_radius * math.cos(angle)
        y = center[1] + outline_radius * math.sin(angle)
        outline_points.append((x, y))
    pygame.draw.polygon(screen, outline_color, outline_points)
    rim_color = tuple(min(c + 50, 255) for c in color)
    pygame.draw.circle(screen, rim_color, center, RADIUS)
    pygame.draw.circle(screen, color, center, RADIUS - 6)
    if highlight:
        pygame.draw.circle(screen, color, center, RADIUS + 3, 3)
    if symbol_color is None:
        symbol_color = WHITE
    if symbol is not None:
        symbol_font = pygame.font.SysFont("Arial", 35, bold=True)
        symbol_text = symbol_font.render(symbol, True, symbol_color)
        symbol_rect = symbol_text.get_rect(center=center)
        screen.blit(symbol_text, symbol_rect)
    if shine:
        shine_radius = RADIUS - 15
        shine_surface = pygame.Surface((shine_radius * 2, shine_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(shine_surface, (255, 255, 255, 80), (shine_radius, shine_radius), shine_radius)
        screen.blit(shine_surface, (center[0] - shine_radius, center[1] - shine_radius))

def draw_board(board):
    screen.fill(BLACK)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            x = c * SQUARESIZE
            y = (r + 2) * SQUARESIZE
            slot_rect = pygame.Rect(x, y, SQUARESIZE, SQUARESIZE)
            pygame.draw.rect(screen, BLUE, slot_rect)
            center = (int(x + SQUARESIZE / 2), int(y + SQUARESIZE / 2))
            pygame.draw.circle(screen, (30, 30, 30), (center[0] + 4, center[1] + 4), RADIUS - 5)
            pygame.draw.circle(screen, BLACK, center, RADIUS - 5)
            pygame.draw.circle(screen, (50, 50, 50), center, RADIUS - 5, 2)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                center = (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2))
                draw_chip(screen, RED, center, symbol="$", shine=False)
            elif board[r][c] == 2:
                center = (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2))
                draw_chip(screen, YELLOW, center, symbol="$", shine=False)
    pygame.display.update()

def animate_drop(col, row, piece):
    x = int(col * SQUARESIZE + SQUARESIZE / 2)
    y_start = int(SQUARESIZE + SQUARESIZE / 2)
    y_end = int((row + 2) * SQUARESIZE + SQUARESIZE / 2)
    color = RED if piece == 1 else YELLOW
    y = y_start
    drop_speed = 20
    while y < y_end:
        pygame.draw.rect(screen, BLACK, (0, SQUARESIZE, width, height - SQUARESIZE))
        draw_board(board)
        draw_chip(screen, color, (x, y), symbol="$", shine=True)
        y += drop_speed
        if y > y_end:
            y = y_end
        pygame.display.update()
        pygame.time.delay(30)
    bounce_distance = 10
    for i in range(3):
        y -= bounce_distance
        pygame.draw.rect(screen, BLACK, (0, SQUARESIZE, width, height - SQUARESIZE))
        draw_board(board)
        draw_chip(screen, color, (x, y), symbol="$", shine=True)
        pygame.display.update()
        pygame.time.delay(50)
        y += bounce_distance
        pygame.draw.rect(screen, BLACK, (0, SQUARESIZE, width, height - SQUARESIZE))
        draw_board(board)
        draw_chip(screen, color, (x, y), symbol="$", shine=True)
        pygame.display.update()
        pygame.time.delay(50)
        bounce_distance = int(bounce_distance / 2)

def display_win_message(winner):
    clock = pygame.time.Clock()
    message = "RED WINS!" if winner == 1 else "YELLOW WINS!"
    color = RED if winner == 1 else YELLOW
    font_size = 75
    max_font_size = 90
    min_font_size = 75
    font_growth = 0.5
    growing = True
    show_message = True
    flash_timer = 0
    flash_interval = 500
    start_ticks = pygame.time.get_ticks()
    duration = 5000
    running = True
    while running:
        screen.fill(BLACK)
        draw_board(board)
        if growing:
            font_size += font_growth
            if font_size >= max_font_size:
                growing = False
        else:
            font_size -= font_growth
            if font_size <= min_font_size:
                growing = True
        flash_timer += clock.get_time()
        if flash_timer >= flash_interval:
            flash_timer = 0
            show_message = not show_message
        if show_message:
            win_font = pygame.font.SysFont("Arial Black", int(font_size), bold=True)
            win_text = win_font.render(message, True, color)
            win_rect = win_text.get_rect(center=(width // 2, height // 2))
            screen.blit(win_text, win_rect)
        pygame.display.update()
        clock.tick(60)
        elapsed_time = pygame.time.get_ticks() - start_ticks
        if elapsed_time >= duration:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    play_again = display_end_options()
    if play_again:
        reset_game()
    else:
        pygame.quit()
        sys.exit()

def display_end_options():
    clock = pygame.time.Clock()
    running = True
    button_width = 200
    button_height = 60
    button_spacing = 20
    play_again_rect = pygame.Rect((width // 2 - button_width - button_spacing // 2, 50), (button_width, button_height))
    exit_rect = pygame.Rect((width // 2 + button_spacing // 2, 50), (button_width, button_height))
    while running:
        screen.fill(BLACK)
        draw_board(board)
        pygame.draw.rect(screen, YELLOW, play_again_rect)
        pygame.draw.rect(screen, RED, exit_rect)
        button_font = pygame.font.SysFont("Arial", 30, bold=True)
        play_again_text = button_font.render("Play Again", True, WHITE)
        exit_text = button_font.render("Exit", True, WHITE)
        play_again_text_rect = play_again_text.get_rect(center=play_again_rect.center)
        exit_text_rect = exit_text.get_rect(center=exit_rect.center)
        screen.blit(play_again_text, play_again_text_rect)
        screen.blit(exit_text, exit_text_rect)
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_again_rect.collidepoint(mouse_pos):
                    return True
                elif exit_rect.collidepoint(mouse_pos):
                    return False
    return False

def reset_game():
    global board, game_over, turn
    board = create_board()
    game_over = False
    turn = 0
    draw_board(board)

def show_start_screen():
    clock = pygame.time.Clock()
    running = True
    button_color = RED
    button_hover_color = (255, 100, 100)
    button_radius = 80
    button_position = (width // 2, height // 2 + 50)
    button_rect = pygame.Rect(0, 0, button_radius * 2, button_radius * 2)
    button_rect.center = button_position
    chips = []
    chip_spawn_timer = 0
    while running:
        screen.fill(BLACK)
        board_top = 150
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                x = col * SQUARESIZE
                y = row * SQUARESIZE + board_top
                slot_rect = pygame.Rect(x, y, SQUARESIZE, SQUARESIZE)
                pygame.draw.rect(screen, BLUE, slot_rect)
                pygame.draw.circle(screen, BLACK, slot_rect.center, RADIUS)
                pygame.draw.rect(screen, DARKER_BLUE, slot_rect, 2)
        chip_spawn_timer += 1
        if chip_spawn_timer >= 30:
            chip_color = RED if random.random() > 0.5 else YELLOW
            chips.append({'pos': [random.randint(50, width - 50), -SQUARESIZE], 'color': chip_color})
            chip_spawn_timer = 0
        for chip in chips[:]:
            chip['pos'][1] += 3
            if chip['pos'][1] > height:
                chips.remove(chip)
            else:
                pygame.draw.circle(screen, chip['color'], (int(chip['pos'][0]), int(chip['pos'][1])), RADIUS)
        title_text = "CONNECT $ BY PAPOVIC"
        title_parts = ["CONNECT ", "$", " BY PAPOVIC"]
        title_colors = [RED, YELLOW, RED]
        title_surfaces = [title_font.render(part, True, color) for part, color in zip(title_parts, title_colors)]
        total_width = sum([s.get_width() for s in title_surfaces])
        x_position = (width - total_width) // 2
        y_position = 30
        shadow_offset = 2
        x_shadow = x_position + shadow_offset
        y_shadow = y_position + shadow_offset
        for surface in title_surfaces:
            shadow_surface = surface.copy()
            shadow_surface.fill(BLACK, special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(shadow_surface, (x_shadow, y_shadow))
            screen.blit(surface, (x_position, y_position))
            x_position += surface.get_width()
            x_shadow += surface.get_width()
        tagline_font_bold = pygame.font.SysFont("Segoe UI", 30, bold=True)
        tagline_surface = tagline_font_bold.render("CAN YOU CONNECT 4?", True, WHITE)
        tagline_rect = tagline_surface.get_rect(center=(width // 2, 150))
        tagline_bg_surface = pygame.Surface((tagline_rect.width + 30, tagline_rect.height + 15), pygame.SRCALPHA)
        tagline_bg_surface.fill((0, 0, 0, 150))
        screen.blit(tagline_bg_surface, (tagline_rect.x - 15, tagline_rect.y - 7))
        screen.blit(tagline_surface, tagline_rect)
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_pos)
        current_button_color = button_hover_color if is_hovered else button_color
        pygame.draw.circle(screen, current_button_color, button_position, button_radius)
        if is_hovered:
            pygame.draw.circle(screen, PURPLE, button_position, button_radius + 5, 3)
        play_text_bold = button_font.render("Play", True, PURPLE)
        text_rect = play_text_bold.get_rect(center=button_position)
        screen.blit(play_text_bold, text_rect)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovered:
                    for scale in range(button_radius, button_radius - 15, -1):
                        pygame.draw.circle(screen, current_button_color, button_position, scale)
                        pygame.display.flip()
                        clock.tick(60)
                    running = False

show_start_screen()

board = create_board()
game_over = False
turn = 0

draw_board(board)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, SQUARESIZE, width, SQUARESIZE))
            posx = event.pos[0]
            center = (posx, SQUARESIZE + int(SQUARESIZE / 2))
            if turn == 0:
                draw_chip(screen, RED, center, symbol="$", symbol_color=WHITE, shine=True, highlight=True)
            else:
                draw_chip(screen, YELLOW, center, symbol="$", symbol_color=WHITE, shine=True, highlight=True)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pygame.draw.rect(screen, BLACK, (0, SQUARESIZE, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                piece = turn + 1
                animate_drop(col, row, piece)
                drop_piece(board, row, col, piece)
                if winning_move(board, piece):
                    game_over = True
                    winner = piece
                draw_board(board)
                turn = (turn + 1) % 2
                if game_over:
                    display_win_message(winner)
                    game_over = False