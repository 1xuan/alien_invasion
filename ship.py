import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        """initialize ship and set the location of begining"""
        self.screen = screen
        self.ai_settings = ai_settings

        # load ship's image and get the information of rect
        self.image = pygame.image.load(r'F:\STUDY\python\alien_invasion\images'
                                       r'\ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # put every ship the bottom of screen in center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store float
        self.center = float(self.rect.centerx)

        # moving logo
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # update object of rect
        self.rect.centerx = self.center

    def blitme(self):
        """draw ship in the point"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """put ship in center"""
        self.center = self.screen_rect.centerx
