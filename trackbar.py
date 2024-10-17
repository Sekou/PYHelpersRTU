#2024, S. Diane, trackbar class for pygame

import pygame
import sys

class Trackbar:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.is_dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        knob_pos = int((self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width)
        abs_pos = (self.rect.x + knob_pos, self.rect.y + self.rect.height // 2)
        pygame.draw.circle(surface, (0, 0, 255), abs_pos, self.rect.height // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.update_value(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.update_value(event.pos)

    def update_value(self, mouse_pos):
        relative_x = mouse_pos[0] - self.rect.x
        if 0 <= relative_x <= self.rect.width:
            self.value = int(self.min_value + (relative_x / self.rect.width) * (self.max_value - self.min_value))
