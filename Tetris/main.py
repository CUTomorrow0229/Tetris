import pygame
from game.game import Tetris_game

def main():
    # 初始化
    pygame.init()
    
    # 開始遊戲
    game = Tetris_game()
    game.run()
    
    # 關閉遊戲
    pygame.time.wait(2000)
    pygame.quit()

# 執行程式
if __name__ == '__main__':
    main()
    