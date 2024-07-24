import pygame

pygame.init()

# Text
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

# Screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Cookie Clicker")
WIDTH = pygame.display.get_surface().get_width()
HEIGHT = pygame.display.get_surface().get_height()
print(WIDTH, HEIGHT)

# Loop Start
clock = pygame.time.Clock()
running = True
FPS = 30

# Game Setting
cookies = 0
enlarge = False
shop_scroll = 0


def get_placement_hover(mouse_x, mouse_y):
    x_box_cord = 0
    y_box_cord = 0
    while mouse_x > 0:
        x_box_cord += 1
        mouse_x -= 80
    while mouse_y > 0:
        y_box_cord += 1
        mouse_y -= 80
    return x_box_cord, y_box_cord


def hex_to_rgb(hex_string):
    hex_string = hex_string[1:]
    rgb = []
    for i in range(0, 6, 2):
        rgb.append(int(hex_string[i:i+2], 16))
    return tuple(rgb)


def write(text):
    write_line = font.render("Cookies: " + str(text), False, (0, 0, 0))
    screen.blit(write_line, (0, 0))


def show_buttons(shop_scroll):
    pass


while running:

    x, y = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_1:
                unplaced = True
                while unplaced:
                    x, y = pygame.mouse.get_pos()
                    tower_x_hover, tower_y_hover = get_placement_hover(x, y)
                    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(tower_x_hover*80, tower_y_hover*80, 80, 80))
                    if event.key == pygame.K_SPACE:
                        unplaced = False
                    pygame.display.update()

        # if event.type == pygame.MOUSEBUTTONUP:
        #     if event.button == 1 and 75 <= x <= 325 and 90 <= y <= 340:
        #         cookies += 1
        #
        #     elif 480 <= x <= 820:
        #         if event.button == 4 and shop_scroll < 0:
        #             shop_scroll += 45
        #
        #         elif event.button == 5:
        #             shop_scroll -= 45

    x_cord_square = 0
    y_cord_square = 0
    screen.fill(hex_to_rgb("#C7EA46"))
    for square_height in range(HEIGHT//80):
        for square_width in range(WIDTH//80):
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x_cord_square, y_cord_square, 80, 80), 1)
            x_cord_square += 80
        x_cord_square = 0
        y_cord_square += 80
    write(cookies)
    show_buttons(shop_scroll)
    pygame.display.update()
    clock.tick(FPS)


