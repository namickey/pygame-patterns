import pygame

# https://riptutorial.com/ja/pygame

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))



screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
FPS = 800  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

rect = pygame.Rect((0, 0), (40, 40))
image = pygame.Surface((40, 40))
image.fill(WHITE)

while True:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if rect.top > 0:
                    rect.move_ip(0, -40*dt)
            elif event.key == pygame.K_s:
                if rect.bottom < 400:
                    rect.move_ip(0, 40*dt)
            elif event.key == pygame.K_a:
                if rect.left > 0:
                    rect.move_ip(-40, 0)
            elif event.key == pygame.K_d:
                if rect.right < 400:
                    rect.move_ip(40, 0)

    screen.fill(BLACK)
    screen.blit(image, rect)
    #screen.blit(image, rect.move(2*16, 0))
    pygame.display.update()  # Or pygame.display.flip()
