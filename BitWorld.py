import pygame
import time
from Map import *

if __name__ == "__main__":
    WIN_SIZE = 600
    viewDistance = 5
    pixelSide = round(WIN_SIZE/(viewDistance*2+1))
    gameMap = Map(initialSize=(0,0))

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    display: pygame.display = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
    timer = pygame.time.Clock()

    x = y = 0

    running = True
    while running:
        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            x -= 1

        if keys_pressed[pygame.K_RIGHT]:
            x += 1

        if keys_pressed[pygame.K_UP]:
            y -= 1

        if keys_pressed[pygame.K_DOWN]:
            y += 1

        for yPixel, line in enumerate(gameMap.view((x, y), viewDistance)):
            for xPixel, pixel in enumerate(line):
                position = (pixelSide*yPixel, pixelSide *
                            xPixel, pixelSide, pixelSide)
                pygame.draw.rect(display, pixel, position)

        pygame.draw.rect(display, (0, 0, 0), (pixelSide*viewDistance,
                                              pixelSide*viewDistance, pixelSide, pixelSide))

        FPS = font.render(
            f"FPS: {round(timer.get_fps())}", True, (255, 255, 255))
        display.blit(FPS, (0, 0))
        mapSize = font.render(
            f"Size: {gameMap.memoryUsage()//1000} KB", True, (255, 255, 255))
        display.blit(mapSize, (0, 30))

        pygame.display.update()
        timer.tick(10)
