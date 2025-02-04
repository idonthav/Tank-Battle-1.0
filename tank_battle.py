import pygame
from time import sleep
import random
from pygame.sprite import collide_rect

# 设置通用属性 | Set general attributes
BG_COLOR = pygame.Color(0,0,0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TEXT_COLOR = pygame.Color(255,0,0)

class Tank:
    '''
    坦克类 | Tank 
    '''
    def __init__(self):
        self.live = True
        # 记录坦克原来的位置 | Store tank's last position
        self.old_left = 0
        self.old_top = 0
    def display_tank(self):
        '''
        显示坦克类 | Display Tank
        '''
        # 获取最新坦克的朝向位置图片 | Get the lastest tank img's direction
        self.image = self.images.get(self.direction)
        MainGame.window.blit(self.image, self.rect)
    def move(self):
        '''
        坦克的移动 | tank movement
        '''
        # 记录坦克原来的位置,为了方便还原碰撞后的位置 | Store tank's last position to reset after collision
        self.old_left = self.rect.left
        self.old_top = self.rect.top
        if self.direction == 'L':
            # 判断坦克位置是否已在左边界 | Check if tank at the left boundary
            if self.rect.left > 0:
                # 修改坦克位置 离左边的距离     - 操作 | Update tank position - to left
                self.rect.left = self.rect.left - self.speed
        elif self.direction == 'R':
            # 判断坦克位置是否已在右边界 | Check if tank at the right boundary
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                # 修改坦克位置 离左边的距离     + 操作 | Update tank position + to left
                self.rect.left = self.rect.left + self.speed
        elif self.direction == 'U':
            # 判断坦克位置是否已在上边界 | Check if tank at the up boundary
            if self.rect.top > 0:
                # 修改坦克位置 离上边的距离     - 操作 | Update tank position - to up
                self.rect.top = self.rect.top - self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                # 修改坦克位置 离上边的距离     + 操作 | Update tank position + to up
                self.rect.top = self.rect.top + self.speed
    def shot(self):
        '''
        坦克的射击 | Tank shooting 
        '''
        pass
    def tank_hit_wall(self) -> None:
        '''
        坦克和墙壁的碰撞 | Tank collision with Wall
        '''
        for wall in MainGame.wall_list:
            # 检测当前坦克是否和墙壁发生碰撞,将位置还原到碰撞前的位置
            if pygame.sprite.collide_rect(self,wall):
                self.rect.left = self.old_left
                self.rect.top = self.old_top
    def tank_hit_tank(self,tank):
        '''
        检测2个坦克是否碰撞 | Check any 2 tanks collision
        '''
        # 判断是否都存活 | Check if all alive
        if self and tank and self.live and tank.live:
            if pygame.sprite.collide_rect(self,tank):
                # 将位置还原到碰撞前的位置 | Reset position as before-collision
                self.rect.left = self.old_left
                self.rect.top = self.old_top
class MyTank(Tank):
    '''
    我方坦克 | My Tank
    '''
    def __init__(self, left:int, top:int):
        super(MyTank,self).__init__()
        # 设置我方坦克图片资源 | Load my tank's imgs
        self.images = {
            'U':pygame.image.load('./img/p1tankU.gif'),
            'D':pygame.image.load('./img/p1tankD.gif'),
            'L':pygame.image.load('./img/p1tankL.gif'),
            'R':pygame.image.load('./img/p1tankR.gif')
        }
        # 设置我方坦克方向 | Set my tank direction
        self.direction = 'L'
        # 获取图片信息 | Get img
        self.image = self.images.get(self.direction)
        # 获取图片的矩形 | Get rect
        self.rect = self.image.get_rect()
        # 设置我方坦克位置 | Set my tank position
        self.rect.left = left
        self.rect.top = top
        # 设置坦克移动速度 | Set speed
        self.speed = 5
        # 设置移动开关 | Set movement option
        self.remove = False
class EnemyTank(Tank):
    '''
    敌方坦克 | Enemy Tank
    '''  
    def __init__(self,left,top,speed):
        # 初始化父类Tank __init__ nadao .live属性 | Initialize Parent class Tank __init__, get .live attribute
        super(EnemyTank,self).__init__()
        self.images = {
            'U':pygame.image.load('./img/enemy1U.gif'),
            'D':pygame.image.load('./img/enemy1D.gif'),
            'L':pygame.image.load('./img/enemy1L.gif'),
            'R':pygame.image.load('./img/enemy1R.gif'),
        }
        # 设置敌方坦克方向 | Set enemy tank direction
        self.direction = self.rand_direction()
        # 获取图片信息 | Get img
        self.image =self.images.get(self.direction)
        # 获取图片的矩形 | Get rect
        self.rect = self.image.get_rect()
        # 设置敌方坦克位置 | Set position
        self.rect.left = left
        self.rect.top = top
        # 设置移动速度 | Set speed
        self.speed = speed
        # 设置移动的步长 | Set step
        self.step = 50
        
    def rand_direction(self) -> str:
        '''
        生成随机方向 | Reture random direction
        '''
        choice = random.randint(1,4)
        if choice == 1:
            return 'U'
        elif choice == 2:
            return 'D'
        elif choice == 3:
            return 'L'
        elif choice == 4:
            return 'R'
    def rand_move(self):
        '''
        随机移动 | Random movement
        '''
        # 判断步长是否为0 | Check if step is 0
        if self.step <= 0:
            # 如果小于0，更换方向 | if step<0, change direction
            self.direction = self.rand_direction()
            # 重置步长 | Reset step
            self.step = 30
        else:
            # 如果大于0，移动 | if >0, move
            self.move()
            # 步长减1 | step -= 1
            self.step -= 1
    def shot(self):
        '''
        敌方坦克的射击 | Enemy tank shooting
        '''
        num = random.randint(1,100)
        if num < 5:
            return Bullet(self)
            
class Bullet:
    '''
    子弹类 | Bullet
    '''
    def __init__(self,tank):
        # 加载图片 | Load img
        self.image = pygame.image.load('./img/enemymissile.gif')
        # 获取子弹的方向 | Get bullet direction
        self.direction = tank.direction
        # 获取子弹的图形 | Get rect
        self.rect = self.image.get_rect()
        # 设置子弹位置 | Set bullet position
        if self.direction == 'L':
            # 子弹位置 = 坦克位置 - 子弹宽度 | bullet position = tank position - bullet's width
            self.rect.left = tank.rect.left - self.rect.width
            # 子弹位置 = 坦克位置 + 坦克高度/2 -子弹高度/2
            self.rect.top = tank.rect.top + tank.rect.height/2 - self.rect.height/2
        elif self.direction == 'R':
            # 子弹位置 = 坦克位置 + 坦克宽度
            self.rect.left = tank.rect.left + tank.rect.width
            # 子弹位置 = 坦克位置 + 坦克高度/2 - 子弹高度/2
            self.rect.top = tank.rect.top + tank.rect.height/2 - self.rect.height/2
        elif self.direction == 'U':
            # 子弹位置 = 坦克的位置 + 坦克的宽度/2 - 子弹的宽度/2
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            # 子弹位置 = 坦克的位置 - 子弹的高度
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            # 子弹位置 = 坦克位置 + 坦克宽度/2 - 子弹宽度/2
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            # 子弹位置 = 坦克位置 + 坦克高度
            self.rect.top = tank.rect.top + tank.rect.height
        # 设置子弹速度 | Set bullet speed
        self.speed = 5
        # 设置子弹的状态 | Set bullet status
        self.live = True
    def display_bullet(self):
        '''
        显示子弹 | Displaying bullet
        '''
        MainGame.window.blit(self.image, self.rect)
    def move(self):
        '''
        子弹的移动 | bullet movement
        '''
        # 根据子弹生成的方向来移动 | bullet position control move direction
        if self.direction == 'L':
            # 判断子弹是否超出屏幕 | Check if exceed window
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            # 判断子弹是否超出屏幕 | Check if exceed window
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False
        elif self.direction == 'U':
            # 判断子弹是否超出屏幕 | Check if exceed window
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            # 判断子弹是否超出屏幕 | Check if exceed window
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
    def hit_enemy_tank(self):
        for e_tank in MainGame.enemy_tank_list:
            # 判断子弹是否击中坦克 | Check if bullet hit tank
            if collide_rect(self,e_tank):
                # 爆炸效果 | Explode
                explode = Explode(e_tank)
                MainGame.explode_list.append(explode)
                # 修改子弹的状态 | Update bullet status
                self.live = False
                e_tank.live = False
    def hit_my_tank(self):
        # 判断我方坦克是否活着 | Check if my tank alive
        if MainGame.my_tank and MainGame.my_tank.live:
            # 判断子弹是否击中我方坦克 | Check if bullet hit my tank
            if collide_rect(self,MainGame.my_tank):
                # 爆炸效果 | Explode
                explode = Explode(MainGame.my_tank)
                MainGame.explode_list.append(explode)
                # 修改子弹的状态 | Update bullet status
                self.live = False
                MainGame.my_tank.live = False
    def hit_wall(self):
        '''
        碰撞墙壁 | Hit wall
        '''
        for wall in MainGame.wall_list:
            # 判断是否撞墙 | Check if hit wall
            if collide_rect(self,wall):
                # 修改子弹的状态 | Update bullet status
                self.live = False
                # 修改墙壁的生命值 | Update wall hp
                wall.hp -= 1  
                # 判断墙壁是否依然显示 | Check if wall visible
                if wall.hp <= 0:
                    wall.live = False
                # 创建攻击墙壁的音效 | Create wall hitting sound effect
                music = Music('./img/hit.wav')
                music.play_music()
class Wall:
    '''
    墙壁类 | Wall
    '''
    def __init__(self,left,top):
        # 加载图片 | Load img
        self.image = pygame.image.load('./img/steels.gif')
        # 获取墙壁的图形 | get rect
        self.rect = self.image.get_rect()
        # 设置墙壁的位置 | set wall position
        self.rect.left = left
        self.rect.top = top
        # 设置墙壁生命值 | set wall hp
        self.hp = 3
        # 设置墙壁的状态 | set wall status
        self.live = True
    def display_wall(self):
        '''
        显示墙壁 | display wall
        '''
        MainGame.window.blit(self.image,self.rect)
class Explode:
    '''
    爆炸效果类 | Explode 
    '''
    def __init__(self,tank:Tank):
        # 加载爆炸效果的图片 | load explode img
        self.images = [
            pygame.image.load('./img/blast0.gif'),
            pygame.image.load('./img/blast1.gif'),
            pygame.image.load('./img/blast2.gif'),
            pygame.image.load('./img/blast3.gif'),
            pygame.image.load('./img/blast4.gif'),
        ]
        # 设置爆炸效果的位置 | set explode position
        self.rect = tank.rect
        # 设置爆炸效果的索引 | set explode index
        self.step = 0
        # 获取需要渲染的图像 | get rendred img
        self.image = self.images[self.step]
        # 设置爆炸状态 | set explode status
        self.live = True
    def display_explode(self):
        '''
        显示爆炸效果 | display explode 
        '''
        # 判断当前爆炸照片的效果是否播放完毕 | check if explode img collection end
        if self.step < len(self.images):
            # 获取当前爆炸效果的图片 | get current explode img
            self.image = self.images[self.step]
            # 获取下一张爆炸效果的图像的索引 | get next explode img index
            self.step += 1
            # 绘制爆炸效果 | show explode
            MainGame.window.blit(self.image, self.rect)
        else:
            self.step = 0
            # 设置爆炸效果的状态，代表爆炸过了 | update explode status
            self.live = False
class Music:
    '''
    音效类 | Music
    '''
    pygame.mixer.init()
    def __init__(self,filename: str):
        # 创建音乐文件 | load music file
        pygame.mixer.music.load(filename)
    def play_music(self):
        '''
        播放音效 | play music
        '''
        pygame.mixer.music.play()
class MainGame:
    '''
    游戏主窗口类 | game window
    '''
    # 游戏主窗口对象 | initialize window
    window = None
    # 设置我方坦克 | initialize my tank
    my_tank = None
    # 存储敌方坦克的列表 | store enemy tank
    enemy_tank_list = []
    # 设置敌方坦克的数量 | initialize enemy tank number
    enemy_tank_count = 6
    # 存储我方子弹列表 | store my tank's bullet
    my_bullet_list = []
    # 存储敌方坦克列表 | store enemy tank's bullet
    enemy_bullet_list = []
    # 存储爆炸效果的列表 | store explode 
    explode_list = []
    # 存储墙壁的列表 | store wall
    wall_list = []

    def __init__(self):
        pass
    def start_game(self):
        '''
        开始游戏 | game start
        '''
        # 初始化游戏窗口 | Initialie window
        pygame.init()
        # 创建一个窗口 | create a window
        MainGame.window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        # 设置窗口标题 | game name
        pygame.display.set_caption('Tank Battle 1.0')
        # 创建一个我方坦克 | create my tank
        # MainGame.my_tank = MyTank(350, 200)
        self.create_my_tank()
        # 创建敌方坦克 | create enemy tank
        self.create_enemy_tank()
        # 创建墙壁 | create wall
        self.create_wall()
        # 刷新窗口 | refresh window
        while True:
            sleep(0.02)
            # 给窗口设置填充色 | bg corlor
            MainGame.window.fill(BG_COLOR)
            # 增加提示文字 | remaining bullet number
            # 1.要增加文字内容
            # num = 6
            text = self.get_text_surface(f'Enemy tank remianing bullet {len(MainGame.enemy_tank_list)}')
            # 2.如何把文字加上 | blit above text
            MainGame.window.blit(text,(10,10))
            # 增加事件 | an event 
            self.get_event()
            # 判断我方坦克是否死亡 | check if my tank alive
            if MainGame.my_tank and MainGame.my_tank.live:
                # 显示我方坦克 | dispay my tank
                MainGame.my_tank.display_tank()
            else:
                MainGame.my_tank = None
            # 显示敌方坦克 | display enemy tank
            self.display_enemy_tank()
            # 判断我方坦克是否死亡 | check if my tank alive
            if MainGame.my_tank and MainGame.my_tank.live:
                # 移动坦克, False表示不移动，True表示移动
                if MainGame.my_tank.remove:
                    MainGame.my_tank.move() 
                    # 检测我方坦克是否与墙壁发生碰撞 | check if my tank hit the wall
                    MainGame.my_tank.tank_hit_wall()
                    # 检测我方坦克是否与敌方坦克发生碰撞 | check if my tank hit tenemy
                    for enemy in MainGame.enemy_tank_list:
                        MainGame.my_tank.tank_hit_tank(enemy)
            # 显示我方子弹
            self.display_my_bullet()
            # 显示敌方子弹
            self.display_enemy_bullet()
            # 显示爆炸效果
            self.display_explode()
            # 显示墙壁
            self.display_wall()
            pygame.display.update()
    
    def create_wall(self) -> None:
        '''
        创建墙壁
        '''
        top = 200
        for i in range(6):
            # 创建墙壁
            wall = Wall(i*148,top)
            # 将墙壁增加到列表中
            MainGame.wall_list.append(wall)
    
    def display_wall(self) -> None:
        '''
        显示墙壁
        '''
        for wall in MainGame.wall_list:
            if wall.live:
                # 显示墙壁
                wall.display_wall()
            else:
                # 从列表中删除
                MainGame.wall_list.remove(wall)

    def create_my_tank(self) -> None:
        '''
        创建我方坦克
        '''
        MainGame.my_tank = MyTank(350,300)
        # 创建音乐对象 
        music = Music('./img/start.wav')
        # 播放音乐
        music.play_music()
    def display_explode(self) -> None:
        '''
        显示爆炸效果
        '''
        for explode in MainGame.explode_list:
            # 判断是否活着
            if explode.live:
                # 显示爆炸效果
                explode.display_explode()
            else:
                # 从列表中删除
                MainGame.explode_list.remove(explode)
    def display_my_bullet(self) -> None:
        '''
        显示我方子弹
        '''
        for my_bullet in MainGame.my_bullet_list:
            # 判断子弹是否粗活
            if my_bullet.live:
                # 显示我方子弹
                my_bullet.display_bullet()
                # 移动我方子弹
                my_bullet.move()
                # 判断我方坦克是否击中敌方坦克
                my_bullet.hit_enemy_tank()
                # 判断我方子弹 是否击中墙壁
                my_bullet.hit_wall()
            else:
                MainGame.my_bullet_list.remove(my_bullet)
    def create_enemy_tank(self) -> None:
        '''
        创建敌方坦克
        '''
        self.enemy_top = 100
        self.enemy_speed = 3
        for i in range(self.enemy_tank_count):
            # 生成坦克的位置
            left = random.randint(0,600)
            # 创建敌方坦克
            e_tank = EnemyTank(left,self.enemy_top,self.enemy_speed)
            # 将地反坦克增加到列表中
            self.enemy_tank_list.append(e_tank)

    def display_enemy_tank(self) -> None:
        '''
        显示敌方坦克
        '''
        for e_tank in self.enemy_tank_list:
            # 判断敌方坦克是否存活
            if e_tank.live:
                # 显示敌方坦克
                e_tank.display_tank()
                # 移动敌方坦克
                e_tank.rand_move()
                # 判断是否与墙壁发生碰撞
                e_tank.tank_hit_wall()
                # 判断是否与我方坦克发生碰撞
                e_tank.tank_hit_tank(MainGame.my_tank)
                # 发射子弹
                e_bullet = e_tank.shot()
                # 判断是否有子弹
                if e_bullet:
                    # 将子弹增加到列表中
                    MainGame.enemy_bullet_list.append(e_bullet)
            else:
                # 从列表中删除
                self.enemy_tank_list.remove(e_tank)
    def display_enemy_bullet(self):
        '''
        显示敌方子弹
        '''
        for e_bullet in MainGame.enemy_bullet_list:
            # 显示子弹
            if e_bullet.live:
                # 如果子弹存活，显示子弹
                e_bullet.display_bullet()
                e_bullet.move()   
                # 判断是否击中我方坦克
                e_bullet.hit_my_tank()
            else:
                # 如果子弹不存活，从列表中移除
                MainGame.enemy_bullet_list.remove(e_bullet)    

    def get_text_surface(self, text:str):
        '''
        获取文字的图片
        '''
        # 初始化字体模块
        pygame.font.init()
        # 获取可以使用字体
        # print(pygame.font.get_fonts())
        # 创建字体
        font = pygame.font.SysFont('kaiti',18)
        # 绘制文字信息
        text_surface = font.render(text, True, TEXT_COLOR)
        # 将绘制的文字信息返回
        return text_surface
    def get_event(self):
        '''
        获取事件
        '''
        # 获取所有事件
        event_list = pygame.event.get()
        # 遍历事件
        for event in event_list:
            # 判断是什么事件，然后做出相应的处理
            if event.type == pygame.QUIT:
                # 点击关闭按钮
                self.end_game()
            if event.type == pygame.KEYDOWN:
                # 如果我方坦克死亡，按Esc键，重新生成我方坦克
                if not MainGame.my_tank and event.key == pygame.K_ESCAPE:           
                    self.create_my_tank()
                # 判断我方坦克是否活着
                if MainGame.my_tank and MainGame.my_tank.live:
                    # 按下键盘
                    if event.key == pygame.K_LEFT:
                        print('坦克向左移动')
                        # 修改方向
                        MainGame.my_tank.direction = 'L'
                        # 修改坦克移动状态为True
                        MainGame.my_tank.remove = True                   
                    elif event.key == pygame.K_RIGHT:
                        print('坦克向右移动')
                        # 修改方向
                        MainGame.my_tank.direction = 'R'
                        # 修改坦克移动状态为True
                        MainGame.my_tank.remove = True
                    elif event.key == pygame.K_UP:
                        print('坦克向上移动')
                        # 修改方向
                        MainGame.my_tank.direction = 'U'
                        # 修改坦克移动状态为True
                        MainGame.my_tank.remove = True
                    elif event.key == pygame.K_DOWN:
                        print('坦克向下移动')
                        # 修改方向
                        MainGame.my_tank.direction = 'D'
                        # 修改坦克移动状态为True
                        MainGame.my_tank.remove = True
                    elif event.key == pygame.K_SPACE:
                        # 判断子弹是否上限
                        if len(MainGame.my_bullet_list) < 5:
                            # 发射子弹
                            print('发射子弹')
                            # 创建子弹
                            m_bullet = Bullet(MainGame.my_tank)
                            MainGame.my_bullet_list.append(m_bullet)  
                            # 播放发射子弹的音乐
                            music = Music('./img/fire.wav')    
                            music.play_music()      
            if event.type == pygame.KEYUP and event.key in (pygame.K_LEFT, pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
                # 判断我方坦克是否活着：
                if MainGame.my_tank and MainGame.my_tank.live:
                    # 修改坦克移动状态为False
                    MainGame.my_tank.remove = False
    def end_game(self):
        '''
        Game Over
        '''
        print('Thankyou. Play again')
        exit()


if __name__ == '__main__':
    # 调用MainGame类中的start_game方法，开始游戏 | start the game 
    MainGame().start_game()