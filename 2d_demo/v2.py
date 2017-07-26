import pygame, sys
from pygame.locals import *
import random

'''玩家随着方向键运动'''

# 玩家
class Player(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__()
        self.surf = pygame.Surface((75,25))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        
    def update(self, key):
        # 随着方向键运动
        if key[K_UP]:
            self.rect.move_ip(0,-5)
        if key[K_DOWN]:
            self.rect.move_ip(0,5)
        if key[K_LEFT]:
            self.rect.move_ip(-5,0)
        if key[K_RIGHT]:
            self.rect.move_ip(5,0)
            
        # 限定player在屏幕中
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
    

# 初始化
pygame.init()

# 屏幕对象
screen = pygame.display.set_mode((800,600)) # 尺寸

# 玩家精灵对象
player = Player()



# 窗口主循环
while True:
    # 遍历事件队列    
    for event in pygame.event.get():
        if event.type == QUIT: # 点击右上角的'X'，终止主循环
            pygame.quit()
            sys.exit()       
        elif event.type == KEYDOWN:           
            if event.key == K_ESCAPE: # 按下'ESC'键，终止主循环
                pygame.quit()
                sys.exit()                
    
    # 更新屏幕
    screen.fill((0,0,0))
    
    # 获得按键
    key = pygame.key.get_pressed() 
    
    # 更新玩家
    player.update(key)
    
    # 放置玩家
    screen.blit(player.surf, player.rect)

    # 更新界面
    pygame.display.flip()