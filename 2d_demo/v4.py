import pygame, sys
from pygame.locals import *
import random

'''飞机躲避导弹'''

# 玩家
class Player(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__()
        self.image = pygame.image.load('jet.png').convert() # load函数，返回一个 Surface 对象
        self.image.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.image.get_rect()
        
    def update(self, key):
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
    
# 敌人
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('missile.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(820, random.randint(0, 600)))
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0) # 从右向左
        if self.rect.right < 0:
            self.kill() # Sprite 的内建方法

# 白云
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('cloud.png').convert()
        self.image.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.image.get_rect(
            center = (random.randint(820,900),random.randint(0,600))
        )

    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right < 0:
            self.kill()
            
# 游戏初始化
pygame.init()

# 屏幕对象
screen = pygame.display.set_mode((800,600)) # 尺寸

# 背景Surface
background = pygame.Surface(screen.get_size())
background.fill((135, 206, 250)) # 浅蓝色

# 两个自定义事件
ADDENEMY = pygame.USEREVENT + 1      # 事件本质上就是整数常量。比 USEREVENT 小的数值已经对应内置事件，因此任何自定义事件都必须比 USEREVENT 大）
pygame.time.set_timer(ADDENEMY, 250) # 每隔 250 毫秒(四分之一秒) 触发
ADDCLOUD = pygame.USEREVENT + 2        
pygame.time.set_timer(ADDCLOUD, 1000)

# 玩家精灵对象
player = Player()

# 三个精灵组
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# 窗口主循环
while True:
    # 遍历事件队列    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()       
        elif event.type == KEYDOWN:           
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()                
        elif event.type == ADDENEMY: # 自定义事件
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD: # 自定义事件
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
            
    # 背景
    screen.blit(background, (0, 0))
    
    # 获取按键
    key = pygame.key.get_pressed()
    
    # 更新精灵（组）
    player.update(key)
    enemies.update()
    clouds.update()
    
    # 放置精灵
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)
    
    # 碰撞检测（灵魂所在）
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        #print('发生碰撞！')
    
    # 重绘界面
    pygame.display.flip()