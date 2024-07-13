#960 1472
from sprites import *
from config import *
import pygame
class Weapns(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self._layer = weapon_layer
        self.groups = self.game.all_sprites, self.game.weapons
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x*tilesize
        self.y = y*tilesize

        self.width = tilesize
        self.height = tilesize
        #brickwall
        self.image = self.game.terrain_spritesheet.get_image(960,1472,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
