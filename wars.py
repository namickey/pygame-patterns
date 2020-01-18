import pygame

# https://riptutorial.com/ja/pygame
FPS = 30
SCREEN_SIZE = 400
BLOCK_SIZE = 40

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Command:
    def __init__(self, world):
        self.world = world
    def execute(self, unit): print('no command.')
class MoveTop(Command):
    def execute(self, unit): unit.move(self.world, unit.rect.left, unit.rect.top-BLOCK_SIZE)
class MoveBottom(Command):
    def execute(self, unit): unit.move(self.world, unit.rect.left, unit.rect.top+BLOCK_SIZE)
class MoveLeft(Command):
    def execute(self, unit): unit.move(self.world, unit.rect.left-BLOCK_SIZE, unit.rect.top)
class MoveRight(Command):
    def execute(self, unit): unit.move(self.world, unit.rect.left+BLOCK_SIZE, unit.rect.top)
class Attack(Command):
    def execute(self, unit): unit.attack(self.world)
class ChangeUnit(Command):
    def execute(self, unit):
        self.world.selectedUnit += 1
        if len(self.world.unitList) <= self.world.selectedUnit:
            self.world.selectedUnit = 0
class InputHandler:
    def __init__(self, world):
        self.moveTop = MoveTop(world)
        self.moveBottom = MoveBottom(world)
        self.moveLeft = MoveLeft(world)
        self.moveRight = MoveRight(world)
        self.changeUnit = ChangeUnit(world)
        self.attack = Attack(world)
    def handleInput(self):
        events = pygame.event.get()
        if self.isPressed(events, pygame.K_w): return self.moveTop
        if self.isPressed(events, pygame.K_s): return self.moveBottom
        if self.isPressed(events, pygame.K_a): return self.moveLeft
        if self.isPressed(events, pygame.K_d): return self.moveRight
        if self.isPressed(events, pygame.K_SPACE): return self.changeUnit
        if self.isPressed(events, pygame.K_RIGHT): return self.attack
        return None
    def isPressed(self, events, key):
        for event in events:
            if event.type == pygame.QUIT: quit()
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False
class Unit(pygame.sprite.Sprite):
    def __init__(self, world, x, y, color):
        super().__init__()
        self.world = world
        self.life = 10
        self.power = 4
        self.text = world.sysfont.render(str(self.life), False, (0,0,0))
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(BLOCK_SIZE*x, BLOCK_SIZE*y)
    def attack(self, world):
        unit = world.getUnit(self.rect.left+BLOCK_SIZE, self.rect.top)
        if unit and unit.image.get_at((0,0)) != self.image.get_at((0,0)):
            unit.damage(self.power)
    def damage(self, power):
        self.life -= power
        self.text = self.world.sysfont.render(str(self.life), False, (0,0,0))
        if self.life <= 0:
            world.unitList.remove(self)
    def move(self, world, x, y):
        if world.checkUnit(x, y):
            if x >= 0 and x < SCREEN_SIZE and y >= 0 and y < SCREEN_SIZE:
                self.rect.left = x
                self.rect.top = y
class World:
    def __init__(self):
        self.sysfont = pygame.font.SysFont(None, 50)
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.clock = pygame.time.Clock()
        self.unitList = [Unit(self,1,1,GREEN), Unit(self,1,2,GREEN), Unit(self,8,8,BLUE), Unit(self,8,9,BLUE)]
        self.selectedUnit = 0
        self.movableList = []
    def createMovableList(self, unit):
        return [self.m(unit,1,0),self.m(unit,0,1),self.m(unit,-1,0),self.m(unit,0,-1)]
    def m(self, unit, x, y):
        return Unit(self, (unit.rect.left/BLOCK_SIZE)+x, (unit.rect.top/BLOCK_SIZE)+y, RED)
    def checkUnit(self, x, y):
        for u in self.unitList:
            if u.rect.left == x and u.rect.top == y:
                return False
        return True
    def getUnit(self, x, y):
        for u in self.unitList:
            if u.rect.left == x and u.rect.top == y:
                return u
    def start(self):
        inputHandler = InputHandler(self)
        while True:
            dt = self.clock.tick(FPS)/1000
            command = inputHandler.handleInput()
            if command:
                command.execute(self.unitList[self.selectedUnit])
            self.screen.fill(BLACK)
            self.movableList = self.createMovableList(self.unitList[self.selectedUnit])
            for u in self.movableList:
                self.screen.blit(u.image, u.rect)
            for u in self.unitList:
                self.screen.blit(u.image, u.rect)
                self.screen.blit(u.text, u.rect)
            pygame.display.update()

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
world = World()
world.start()
