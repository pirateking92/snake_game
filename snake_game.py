import pygame
import sys
import random

pygame.init()

SW, SH = 800, 800

BLOCK_SIZE = 50

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("SNAAAAAKE! by Matt")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = [pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.body = []
        self.dead = False
        self.apple_eaten = False

    def update(self):
        global apple
        for square in self.body:
            if self.head[0].colliderect(square):
                self.dead = True
        if not (0 <= self.head[0].x < SW) or not (0 <= self.head[0].y < SH):
            self.dead = True

        if self.dead:
            if self.head[0].colliderect(apple.rect):
                self.body.append(pygame.Rect(self.head[0].x, self.head[0].y, BLOCK_SIZE, BLOCK_SIZE))
                apple.respawn()
                self.dead = False
            else:
                self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
                self.head = [pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)]
                self.body = []
                self.xdir = 1
                self.ydir = 0
                apple = Apple()

        if not self.dead:
            if self.head[0].colliderect(apple.rect) and not self.apple_eaten:
                self.body.append(pygame.Rect(self.head[0].x, self.head[0].y, BLOCK_SIZE, BLOCK_SIZE))
                self.apple_eaten = True
            else:
                self.apple_eaten = False

            self.body.append(self.head[0].copy())
            for i in range(len(self.body) - 1):
                self.body[i].x = self.body[i + 1].x
                self.body[i].y = self.body[i + 1].y
            self.head[0].x += self.xdir * BLOCK_SIZE
            self.head[0].y += self.ydir * BLOCK_SIZE
            if len(self.body) > 0:
                self.body.pop()

class Apple:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.x = random.randint(0, (SW - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.y = random.randint(0, (SH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)

def draw_grid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "green", rect, 1)

draw_grid()

snake = Snake()
apple = Apple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT:
                snake.ydir = 0
                snake.xdir = -1

    snake.update()

    screen.fill('black')
    draw_grid()

    apple.update()

    pygame.draw.rect(screen, "green", snake.head[0])

    for square in snake.body:
        pygame.draw.rect(screen, "green", square)
    
    if snake.head[0].x == apple.x and snake.head[0].y == apple.y:
        snake.body.append(pygame.Rect(snake.head[0].x, snake.head[0].y, BLOCK_SIZE, BLOCK_SIZE))
        apple.respawn()

    pygame.display.update()
    clock.tick(10)
