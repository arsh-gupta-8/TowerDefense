import pygame

pygame.init()

# Text
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

# Screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Tower Defense")
WIDTH = pygame.display.get_surface().get_width()
HEIGHT = pygame.display.get_surface().get_height()
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


def hex_to_rgb(hex_string):
    hex_string = hex_string[1:]
    rgb = []
    for i in range(0, 6, 2):
        rgb.append(int(hex_string[i:i+2], 16))
    return tuple(rgb)


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

    screen.fill(GRASS)

    for path in pathway:
        pygame.draw.rect(screen, PATH, path)

    if placement:
        x_cord_square = 0
        y_cord_square = 0
        for square_height in range(9):
            for square_width in range(16):
                pygame.draw.rect(screen, BLACK, pygame.Rect(x_cord_square, y_cord_square, w_ratio, h_ratio), 1)
                x_cord_square += w_ratio
            x_cord_square = 0
            y_cord_square += h_ratio

    pygame.display.update()
    clock.tick(FPS)


