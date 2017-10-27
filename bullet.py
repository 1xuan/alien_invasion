import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """regulating bullets which the ship shot"""

    def __init__(self, ai_settings, screen, ship):
        """create a bullet at ship's location"""
        super(Bullet, self).__init__()
        self.screen = screen

        # create a bullet at (0,0) and then set accurate location
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """move up bullet"""
        # update number of bullet's location
        self.y -= self.speed_factor
        # update location of bullet's rect
        self.rect.y = self.y

    def draw_bullet(self):
        """draw bullet on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
