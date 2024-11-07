from game_data import levels
import pygame


class Settings:
    def __init__(self) -> None:
        self.rectangle = None
        self.vert_tile_num = 11
        self.tile_size = 16
        self.tile_size_mult = 4
        self.screen_width = 1152
        self.screen_height = self.vert_tile_num * self.tile_size * self.tile_size_mult
        self.level_name = "level0"
        self.reload_level = False
        self.screen = None
        self.player_dead = False
        self.score = 0
        self.health = 5
        self.invincible = False
        self.invincibility_duration = 2000  # Duration in milliseconds
        self.invincibility_start_time = 0
        self.charge = {
            "dash": 120
        }

    def set_level(self, name):
        if levels.__contains__(name):
            self.level_name = name
