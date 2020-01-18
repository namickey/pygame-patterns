import pygame

# https://riptutorial.com/ja/pygame

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

SCREEN_SIZE = 400
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
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
        self.onGoal = False
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
        if self.rect.top + y >= 0 and self.rect.bottom + y <= SCREEN_SIZE:
            if self.rect.left + x >= 0 and self.rect.right + x <= SCREEN_SIZE:
                self.rect.move_ip(x, y)
    def isGoal(self, goal):
        if self.rect.colliderect(goal.rect):
            if not self.onGoal:
                print('goal')
                self.onGoal = True
        else:
            self.onGoal = False

class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.move_ip(40*5, 40*5)

player = Player()
goal = Goal()
VELOCITY = 200

while True:
    dt = clock.tick(FPS)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.velocity[1] = -1*VELOCITY*dt
                player.pos[1] = -40
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.velocity[1] = VELOCITY*dt
                player.pos[1] = 40
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.velocity[0] = -1*VELOCITY*dt
                player.pos[0] = -40
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.velocity[0] = VELOCITY*dt
                player.pos[0] = 40
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.velocity[1] = 0
                player.pos[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.velocity[0] = 0
                player.pos[0] = 0
    screen.fill(BLACK)
    player.update()
    player.isGoal(goal)
    screen.blit(goal.image, goal.rect)
    screen.blit(player.image, player.rect)
    pygame.display.update()  # Or pygame.display.flip()
