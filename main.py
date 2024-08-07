import pygame

pygame.init()

# Text
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

# Screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH = pygame.display.get_surface().get_width()
HEIGHT = pygame.display.get_surface().get_height()
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Tower Defense")
w_ratio = WIDTH//16
h_ratio = HEIGHT//9
w_ratio_center = w_ratio * 0.2
h_ratio_center = h_ratio * 0.2

# Colours
GRASS = (199, 234, 70)
PATH = (211, 182, 131)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ENEMY_COLOURS = [PATH, (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (254, 127, 154)]

# Loop Start
clock = pygame.time.Clock()
running = True
FPS = 60

# Enemy Path
pathway = []
pathway.append(pygame.Rect(0, h_ratio * 7, w_ratio * 11, h_ratio))
pathway.append(pygame.Rect(w_ratio * 10, h_ratio * 4, w_ratio, h_ratio*3))
pathway.append(pygame.Rect(w_ratio * 2, h_ratio * 4, w_ratio * 8, h_ratio))
pathway.append(pygame.Rect(w_ratio * 2, h_ratio * 2, w_ratio, h_ratio * 2))
pathway.append(pygame.Rect(w_ratio * 2, h_ratio, w_ratio * 12, h_ratio))
pathway.append(pygame.Rect(w_ratio * 13, h_ratio, w_ratio, h_ratio * 13))

# Game Setting
placement = False
can_place = False
tower_cords = []
tower_bullets = []
wave_enemies = [[[5, 1]], [[5, 2]], [[5, 3]], [[5, 4]], [[5, 5]]]
enemies_list = []
enemy_now = 0
wave = 0
wave_end = True
dead = 0

class Enemy:
    def __init__(self, health):
        self.xp = w_ratio * -1
        self.yp = h_ratio * 7 + h_ratio_center
        self.path_num = 1
        self.speed = 5
        self.health = health
        self.colour = PATH

    def change_pos(self):
        if self.path_num == 1:
            if self.xp > w_ratio * 10 + w_ratio_center:
                self.xp = w_ratio * 10 + w_ratio_center
                self.path_num = 2
        elif self.path_num == 2:
            if self.yp < h_ratio * 4 + h_ratio_center:
                self.yp = h_ratio * 4 + h_ratio_center
                self.path_num = 3
        elif self.path_num == 3:
            if self.xp < w_ratio * 2 + w_ratio_center:
                self.xp = w_ratio * 2 + w_ratio_center
                self.path_num = 4
        elif self.path_num == 4:
            if self.yp < h_ratio + h_ratio_center:
                self.yp = h_ratio + h_ratio_center
                self.path_num = 5
        elif self.path_num == 5:
            if self.xp > w_ratio * 13 + w_ratio_center:
                self.xp = w_ratio * 13 + w_ratio_center
                self.path_num = 6

        if self.path_num == 1 or self.path_num == 5:
            self.xp += self.speed
        elif self.path_num == 2 or self.path_num == 4:
            self.yp -= self.speed
        elif self.path_num == 3:
            self.xp -= self.speed
        else:
            self.yp += self.speed

    def change_col(self):
        self.colour = ENEMY_COLOURS[self.health]

class Bullet:
    def __init__(self, alive):
        self.alive = alive
        self.xbp = -20
        self.ybp = -20
        self.x_change = 0
        self.y_change = 0
        self.bullet_speed = 30

    def calculate_change(self, enemy_x, enemy_y):
        x_scale = enemy_x - self.xbp + w_ratio_center
        y_scale = enemy_y - self.ybp + h_ratio_center
        neg_x = 1
        neg_y = 1
        if x_scale < 0:
            neg_x = -1
        if y_scale < 0:
            neg_y = -1
        x_scale = abs(x_scale)
        y_scale = abs(y_scale)
        if x_scale <= y_scale:
            self.x_change = (x_scale / y_scale) * self.bullet_speed * neg_x
            self.y_change = self.bullet_speed * neg_y
        else:
            self.x_change = self.bullet_speed * neg_x
            self.y_change = (y_scale / x_scale) * self.bullet_speed * neg_y

    def bullet_move(self):
        self.xbp += self.x_change
        self.ybp += self.y_change

while running:

    x, y = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                if placement:
                    placement = False
                else:
                    placement = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if placement and can_place:
                tower_cords.append(tower_cord)
                placement = False

    screen.fill(GRASS)

    for path in pathway:
        pygame.draw.rect(screen, PATH, path)

    if len(tower_bullets) < len(tower_cords):
        tower_bullets.append(Bullet(False))

    for i in range(len(tower_bullets)):
        if tower_bullets[i].alive:
            tower_bullets[i].bullet_move()
            bullet_cord = pygame.Rect(tower_bullets[i].xbp, tower_bullets[i].ybp, w_ratio_center, h_ratio_center)
            pygame.draw.rect(screen, BLACK, bullet_cord)
            if tower_bullets[i].xbp < 0 or tower_bullets[i].xbp > WIDTH or tower_bullets[i].ybp < 0 or tower_bullets[i].ybp > HEIGHT:
                tower_bullets[i].alive = False
            for j in range(enemy_now):
                enemy_cord = pygame.Rect(enemies_list[j].xp, enemies_list[j].yp, w_ratio * 0.6, h_ratio * 0.6)
                if bullet_cord.colliderect(enemy_cord):
                    enemies_list[j].health -= 1
                    tower_bullets[i].alive = False

        else:
            if len(enemies_list) > 0:
                tower_bullets[i].xbp = tower_cords[i][0] + w_ratio_center
                tower_bullets[i].ybp = tower_cords[i][1] + h_ratio_center
                tower_bullets[i].calculate_change(enemies_list[0].xp, enemies_list[0].yp)
                tower_bullets[i].alive = True

    for tower in tower_cords:
        pygame.draw.rect(screen, (0, 0, 139), tower)

    if placement:
        tower_x = w_ratio * (x // w_ratio) + w_ratio_center
        tower_y = h_ratio * (y // h_ratio) + h_ratio_center
        tower_cord = [tower_x, tower_y, w_ratio * 0.6, h_ratio * 0.6]
        if screen.get_at((x, y)) == PATH or tower_cord in tower_cords:
            can_place = False
            pygame.draw.rect(surface, (255, 0, 0, 80), [0, 0, WIDTH, HEIGHT])
        else:
            can_place = True
            pygame.draw.rect(surface, (0, 255, 0, 80), [0, 0, WIDTH, HEIGHT])
        pygame.draw.rect(surface, (0, 0, 139, 120), tower_cord)
        screen.blit(surface, (0, 0))

    if wave_end:
        wave_end = False
        for i in range(len(wave_enemies[wave])):
            for j in range(wave_enemies[wave][i][0]):
                enemies_list.append(Enemy(wave_enemies[wave][i][1]))
        enemy_total = len(enemies_list)
        enemy_now = 0
        spawned = 0
        spawn_timer = 0
        dead = 0

    else:
        dead = 0
        remove_list = []
        spawn_timer += 1
        if enemy_now < enemy_total and spawned != enemy_total:
            if spawn_timer % 30 == 1:
                enemy_now += 1
                spawned += 1

        for i in range(enemy_now):

            enemies_list[i].change_pos()
            enemies_list[i].change_col()
            enemy_cord = pygame.Rect(enemies_list[i].xp, enemies_list[i].yp, w_ratio * 0.6, h_ratio * 0.6)
            pygame.draw.rect(screen, enemies_list[i].colour, enemy_cord)

            if enemies_list[i].health == 0 or enemies_list[i].yp > HEIGHT:
                remove_list.append(i)
                dead += 1

        remove_list.reverse()

        for num in remove_list:
            enemies_list.pop(num)

        enemy_now -= dead

        if len(enemies_list) == 0:
            wave_end = True
            wave += 1

    pygame.display.update()
    clock.tick(FPS)


