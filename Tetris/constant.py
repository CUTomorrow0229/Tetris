import pygame

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
