import pygame
from constant import (tetromino_size, color_white, color_red)

# 繪製網格    
def draw_grid(screen, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                color = grid[y][x]
                pygame.draw.rect(screen, color,
                               [x * tetromino_size, y * tetromino_size,
                                tetromino_size - 1, tetromino_size - 1])
    
# 繪製正在落下的方塊                
def draw_current_piece(screen, current_piece):
    shape = current_piece.shape
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x]:
                pygame.draw.rect(screen, current_piece.color,
                               [(current_piece.x + x) * tetromino_size,
                                (current_piece.y + y) * tetromino_size,
                                tetromino_size - 1, tetromino_size - 1])
                
def draw_score(screen, score, grid_width, tetromino_size):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, color_white)
    screen.blit(score_text, (grid_width * tetromino_size + 10, 10))

# 繪製遊戲結束
def draw_game_over(screen, screen_width, screen_height):
    game_over_font = pygame.font.Font(None, 48)
    game_over_text = game_over_font.render('Game Over!', True, color_red)
    screen.blit(game_over_text, 
                (screen_width//2 - game_over_text.get_width()//2,
                 screen_height//2 - game_over_text.get_height()//2))