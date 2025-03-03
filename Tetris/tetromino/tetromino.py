import random
from constant import shapes, tetromino_color, grid_width

# 方塊行為
class Tetromino:
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