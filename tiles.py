import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift


class StaticTile(Tile):
    def __init__(self, pos, size, surface, sett):
        size *= sett.tile_size_mult
        super().__init__(pos, size)
        self.image = pygame.transform.scale(surface, (size, size))

class Crate(StaticTile):
    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.image.load("./graphics/terrain/crate.png").convert_alpha())
        offset_y = pos[1] + size
        self.rect = self.image.get_rect(bottomleft=(pos[0], offset_y))

class AnimatedTile(Tile):
    def __init__(self, pos, sizex, sizey, path, sett):
        sizex *= sett.tile_size_mult
        sizey *= sett.tile_size_mult
        super().__init__(pos, sizex)
        self.sizex = sizex
        self.sizey = sizey
        self.sett = sett
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = pygame.transform.scale(self.frames[self.frame_index], (sizex, sizey))

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (self.sizex, self.sizey))

    def update(self, x_shift, y_shift):
        self.animate()
        self.rect.x += x_shift
        self.rect.y += y_shift


class Coin(AnimatedTile):
    def __init__(self, pos, size, path, sett):
        super().__init__(pos, size, path)
        self.sett = sett
        self.type = path.split("/")
        self.type = self.type[len(self.type) - 1]
        center_x = pos[0] + int(size / 2)
        center_y = pos[1] + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))

    def collision(self, player):
        if self.rect.colliderect(player.rect):
            if self.type == "silver":
                self.sett.score += 1
            elif self.type == "gold":
                self.sett.score += 2
            self.kill()

    def update(self, x_shift, y_shift, player):
        self.animate()
        self.collision(player)
        self.rect.x += x_shift
        self.rect.y += y_shift


class Palm(AnimatedTile):
    def __init__(self, pos, size, path, offset):
        super().__init__(pos, size, path)
        offset_y = pos[1] - offset
        self.rect.topleft = (pos[0], offset_y)


class EndPoint(StaticTile):
    def __init__(self, pos, size, surface, sett):
        super().__init__(pos, size, surface, sett)
        self.sett = sett

    def collision(self, player):
        return self.rect.colliderect(player.rect)

    def update(self, x_shift, y_shift, player):
        self.rect.x += x_shift
        self.rect.y += y_shift
        collided = self.collision(player)
        return collided
