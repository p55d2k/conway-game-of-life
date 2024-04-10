from colorama import Fore
import pygame
import random
import time
import json
import sys
import os

print("\033c")
print(Fore.RED + "Conway's Game of Life\n")
time.sleep(0.5)

print(Fore.GREEN + "Click on the Grid to Toggle Cells")
print("Press Right Arrow Key to Move to Next Generation")
print("Press Left Arrow Key to Move to Previous Generation")
print("Press S to Auto Run the Simulation until stopped by pressing S again")
print("Press E to Randomize the Grid")
print("Press R to Reset the Grid")
print("Press Ctrl+C to Exit\n" + Fore.BLUE)
time.sleep(0.5)

if os.path.exists("config.json"):
    with open("config.json", "r") as f:
        print("Config File found, using values from config.json")
        config = json.load(f)
        try:
            GRIDSIZE = min(config["GRIDSIZE"], 100)
            SIMULATION_SPEED = config["SIMULATION_SPEED"]
            WIDTH = config["WIDTH"]
            HEIGHT = config["HEIGHT"]
        except:
            print("Invalid Config File, using default values.")
            GRIDSIZE = 10
            SIMULATION_SPEED = 12
            WIDTH, HEIGHT = 500, 500
else:
    print("Config File not found, using default values. You can create a config.json file to change the values.")
    GRIDSIZE = 10
    SIMULATION_SPEED = 12
    WIDTH, HEIGHT = 500, 500

    print(f"Grid Size: {GRIDSIZE}x{GRIDSIZE}")
    print(f"Simulation Speed: {SIMULATION_SPEED} FPS")
    print(f"Window Size: {WIDTH}x{HEIGHT}")

print(Fore.YELLOW)
time.sleep(0.5)

pattern = [[0 for i in range(GRIDSIZE)] for j in range(GRIDSIZE)]

pattern_history = []
generation = 0

def is_pattern_empty():
    for i in range(0, GRIDSIZE):
        for j in range(0, GRIDSIZE):
            if pattern[i][j] == 1:
                return False
    return True

def draw_text():
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT, WIDTH, 100))

    generation_text = font.render(f"Generation: {generation}", True, (0, 135, 255))
    generation_rect = generation_text.get_rect(center=(WIDTH // 2, HEIGHT + 35))
    screen.blit(generation_text, generation_rect)

    text = font.render("Conway's Game of Life", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 65))
    screen.blit(text, text_rect)

def draw_grid():
    for x in range(0, GRIDSIZE):
        for y in range(0, GRIDSIZE):
            if pattern[x][y] == 1:
                pygame.draw.rect(screen, (255, 255, 255), (x * WIDTH // GRIDSIZE, y * HEIGHT // GRIDSIZE, WIDTH // GRIDSIZE, HEIGHT // GRIDSIZE))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x * WIDTH // GRIDSIZE, y * HEIGHT // GRIDSIZE, WIDTH // GRIDSIZE, HEIGHT // GRIDSIZE))
    for x in range(0, GRIDSIZE):
        pygame.draw.line(screen, (255, 255, 255), (x * WIDTH // GRIDSIZE, 0), (x * WIDTH // GRIDSIZE, HEIGHT))
        pygame.draw.line(screen, (255, 255, 255), (0, x * HEIGHT // GRIDSIZE), (WIDTH, x * HEIGHT // GRIDSIZE))
    pygame.draw.line(screen, (255, 255, 255), (0, HEIGHT), (WIDTH, HEIGHT))

def count_neighbours(x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if x + i < 0 or x + i >= GRIDSIZE or y + j < 0 or y + j >= GRIDSIZE:
                continue
            if pattern[x + i][y + j] == 1:
                count += 1
    return count

def update():
    new_pattern = [[0 for i in range(GRIDSIZE)] for j in range(GRIDSIZE)]
    for x in range(0, GRIDSIZE):
        for y in range(0, GRIDSIZE):
            neighbours = count_neighbours(x, y)
            if pattern[x][y] == 1:
                if neighbours < 2:
                    new_pattern[x][y] = 0
                elif neighbours == 2 or neighbours == 3:
                    new_pattern[x][y] = 1
                else:
                    new_pattern[x][y] = 0
            else:
                if neighbours == 3:
                    new_pattern[x][y] = 1
    return new_pattern

def randomize():
    for i in range(0, GRIDSIZE):
        for j in range(0, GRIDSIZE):
            pattern[i][j] = random.choice([0, 1])

def auto_run():
    global generation, pattern
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return

        pattern = update()
        generation += 1
        pattern_history.append(pattern)

        draw_text()
        draw_grid()
        pygame.display.flip()
        clock.tick(SIMULATION_SPEED)

        if is_pattern_empty():
            print("Grid Empty, Stopping Simulation")
            break

        if pattern in pattern_history[-4:]:
            print("Grid Repeated, Stopping Simulation")
            break

pygame.init()
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = x // (WIDTH // GRIDSIZE)
            y = y // (HEIGHT // GRIDSIZE)
            try:
                pattern[x][y] = 1 if pattern[x][y] == 0 else 0
            except:
                pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pattern = update()
                generation += 1
                pattern_history.append(pattern)
            if event.key == pygame.K_LEFT:
                if generation > 0:
                    generation -= 1
                    pattern = pattern_history.pop()
            if event.key == pygame.K_r:
                pattern = [[0 for i in range(GRIDSIZE)] for j in range(GRIDSIZE)]
                generation = 0
                pattern_history = []
            if event.key == pygame.K_e:
                randomize()
            if event.key == pygame.K_s:
                auto_run()

    draw_text()
    draw_grid()
    pygame.display.flip()
    clock.tick(15)
