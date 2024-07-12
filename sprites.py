from config import *
import pygame
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self._layer = blocks_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x*tilesize
        self.y = y*tilesize

        self.width = tilesize
        self.height = tilesize
        #brickwall
        self.image = self.game.terrain_spritesheet.get_image(320,128,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
       self.game = game
       self._layer = ground_layer
       self.groups = self.game.all_sprites
       pygame.sprite.Sprite.__init__(self, self.groups)
       
       self.x = x*tilesize
       self.y = y*tilesize

       self.width = tilesize
       self.height = tilesize
       #grass
       self.image = self.game.terrain_spritesheet.get_image(608,288,self.width,self.height)
       self.rect = self.image.get_rect()
       self.rect.x = self.x
       self.rect.y = self.y

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x*tilesize
        self.y = y*tilesize

        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        # x:0 y:2049

        #Player.sprite
        self.image = self.game.terrain_spritesheet.get_image(896,1920,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = 'right'

    def move(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            self.x_change = self.x_change - player_steps
            self.direction = 'left'
        elif pressed[pygame.K_RIGHT]:
            self.x_change = self.x_change + player_steps
            self.direction = 'right'
        elif pressed[pygame.K_UP]:
            self.y_change = self.y_change - player_steps
            self.direction = 'up'
        elif pressed[pygame.K_DOWN]:
            self.y_change = self.y_change + player_steps
            self.direction = 'down'

    def update(self):
        self.move()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        self.collide_block()
        self.collide_enemy()
        self.x_change = 0
        self.y_change = 0


    def collide_block(self):
        pressed = pygame.key.get_pressed()
        collide = pygame.sprite.spritecollide(self, self.game.blocks, False, pygame.sprite.collide_rect_ratio(0.85))

        if collide:
            self.game.collided_block = True
            if pressed[pygame.K_LEFT]:
                self.rect.x += player_steps
            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= player_steps
            elif pressed[pygame.K_UP]:
                self.rect.y += player_steps
            elif pressed[pygame.K_DOWN]:
                self.rect.y -= player_steps
        else:
            self.game.collided_block = False


    def collide_enemy(self):
        pressed = pygame.key.get_pressed()
        collide = pygame.sprite.spritecollide(self, self.game.enemies, False, pygame.sprite.collide_rect_ratio(0.85))
        
        if collide:
            self.game.collided_enemy = True
            if pressed[pygame.K_LEFT]:
                self.rect.x += player_steps
            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= player_steps
            elif pressed[pygame.K_UP]:
                self.rect.y += player_steps
            elif pressed[pygame.K_DOWN]:
                self.rect.y -= player_steps
        else:
            self.game.collided_enemy = False



        

#OGRE
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x*tilesize
        self.y = y*tilesize

        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        # x:0 y:2049

        #ENEMY
        self.image = self.game.terrain_spritesheet.get_image(256,1888,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.direction = random.choice(['left','right','up','down'])
        self.steps = random.choice([30,40,50,60])
        self.current_steps = 0

        self.state = 'moving'
        self.stall_steps = 80

    def move(self):
            
        if self.state == 'moving':
            if self.direction == 'left':
                self.x_change = self.x_change - enemy_steps
                self.current_steps += 1
            elif self.direction == 'right':
                self.x_change = self.x_change + enemy_steps
                self.current_steps += 1
            elif self.direction == 'up':
                self.y_change = self.y_change - enemy_steps
                self.current_steps += 1
            elif self.direction == 'down':
                self.y_change = self.y_change + enemy_steps
                self.current_steps += 1

        elif self.state == 'stalling':
            self.current_steps += 1
            if self.current_steps == self.stall_steps:
                self.state = 'moving'
                self.current_steps = 0
            


    def update(self):
        self.move()

        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change

        self.x_change = 0
        self.y_change = 0

        if self.current_steps == self.steps:
            if self.state != 'stalling':
                self.current_steps = 0
            self.direction = random.choice(['left','right','up','down'])
            self.state = 'stalling'
        
        self.collide_block()
    
    def collide_block(self):

        collide_block = pygame.sprite.spritecollide(self, self.game.blocks, False)

        if collide_block:
            if self.direction == 'left':
                self.rect.x += enemy_steps
                self.direction = 'right'
            elif self.direction == 'right':
                self.rect.x -= enemy_steps
                self.direction = 'left'
            elif self.direction == 'up':
                self.rect.y += enemy_steps
                self.direction = 'down'
            elif self.direction == 'down':
                self.rect.y -= enemy_steps
                self.direction = 'up'
                 






        


