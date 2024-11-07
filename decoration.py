import pygame
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint
import math, random

class Sky:
    def __init__(self,horizon,map_height,sett):
        '''
        self.top = pygame.image.load('./graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('./graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('./graphics/decoration/sky/sky_middle.png').convert()
        self.horizon = horizon
        self.map_height = map_height
        self.sett = sett

        self.top = pygame.transform.scale(self.top,(self.sett.screen_width,self.sett.tile_size * self.sett.tile_size_mult))
        self.bottom = pygame.transform.scale(self.bottom,(self.sett.screen_width,self.sett.tile_size * self.sett.tile_size_mult))
        self.middle = pygame.transform.scale(self.middle,(self.sett.screen_width,self.sett.tile_size * self.sett.tile_size_mult))
        '''
        self.back0 = pygame.image.load('./graphics/background/0.png').convert_alpha()
        self.back1 = pygame.image.load('./graphics/background/1.png').convert_alpha()
        self.back2 = pygame.image.load('./graphics/background/2.png').convert_alpha()
        self.top = pygame.image.load('./graphics/background/top.png').convert_alpha()

        self.back0 = pygame.transform.scale_by(self.back0,sett.tile_size_mult)
        self.back1 = pygame.transform.scale_by(self.back1,sett.tile_size_mult)
        self.back2 = pygame.transform.scale_by(self.back2,sett.tile_size_mult)
        self.top = pygame.transform.scale_by(self.top,sett.tile_size_mult)

        self.height = map_height
        self.sett = sett

        self.top_count = math.ceil((self.height - (180 * self.sett.tile_size_mult)) / (58 * self.sett.tile_size_mult)) + 4
        self.offsets = []
        for i in range(self.top_count):
            self.offsets.append(math.ceil((random.random() * 800) - 400))

    def draw(self,surface,x_shift,y_shift):
        '''
        for row in range(self.map_height):
            y = row * self.sett.tile_size * self.sett.tile_size_mult
            if row < self.horizon:
                surface.blit(self.top,(0,y))
            elif row == self.horizon:
                surface.blit(self.middle,(0,y))
            else:
                surface.blit(self.bottom,(0,y))
        '''
        amount = 3
        back_shift = 0
        for i in range(amount):
            if x_shift > 0:
                back_shift = math.ceil(x_shift / (288 * self.sett.tile_size_mult))
            else:
                back_shift = math.floor(x_shift / (288 * self.sett.tile_size_mult))
            surface.blit(self.back0,((((math.floor(amount / 2) * -1) + i) * (288 * self.sett.tile_size_mult)) + x_shift - (back_shift * (288 * self.sett.tile_size_mult)),self.sett.screen_height - (122 * self.sett.tile_size_mult) + y_shift))
            surface.blit(self.back1,((((math.floor(amount / 2) * -1) + i) * (288 * self.sett.tile_size_mult)) + x_shift - (back_shift * (288 * self.sett.tile_size_mult)),self.sett.screen_height - (122 * self.sett.tile_size_mult) + y_shift))
            surface.blit(self.back2,((((math.floor(amount / 2) * -1) + i) * (288 * self.sett.tile_size_mult)) + x_shift - (back_shift * (288 * self.sett.tile_size_mult)),self.sett.screen_height - (122 * self.sett.tile_size_mult) + y_shift))
        for i in range(amount + 4):
            if x_shift > 0:
                back_shift = math.ceil(x_shift / (288 * self.sett.tile_size_mult))
            else:
                back_shift = math.floor(x_shift / (288 * self.sett.tile_size_mult))
            for n in range(self.top_count):
                surface.blit(self.top,((((math.floor((amount + 4) / 2) * -1) + i) * (288 * self.sett.tile_size_mult)) + x_shift - (back_shift * (288 * self.sett.tile_size_mult)) + self.offsets[n],self.sett.screen_height - (180 * self.sett.tile_size_mult) - (n * 58 * self.sett.tile_size_mult) + y_shift))


class Water:
    def __init__(self,top,level_width,sett):
        self.sett = sett
        water_start = -self.sett.screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + (self.sett.screen_width * 2)) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = (tile * water_tile_width) + water_start
            y = top
            sprite = AnimatedTile((x,y),water_tile_width,"./graphics/decoration/water")
            self.water_sprites.add(sprite)

    def draw(self,surface,x_shift,y_shift):
        self.water_sprites.update(x_shift,y_shift)
        self.water_sprites.draw(surface)

class Clouds:
    def __init__(self,horizon,level_width,cloud_number,sett):
        self.sett = sett
        cloud_surf_list = import_folder('./graphics/decoration/clouds')
        min_x = -self.sett.screen_width
        max_x = level_width + self.sett.screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x,max_x)
            y = randint(min_y,max_y)
            sprite = StaticTile((x,y),0,cloud,self.sett)
            self.cloud_sprites.add(sprite)

    def draw(self,surface,x_shift,y_shift):
        self.cloud_sprites.update(x_shift,y_shift)
        self.cloud_sprites.draw(surface)

class Void:
    def __init__(self,top,level_width,sett):
        self.sett = sett
        void_start = -self.sett.screen_width
        void_tile_width = 16
        tile_x_amount = int((level_width + (self.sett.screen_width * 2)) / void_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = (tile * void_tile_width) + void_start
            y = top
            sprite = StaticTile((x,y),void_tile_width,pygame.image.load("./graphics/void.png"),sett)
            self.water_sprites.add(sprite)

    def draw(self,surface,x_shift,y_shift):
        self.water_sprites.update(x_shift,y_shift)
        self.water_sprites.draw(surface)