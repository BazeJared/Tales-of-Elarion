from config import *
import sys
import pygame
from sprites import * 
class SpriteSheet:
    def __init__(self,path):
        self.spritesheet = pygame.image.load(path).convert_alpha()

    def get_image(self,x,y,width,height):
        sprite = pygame.Surface([width,height], pygame.SRCALPHA)
        sprite.blit(self.spritesheet,(0,0),(x,y,width,height))
        return sprite
    
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.terrain_spritesheet = SpriteSheet('assets/sprites.png')
        self.running = True
        self.collided = False

    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, col in enumerate(row):
                Ground(self,j,i,)
                if col == 'B':
                    Block(self,j,i)
                if col == 'P':
                    Player(self,j,i)
                if col == 'E':
                    Enemy(self,j,i)
                #Ogre

    def create(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.create_tilemap()
        
    def update(self):
        self.all_sprites.update()
        
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
    def draw(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        self.clock.tick(fps)
        pygame.display.update()

    def camera(self):
        if self.collided == False:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_LEFT]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.x += player_steps
            elif pressed[pygame.K_RIGHT]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.x -= player_steps
            elif pressed[pygame.K_UP]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.y += player_steps
            elif pressed[pygame.K_DOWN]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.y -= player_steps

    def main(self):
        while self.running:
            self.event()
            self.camera()
            self.update()
            self.draw()

pygame.init()
game = Game()
game.create()

while game.running:
    game.main()

pygame.quit()
sys.exit()

#TO do : Player, enemy, water: animation