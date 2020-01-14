import pygame

# https://riptutorial.com/ja/pygame

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.pos = [0, 0]
    def update(self):
        self.pos = [x+y for (x, y) in zip(self.velocity, self.pos)]
        x = 0
        if abs(self.pos[0]) > 40:
            x = abs(self.pos[0])/self.pos[0]*40
            self.pos[0] = 0
        y = 0
        if abs(self.pos[1]) > 40:
            y = abs(self.pos[1])/self.pos[1]*40
            self.pos[1] = 0
        self.rect.move_ip(x, y)

player = Player()
rect = pygame.Rect((0, 0), (40, 40))
image = pygame.Surface((40, 40))
image.fill(WHITE)

while True:
    dt = clock.tick(FPS)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.velocity[1] = -200*dt
                player.pos[1] = -20
            elif event.key == pygame.K_s:
                player.velocity[1] = 200*dt
                player.pos[1] = 20
            elif event.key == pygame.K_a:
                player.velocity[0] = -200*dt
                player.pos[0] = -20
            elif event.key == pygame.K_d:
                player.velocity[0] = 200*dt
                player.pos[0] = 20
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.velocity[1] = 0
                player.pos[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                player.velocity[0] = 0
                player.pos[0] = 0
    screen.fill(BLACK)
    player.update()
    screen.blit(player.image, player.rect)
    pygame.display.update()  # Or pygame.display.flip()
