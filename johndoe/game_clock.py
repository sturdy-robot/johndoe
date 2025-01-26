import pygame


class GameClock:
    def __init__(self):
        self.total_time = 0
        self.paused = False
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.paused:
            self.total_time += current_time - self.last_update_time
        self.last_update_time = current_time

    def toggle_pause(self):
        self.paused = not self.paused
        self.update()

    def get_time(self):
        return self.total_time
