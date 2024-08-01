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

# Colours
GRASS = (199, 234, 70)
PATH = (211, 182, 131)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
wave_enemies = [[[5, 1]], [[10, 1], [5, 2]]]
enemies_list = []
wave = 0
wave_end = True

class Enemy:
    def __init__(self, health):
        self.xp = w_ratio * -1
        self.yp = h_ratio * 7 + h_ratio * 0.2
        self.path_num = 1
        self.speed = 5
        self.health = health

    def change_pos(self):
        if self.path_num == 1:
            if self.xp > w_ratio * 10 + w_ratio * 0.20:
                self.xp = w_ratio * 10 + w_ratio * 0.20
                self.path_num = 2
        elif self.path_num == 2:
            if self.yp < h_ratio * 4 + h_ratio * 0.20:
                self.yp = h_ratio * 4 + h_ratio * 0.20
                self.path_num = 3
        elif self.path_num == 3:
            if self.xp < w_ratio * 2 + w_ratio * 0.20:
                self.xp = w_ratio * 2 + w_ratio * 0.20
                self.path_num = 4
        elif self.path_num == 4:
            if self.yp < h_ratio + h_ratio * 0.20:
                self.yp = h_ratio + h_ratio * 0.20
                self.path_num = 5
        elif self.path_num == 5:
            if self.xp > w_ratio * 13 + w_ratio * 0.20:
                self.xp = w_ratio * 13 + w_ratio * 0.20
                self.path_num = 6

        if self.path_num == 1 or self.path_num == 5:
            self.xp += self.speed
        elif self.path_num == 2 or self.path_num == 4:
            self.yp -= self.speed
        elif self.path_num == 3:
            self.xp -= self.speed
        else:
            self.yp += self.speed


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

    for tower in tower_cords:
        pygame.draw.rect(screen, (0, 0, 139), tower)

    if placement:
        tower_x = w_ratio * (x // w_ratio) + w_ratio * 0.2
        tower_y = h_ratio * (y // h_ratio) + h_ratio * 0.2
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
        spawn_timer = 0
    else:
        spawn_timer += 1
        if enemy_now < enemy_total:
            if spawn_timer % 30 == 1:
                enemy_now += 1
        for i in range(enemy_now):
            enemies_list[i].change_pos()
            pygame.draw.rect(screen, BLACK, [enemies_list[i].xp, enemies_list[i].yp, w_ratio * 0.6, h_ratio * 0.6])

    pygame.display.update()
    clock.tick(FPS)


