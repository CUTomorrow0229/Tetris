import pygame
import random

# 初始化
pygame.init()

# 定義顏色
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_cyan = (0, 255, 255)
color_yellow = (255, 255, 0)
color_pink = (255, 0, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_orange = (255, 150, 0)

# 場地常數
tetromino_size = 30
grid_width = 10
grid_height = 20
screen_width = tetromino_size * (grid_width + 8)
screen_height =tetromino_size * grid_height

# 方塊形狀
shapes = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1, 0], [0, 1, 1]], # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

# 方塊顏色
tetromino_color = [color_cyan, color_yellow, color_pink, color_orange, color_blue, color_green, color_red]

# 方塊行為
class tetromino:
    # 方塊初始化（選定方塊形狀、顏色、位置）
    def __init__(self):
        self.shape_idx = random.randint(0, len(shapes) - 1)
        self.shape = shapes[self.shape_idx]
        self.color = tetromino_color[self.shape_idx]
        self.x = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0
        
    # 旋轉方塊
    def rotate(self):
        '''
        旋轉的原理：
        先用self.shape[::-1]把矩陣上下顛倒
        再用zip(*)把矩陣轉置
        '''
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# 遊戲行為
class TetrisGame:
    # 初始化整個遊戲
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        self.current_piece = tetromino()
        self.game_over = False
        self.score = 0

    # 繪製網格    
    def draw_grid(self):
        for y in range(grid_height):
            for x in range(grid_width):
                if self.grid[y][x]:
                    color = self.grid[y][x]
                    pygame.draw.rect(self.screen, color,
                                   [x * tetromino_size, y * tetromino_size,
                                    tetromino_size - 1, tetromino_size - 1])
    
    # 繪製正在落下的方塊                
    def draw_current_piece(self):
        shape = self.current_piece.shape
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x]:
                    pygame.draw.rect(self.screen, self.current_piece.color,
                                   [(self.current_piece.x + x) * tetromino_size,
                                    (self.current_piece.y + y) * tetromino_size,
                                    tetromino_size - 1, tetromino_size - 1])

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
                    self.current_piece = tetromino()
                    if self.check_collision():
                        self.game_over = True
                fall_time = 0
            
            # 事件處理
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
            self.draw_grid()
            self.draw_current_piece()
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, color_white)
            self.screen.blit(score_text, (grid_width * tetromino_size + 10, 10))
            
            pygame.display.flip()
        
        # 顯示遊戲結束
        game_over_font = pygame.font.Font(None, 48)
        game_over_text = game_over_font.render('Game Over!', True, color_red)
        self.screen.blit(game_over_text, 
                        (screen_width//2 - game_over_text.get_width()//2,
                         screen_height//2 - game_over_text.get_height()//2))
        pygame.display.flip()
        

# 執行程式
if __name__ == '__main__':
    game = TetrisGame()
    game.run()
    pygame.time.wait(2000)
    pygame.quit()