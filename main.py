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


class Enemy:
    def __init__(self, xp, yp, path_num):
        self.xp = xp
        self.yp = yp
        self.path_num = path_num

    def change_pos(self):
        if self.path_num == 1:
            if self.xp > w_ratio * 10 + w_ratio * 0.20:
                self.path_num = 2
        elif self.path_num == 2:
            if self.yp < h_ratio * 4 - h_ratio * 0.20:
                self.path_num = 3
        elif self.path_num == 3:
            if self.xp < w_ratio * 3 - w_ratio * 0.20:
                self.path_num = 4
        elif self.path_num == 4:
            if self.yp < h_ratio - h_ratio * 0.20:
                self.path_num = 5
        elif self.path_num == 5:
            if self.xp < w_ratio * 13 + w_ratio * 0.20:
                self.path_num = 6

        if self.path_num == 1 or self.path_num == 5:
            self.xp += 5
        elif self.path_num == 2 or self.path_num == 4:
            self.yp += 5
        elif self.path_num == 3:
            self.xp -= 5
        else:
            self.yp -= 5


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

    pygame.display.update()
    clock.tick(FPS)


