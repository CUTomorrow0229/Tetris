import pygame
from constant import (grid_width, grid_height, screen_width, screen_height,
                      tetromino_size, color_black, color_red)
from tetromino.tetromino import Tetromino
from drawing.drawing import draw_current_piece, draw_grid, draw_game_over, draw_score

class Tetris_game:
    # 初始化整個遊戲
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        self.current_piece = Tetromino()
        self.game_over = False
        self.score = 0

    # 碰撞檢測                
    def check_collision(self, dx=0, dy=0):
        for y in range(len(self.current_piece.shape)):
            for x in range(len(self.current_piece.shape[y])):
                if self.current_piece.shape[y][x]:
                    new_x = self.current_piece.x + x + dx
                    new_y = self.current_piece.y + y + dy
                    if (new_x < 0 or new_x >= grid_width or
                        new_y >= grid_height or
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return True
        return False
    
    # 合併方塊
    def merge_piece(self):
        for y in range(len(self.current_piece.shape)):
            for x in range(len(self.current_piece.shape[y])):
                if self.current_piece.shape[y][x]:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color

    # 消除方塊、加分                
    def remove_complete_lines(self):
        lines_cleared = 0
        y = grid_height - 1
        '''
        從最下面開始檢查
        如果整列都有方塊
        消行數+1
        該列以上全部向下移一排
        頂部多加一列（空的）
        沒有就繼續往上檢查
        '''
        while y >= 0:
            if all(self.grid[y]):
                lines_cleared += 1
                for move_y in range(y, 0, -1):
                    self.grid[move_y] = self.grid[move_y - 1][:]
                self.grid[0] = [0] * grid_width
            else:
                y -= 1
        self.score += lines_cleared * 100

    # 主要執行項目    
    def run(self):
        fall_time = 0
        fall_speed = 500
        
        while not self.game_over:
            fall_time += self.clock.get_rawtime()
            self.clock.tick()
            
            # 方塊行為
            if fall_time >= fall_speed:
                if not self.check_collision(dy=1):
                    self.current_piece.y += 1
                else:
                    self.merge_piece()
                    self.remove_complete_lines()
                    self.current_piece = Tetromino()
                    if self.check_collision():
                        self.game_over = True
                fall_time = 0
            
            # 事件處理（退出、左右上下）
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not self.check_collision(dx=-1):
                        self.current_piece.x -= 1
                    if event.key == pygame.K_RIGHT and not self.check_collision(dx=1):
                        self.current_piece.x += 1
                    if event.key == pygame.K_DOWN and not self.check_collision(dy=1):
                        self.current_piece.y += 1
                    if event.key == pygame.K_UP:
                        self.current_piece.rotate()
            
            # 畫面顯示
            self.screen.fill(color_black)
            draw_grid(self.screen, self.grid)
            draw_current_piece(self.screen, self.current_piece)
            draw_score(self.screen, self.score, grid_width, tetromino_size)            
            
            pygame.display.flip()
        
        draw_game_over(self.screen, screen_width, screen_height)
        pygame.display.flip()