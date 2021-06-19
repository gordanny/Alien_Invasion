import pygame
from pygame.sprite import Group

import game_function as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship

def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(ai_settings, "Play", screen)

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets and a group of aliens.
    aliens = Group()
    bullets = Group()
    ship = Ship(ai_settings, screen)

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, aliens, screen, ship)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, aliens, bullets, play_button, sb, screen, ship, stats)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, aliens, bullets, sb, screen, ship, stats)
            gf.update_aliens(ai_settings, aliens, bullets, sb, screen, ship, stats)

        gf.update_screen(ai_settings, aliens, bullets, play_button, sb, screen, ship, stats)

run_game()
