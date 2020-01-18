import pygame

# https://riptutorial.com/ja/pygame

SCREEN_SIZE = 400
BLOCK_SIZE = 40
FPS = 60  # Frames per second.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()

class Command:
    def execute(self, player): print('no command.')
class MoveTop(Command):
    def execute(self, player): player.moveTop()
class MoveBottom(Command):
    def execute(self, player): player.moveBottom()
class MoveLeft(Command):
    def execute(self, player): player.moveLeft()
class MoveRight(Command):
    def execute(self, player): player.moveRight()
class InputHandler:
    def __init__(self):
        self.moveTop = MoveTop()
        self.moveBottom = MoveBottom()
        self.moveLeft = MoveLeft()
        self.moveRight = MoveRight()
    def handleInput(self):
        events = pygame.event.get()
        if self.isPressed(events, pygame.K_w): return self.moveTop
        if self.isPressed(events, pygame.K_s): return self.moveBottom
        if self.isPressed(events, pygame.K_a): return self.moveLeft
        if self.isPressed(events, pygame.K_d): return self.moveRight
        return None
    def isPressed(self, events, key):
        for event in events:
            if event.type == pygame.QUIT: quit()
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.onGoal = False
    def moveTop(self):
        if self.rect.top >= BLOCK_SIZE: self.rect.move_ip(0, -1*BLOCK_SIZE)
    def moveBottom(self):
        if self.rect.bottom + BLOCK_SIZE <= SCREEN_SIZE: self.rect.move_ip(0, BLOCK_SIZE)
    def moveLeft(self):
        if self.rect.left >= BLOCK_SIZE: self.rect.move_ip(-1*BLOCK_SIZE, 0)
    def moveRight(self):
        if self.rect.right + BLOCK_SIZE <= SCREEN_SIZE: self.rect.move_ip(BLOCK_SIZE, 0)
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
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.move_ip(BLOCK_SIZE*5, BLOCK_SIZE*5)

player = Player()
goal = Goal()
inputHandler = InputHandler()

while True:
    dt = clock.tick(FPS)/1000

    command = inputHandler.handleInput()
    if command:
        command.execute(player)

    screen.fill(BLACK)
    player.isGoal(goal)
    screen.blit(goal.image, goal.rect)
    screen.blit(player.image, player.rect)
    pygame.display.update()  # Or pygame.display.flip()
