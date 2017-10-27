import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ represent one alien"""
    def __init__(self, ai_settings, screen):
        """initialize Alien and set location of begin"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load picture of alien ,setting its rect
        self.image = pygame.image.load(r'F:\STUDY\python\alien_invasion\images'
                                       r'\alien.png')
        self.rect = self.image.get_rect()

        # every alien at top left coner at first
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store accurate location
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """move alien right or left"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """return True if alien in the margin"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


