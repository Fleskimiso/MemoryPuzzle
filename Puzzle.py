import pygame

from Shapes import *


class Puzzle:
    def __init__(self, shape, color, x_pos, y_pos):
        self.width = 50
        self.height = 50
        self.shape = shape
        self.color = color
        self.x_position = x_pos
        self.y_position = y_pos
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.surface_orignal = self.surface.copy()
        self.draw_blank()

    def draw_figure(self):
        self.surface = self.surface_orignal.copy()
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, self.width, self.height), 1)
        if self.shape == Shapes.circle:
            pygame.draw.circle(self.surface, self.color.value, self.surface.get_rect().center, int(self.width / 2), 10)
        elif self.shape == Shapes.square:
            pygame.draw.polygon(self.surface, self.color.value, [
                (10, 10), (self.width - 10, 10), (self.width - 10, self.height - 10), (10, self.height - 10)
            ], 5)
        elif self.shape == Shapes.cross:
            pygame.draw.line(self.surface, self.color.value, (0, 0), (self.width, self.height))
            pygame.draw.line(self.surface, self.color.value, (self.width, 0), (0, self.height))
        elif self.shape == Shapes.elipse:
            pygame.draw.ellipse(self.surface, self.color.value, (0, 10, self.width, self.height - 2 * 10), 15)

    def draw_blank(self):
        self.surface = self.surface_orignal.copy()
        pygame.draw.rect(self.surface, (0, 0, 0, 255), ((0, 0), (self.width, self.height)), 1)
