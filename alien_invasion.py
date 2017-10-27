
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # initialize game and create a screen objection
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # create an instance of storing statistics for game and scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # create a ship
    ship = Ship(ai_settings, screen)
    # create a group for storing bullet and alien
    bullets = Group()
    aliens = Group()

    # create a group of alien
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # create button "play"
    play_button = Button(ai_settings, screen, "play")

    # begin circle of game
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button,
                        ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                             play_button)

run_game()
