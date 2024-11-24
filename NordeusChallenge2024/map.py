import math
from collections import deque
import pygame
from backend import *
from config import *
from island import Island

class Field:
    def __init__(self, height):
        self.height = height
        self.island_id = 0
        self.borders = 0
        self.effect_start_time = None

    def draw(self, i, j, screen):
        from game import Game
        color = LAND_COLORS[(self.height - 1) * len(LAND_COLORS) // 1000] if self.height > 0 else WATER_COLOR

        x, y = j * FIELDSIZE, i * FIELDSIZE
        rect = pygame.Rect(x, y, FIELDSIZE, FIELDSIZE)
        pygame.draw.rect(screen, color, rect)

        selected = Game.get_selected()

        if selected == self.island_id:
            # Pulsing effect
            border_color = SUCCESS_COLOR if selected == Game.get_solution() else WRONG_SELECTION_COLOR
            time = pygame.time.get_ticks()  # Get current time in milliseconds
            if self.effect_start_time is None:
                self.effect_start_time = pygame.time.get_ticks()

            seconds = (pygame.time.get_ticks() - self.effect_start_time) // 1000
            if not seconds:
                pulse = BORDER_WIDTH + abs(2 * math.sin(time * 0.005))
                bw = int(pulse)  # Adjust border width dynamically
            else:
                bw = BORDER_WIDTH

        else:
            self.effect_start_time = None
            border_color = BORDER_COLOR
            bw = BORDER_WIDTH

        if self.borders & TOP:  # Check if top border is set
            pygame.draw.line(screen, border_color, (x, y), (x + FIELDSIZE, y), bw)  # Top border
        if self.borders & RIGHT:  # Check if right border is set
            pygame.draw.line(screen, border_color, (x + FIELDSIZE - bw, y), (x + FIELDSIZE - bw, y + FIELDSIZE),bw)  # Right border
        if self.borders & BOTTOM:  # Check if bottom border is set
            pygame.draw.line(screen, border_color, (x, y + FIELDSIZE - bw), (x + FIELDSIZE, y + FIELDSIZE - bw), bw)  # Bottom border
        if self.borders & LEFT:  # Check if left border is set
            pygame.draw.line(screen, border_color, (x, y), (x, y + FIELDSIZE), bw)  # Left border
class Map:
    def __init__(self):
        self.grid = get_new_map()
        self.solution = 0

    def __str__(self):
        for row in self.grid:
            for cell in row:
                print(cell[0], end=' ')
            print()

    @staticmethod
    def __valid_index(i, j):
        return 0 <= i < N and 0 <= j < M

    def __get_neighbors(self, row, col):
        neighbors = []
        directions = [[1,0],[0,1],[-1,0],[0,-1]] # B, R, T, L
        for d in range(len(directions)):
            dr, dc = directions[d]
            i, j = row + dr, col + dc
            if self.__valid_index(i,j):
                if self.grid[i][j].height == 0:
                    self.grid[row][col].borders |= 1 << d
                    continue
                neighbors.append((i,j))
        return neighbors

    def __landNotVisited(self, i, j):
        return self.grid[i][j].height > 0 and self.grid[i][j].island_id == 0

    def initialize(self):
        # DFS or BFS algorithm
        # - identify island
        # - mark island_id in field[1]
        # - mark the solution island

        # if field is land:
        # field[1] > 0 <=> visited

        for i in range(N):
            for j in range(M):
                if self.__landNotVisited(i, j):
                    island = Island()
                    island.mark_field(self.grid[i][j])
                    self.__explore_island(i, j, island)

        self.find_solution()

    def __explore_island(self, i, j, island):
        stack = deque()
        stack.append((i,j))

        while stack:
            r, c = stack.pop()
            neighbors = self.__get_neighbors(r, c)
            for i, j in neighbors:
                if self.__landNotVisited(i, j):
                    island.mark_field(self.grid[i][j])
                    stack.append((i, j))

    def find_solution(self):
        max_height = 0
        for island_id, island in Island.islands.items():
            if island.average_height() > max_height:
                max_height = island.average_height()
                self.solution = island_id

    def draw(self, screen):
        for i in range(M):
            for j in range(N):
                self.grid[i][j].draw(i, j, screen)
