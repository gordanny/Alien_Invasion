import pygame

class Settings():
    '''A class to store all settings in Alien Invasion.'''

    def __init__(self):
        '''Initialize the game's settings.'''
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 40)
        self.bg = pygame.image.load('images\BG.jpg')

        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (243, 152, 122)
        self.bullets_allowed = 3

        # Ship settings.
        self.ships_limit = 3

        # Aliens settings.
        self.fleet_drop_speed = 10

        # How quickly the game speeds up.
        self.speedup_scale = 1.3
        self.scoreup_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game.'''
        self.bullet_speed = 5
        self.ship_speed = 3
        self.alien_speed = 3
        self.alien_points = 50

        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1


    def increase_speed(self):
        '''Increase game speed settings.'''
        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.scoreup_scale)
