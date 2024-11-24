import time
from asyncio import wait_for

import pygame
from config import WIDTH, HEIGHT, TITLE, BGCOLOR, FIELDSIZE, PANEL_HEIGHT

from map import Map

class Game:

    game = None

    def __init__(self):
        self.map = None
        self.playing = False
        self.misses = 0
        self.selected_island = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

    @staticmethod
    def start_game():
        if not Game.game:
            Game.game = Game()
            Game.game.map = Map()
            Game.game.map.initialize()
            Game.game.run()

    @staticmethod
    def get_selected():
        return Game.game.selected_island

    @staticmethod
    def get_solution():
        return Game.game.map.solution

    def run(self):
        self.playing = True
        while True:
            self.events()
            self.draw()
            self.draw_bottom_panel()

    def draw_bottom_panel(self):
        """Draw the panel at the bottom of the screen"""

        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, HEIGHT - PANEL_HEIGHT, WIDTH, PANEL_HEIGHT))
        pygame.draw.line(self.screen, (255, 255, 255), (0, HEIGHT - PANEL_HEIGHT),
                         (WIDTH, HEIGHT - PANEL_HEIGHT), 2)

        font = pygame.font.SysFont("Arial", 24)

        # Streak
        streak_text = font.render(f"Streak: {self.misses}", True, (255, 255, 255))
        streak_rect = streak_text.get_rect(topleft=(20, HEIGHT - PANEL_HEIGHT + 10))
        self.screen.blit(streak_text, streak_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.map.draw(self.screen)
        pygame.display.flip()

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if not self.playing: return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                mx //= FIELDSIZE
                my //= FIELDSIZE
                field = self.map.grid[my][mx]
                if field.height > 0:
                    self.selected_island = field.island_id
                    if self.selected_island == self.map.solution:
                        self.handle_win()
                    else:
                        self.handle_missed_guess()
                
                # ...

    def handle_win(self):
        self.playing = False

    def handle_missed_guess(self):
        self.misses += 1
        if self.misses == 3:
            self.playing = False
