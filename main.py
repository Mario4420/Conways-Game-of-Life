#!/usr/bin/env python

import sys
import random
import pygame
pygame.init()

SCREEN_SIZE = 600
SCALE = 50
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

clock = pygame.time.Clock()
FPS = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Cell(pygame.Rect):

    def __init__(self, x, y, size, active):
        super().__init__(x, y, size, size)
        self.active = active
        self.active_neighbors = 0


CELL_SIZE = (SCREEN_SIZE // SCALE) - 1

PROBABILITY = 95


def create_grid(screen_size, scale, cell_size, probability):
    return [[Cell(x, y, CELL_SIZE,
            True if random.randrange(100) > probability else False)
            for x in range(0, SCREEN_SIZE, SCREEN_SIZE // SCALE)]
            for y in range(0, SCREEN_SIZE, SCREEN_SIZE // SCALE)]


def draw_grid(screen, grid, active_col, non_active_col):
    for row in grid:
        for cell in row:
            if cell.active:
                pygame.draw.rect(screen, active_col, cell)
            else:
                pygame.draw.rect(screen, non_active_col, cell)


def is_inbounds(y, x, grid_len):
    if y < 0 or y >= grid_len \
       or x < 0 or x >= grid_len:
        return False
    return True


def count_neighbors(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    if is_inbounds(y+i, x+j, len(grid)):
                        if grid[y+i][x+j].active:
                            cell.active_neighbors += 1


def change_grid_state(grid):
    for row in grid:
        for cell in row:
            if cell.active_neighbors < 2:
                cell.active = False

            elif cell.active_neighbors == 2 or cell.active_neighbors == 3 \
                    and cell.active:
                cell.active = True

            elif cell.active_neighbors > 3 and cell.active:
                cell.active = False

            elif cell.active_neighbors == 3 and not cell.active:
                cell.active = True

            else:
                cell.active = False

            cell.active_neighbors = 0


def main():
    grid = create_grid(SCREEN_SIZE, SCALE, CELL_SIZE, PROBABILITY)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

        screen.fill(BLACK)

        count_neighbors(grid)
        change_grid_state(grid)
        draw_grid(screen, grid, RED, WHITE)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
