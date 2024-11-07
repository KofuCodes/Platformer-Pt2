import pygame.sprite

from decoration import Sky
from particles import ParticleEffect
from player import Player
from settings import *
from support import import_csv_layout, import_cut_graphics
from tiles import EndPoint, StaticTile, Tile
from enemy import Enemy


class Level:
    def __init__(self, level_data, surface, sett):
        self.old_score = sett.score
        self.constraint_sprites = None
        self.player_sprite = None
        self.player_spawn = None
        self.enemy_sprites = None

        self.sett = sett
        self.next_level = level_data['next']
        self.collision_sprites = pygame.sprite.Group()

        terrain_layout, height = import_csv_layout(level_data['map']['terrain'])
        self.height = height
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        self.display_surface = surface
        self.total_world_shift = 0
        self.total_y_shift = 0
        self.world_shift = 0
        self.y_shift = 0
        self.current_x = 0

        player_layout, height = import_csv_layout(level_data['map']['player_spawn'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        '''
        grass_layout, height = import_csv_layout(level_data['map']['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')

        crate_layout, height = import_csv_layout(level_data['map']['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout,'crates')

        coin_layout, height = import_csv_layout(level_data['map']['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')

        fg_palm_layout, height = import_csv_layout(level_data['map']['fg_palms'])
        self.fg_palms_sprites = self.create_tile_group(fg_palm_layout,'fg_palms')

        bg_palm_layout, height = import_csv_layout(level_data['map']['bg_palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palm_layout,'bg_palms')

        enemy_layout, height = import_csv_layout(level_data['map']['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

        constraint_layout, height = import_csv_layout(level_data['map']['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')
        '''

        decoration_layout, height = import_csv_layout(level_data['map']['decoration'])
        self.decoration_sprites = self.create_tile_group(decoration_layout, 'decoration')

        platform_layout, height = import_csv_layout(level_data['map']['platform'])
        self.platform_sprites = self.create_tile_group(platform_layout, 'platform')

        big_tree_layout, height = import_csv_layout(level_data['map']['big_tree'])
        self.big_tree_sprites = self.create_tile_group(big_tree_layout, 'big_tree')

        small_tree_layout, height = import_csv_layout(level_data['map']['small_tree'])
        self.small_tree_sprites = self.create_tile_group(small_tree_layout, 'small_tree')

        enemy_layout, height = import_csv_layout(level_data['map']['enemy_setup'])
        self.enemy_sprites, self.constraint_sprites = self.create_tile_group(enemy_layout, "enemy")

        orb_layout, height = import_csv_layout(level_data['map']['orbs'])
        self.big_orb_sprites, self.small_orb_sprites = self.create_tile_group(orb_layout, "orb")

        self.sky = Sky(8, self.height * sett.tile_size * sett.tile_size_mult, self.sett)
        # self.water = Water(self.sett.screen_height - 40,len(terrain_layout[0]) * self.sett.tile_size,self.sett)
        # self.clouds = Clouds(400,len(terrain_layout[0]) * self.sett.tile_size,30,self.sett) self.void = Void(
        # self.sett.screen_height - 64,len(terrain_layout[0]) * self.sett.tile_size * self.sett.tile_size_mult, self.sett)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        enemy_sprites = pygame.sprite.Group()
        constraint_sprites = pygame.sprite.Group()
        small_orb_sprites = pygame.sprite.Group()
        big_orb_sprites = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != "-1":
                    x = col_index * self.sett.tile_size * self.sett.tile_size_mult
                    y = ((row_index - len(
                        layout)) * self.sett.tile_size * self.sett.tile_size_mult) + self.sett.screen_height

                    '''
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics("./graphics/terrain/terrain_tiles.png",self.sett.tile_size)
                        tile_surface = terrain_tile_list[int(col)]
                        sprite = StaticTile((x,y),self.sett.tile_size,tile_surface)
                        self.collision_sprites.add(sprite)
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('./graphics/decoration/grass/grass.png',self.sett.tile_size)
                        tile_surface = grass_tile_list[int(col)]
                        sprite = StaticTile((x,y),self.sett.tile_size,tile_surface)
                    if type == 'crates':
                        sprite = Crate((x,y),self.sett.tile_size)
                        self.collision_sprites.add(sprite)
                    if type == 'coins':
                        if col == "0": sprite = Coin((x,y),self.sett.tile_size,"./graphics/coins/gold",self.sett)
                        if col == "1": sprite = Coin((x,y),self.sett.tile_size,"./graphics/coins/silver",self.sett)
                    if type == 'fg_palms':
                        if col == '0': sprite = Palm((x,y),self.sett.tile_size,'./graphics/terrain/palm_small',38)
                        if col == '1': sprite = Palm((x,y),self.sett.tile_size,'./graphics/terrain/palm_large',64)
                        self.collision_sprites.add(sprite)
                    if type == 'bg_palms':
                        sprite = Palm((x,y),self.sett.tile_size,'./graphics/terrain/palm_bg',64)
                    if type == 'enemies':
                        sprite = Enemy((x,y),self.sett.tile_size,self.sett)
                    if type == 'constraint':
                        sprite = Tile((x,y),self.sett.tile_size)
                    '''
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics("./graphics/terrain.png", self.sett.tile_size)
                        tile_surface = terrain_tile_list[int(col)]
                        sprite = StaticTile((x, y), self.sett.tile_size, tile_surface, self.sett)
                        self.collision_sprites.add(sprite)
                    if type == 'platform':
                        platform_tile_list = import_cut_graphics("./graphics/platform.png", self.sett.tile_size)
                        tile_surface = platform_tile_list[int(col)]
                        sprite = StaticTile((x, y), self.sett.tile_size, tile_surface, self.sett)
                        self.collision_sprites.add(sprite)
                    if type == 'decoration':
                        decoration_tile_list = import_cut_graphics("./graphics/decoration.png", self.sett.tile_size)
                        tile_surface = decoration_tile_list[int(col)]
                        sprite = StaticTile((x, y), self.sett.tile_size, tile_surface, self.sett)
                        # self.collision_sprites.add(sprite)
                    if type == 'big_tree':
                        big_tree_tile_list = import_cut_graphics("./graphics/big_tree.png", self.sett.tile_size)
                        tile_surface = big_tree_tile_list[int(col)]
                        sprite = StaticTile((x, y), self.sett.tile_size, tile_surface, self.sett)
                        # self.collision_sprites.add(sprite)
                    if type == 'small_tree':
                        small_tree_tile_list = import_cut_graphics("./graphics/small_tree.png", self.sett.tile_size)
                        tile_surface = small_tree_tile_list[int(col)]
                        sprite = StaticTile((x, y), self.sett.tile_size, tile_surface, self.sett)
                        # self.collision_sprites.add(sprite)
                    if type == 'enemy':
                        if col == "0":
                            sprite = Enemy((x, y), 16, 9, self.sett)
                            enemy_sprites.add(sprite)
                        elif col == "1":
                            #sprite = Tile((x,y), self.sett.tile_size)
                            enemy_tile_list = import_cut_graphics("./graphics/enemy_setup.png", self.sett.tile_size)
                            tile_surface = enemy_tile_list[int(col)]
                            sprite = StaticTile((x, y), self.sett.tile_size, tile_surface, self.sett)
                            constraint_sprites.add(sprite)
                    if type == 'orb':
                        if col == "0":
                            orb_tile_list = import_cut_graphics("./graphics/orbs.png", 6)
                            tile_surface = orb_tile_list[int(col)]
                            sprite = StaticTile((x + 20, y + 20), 6, tile_surface, self.sett)
                            self.collision_sprites.add(sprite)
                            small_orb_sprites.add(sprite)
                        elif col == "1":
                            orb_tile_list = import_cut_graphics("./graphics/orbs.png", 6)
                            tile_surface = orb_tile_list[int(col)]
                            sprite = StaticTile((x + 20, y + 20), 6, tile_surface, self.sett)
                            self.collision_sprites.add(sprite)
                            big_orb_sprites.add(sprite)

                    if type != 'enemy' and type != 'orb':
                        sprite_group.add(sprite)

        if len(sprite_group) == 0 and type == 'enemy':
            return enemy_sprites, constraint_sprites
        elif type == 'orb':
            return big_orb_sprites, small_orb_sprites
        else:
            return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * self.sett.tile_size * self.sett.tile_size_mult
                y = ((row_index - len(
                    layout)) * self.sett.tile_size * self.sett.tile_size_mult) + self.sett.screen_height
                if col == "0":
                    self.player_spawn = (x, y)
                    self.player_sprite = Player((x, y), self.display_surface, self.create_jump_particles, self.sett)
                    self.player_sprite.rect = self.player_sprite.image.get_rect(center=self.player_spawn)
                    self.player.add(self.player_sprite)
                if col == '1':
                    goal_surface = pygame.image.load('./graphics/goal.png').convert_alpha()
                    sprite = EndPoint((x, y), self.sett.tile_size, goal_surface, self.sett)
                    sprite.rect = sprite.image.get_rect(
                        center=(x + int(self.sett.tile_size / 2), y + int(self.sett.tile_size / 2)))
                    self.goal.add(sprite)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(-10, 5)
        else:
            pos += pygame.math.Vector2(-10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(-10, 15)
            else:
                offset = pygame.math.Vector2(10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < self.sett.screen_width / 4 and direction_x < 0:
            self.world_shift = 8 * -self.player.sprite.direction.x
            player.speed = 0
        elif player_x > (self.sett.screen_width / 4) * 3 and direction_x > 0:
            self.world_shift = 8 * -self.player.sprite.direction.x
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

        self.total_world_shift += self.world_shift

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y < self.sett.screen_height / 5 and direction_y < 0:
            self.y_shift = -player.direction.y
            player.y_speed = 0
        elif player_y > (self.sett.screen_height / 3) * 2 and direction_y > 0:
            self.y_shift = -player.direction.y
            player.y_speed = 0
        else:
            self.y_shift = 0
            player.y_speed = 1

        if (self.total_y_shift + self.y_shift) >= 0:
            self.total_y_shift += self.y_shift
        else:
            player.y_speed = 1
            self.y_shift = -self.total_y_shift
            self.total_y_shift = 0

    def horizontal_movement_collision(self):
        player = self.player.sprite

        prevRect = player.rect.x

        player.rect.x += player.direction.x * player.speed

        difference = 32 + (player.direction.x ** 2)

        for sprite in self.collision_sprites.sprites():
            # if self.platform_sprites.has(sprite):
            #    return

            if sprite.rect.colliderect(player.rect):
                '''player.rect.x = prevRect

                if player.direction.x < 0:
                    player.on_left = True
                elif player.direction.x > 0:
                    player.on_right = True

                player.direction.x = 0'''

                if self.big_orb_sprites.has(sprite):
                    sprite.kill()
                    self.sett.score += 2
                    return
                if self.small_orb_sprites.has(sprite):
                    sprite.kill()
                    self.sett.score += 1
                    return

                if player.direction.x < 0 and (
                        sprite.rect.right + difference > player.rect.left > sprite.rect.right - difference):
                    # if self.fg_palms_sprites.has(sprite):
                    #    player.on_tree_left = True
                    # else:
                    #    player.on_tree_left = False
                    if self.platform_sprites.has(sprite):
                        return
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0 and (
                        sprite.rect.left + difference > player.rect.right > sprite.rect.left - difference):
                    # if self.fg_palms_sprites.has(sprite):
                    #    player.on_tree_right = True
                    # else:
                    #    player.on_tree_right = False
                    if self.platform_sprites.has(sprite):
                        return
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
            player.on_tree_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
            player.on_tree_right = False

        if player.on_left or player.on_right:
            player.gravity_mod = 0.25
        else:
            player.gravity_mod = 1

    def vertical_movement_collision(self):
        player = self.player.sprite

        prevRect = player.rect.y

        player.apply_gravity()

        difference = 32 + (player.direction.y ** 2)

        hitSprites = []
        direction = 1
        if player.direction.y < 0:
            direction = -1

        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                '''if self.platform_sprites.has(sprite) and player.direction.y < 0:
                    return
                
                player.rect.y = prevRect

                if player.direction.y > 0:
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.on_ceiling = True

                player.direction.y = 0'''

                if self.big_orb_sprites.has(sprite):
                    sprite.kill()
                    self.sett.score += 2
                    return
                if self.small_orb_sprites.has(sprite):
                    sprite.kill()
                    self.sett.score += 1
                    return

                if player.direction.y > 0 and (
                        sprite.rect.top + difference > player.rect.bottom > sprite.rect.top - difference):
                    if self.platform_sprites.has(sprite) and sprite.rect.top + 16 < player.rect.bottom:
                        return
                    player.rect.bottom = sprite.rect.top
                    hitSprites.append(sprite)
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0 and (
                        sprite.rect.bottom + difference > player.rect.top > sprite.rect.bottom - difference):
                    if self.platform_sprites.has(sprite):
                        return
                    player.rect.top = sprite.rect.bottom + 16
                    hitSprites.append(sprite)
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > player.gravity:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def get_death(self):
        if self.player_sprite.rect.midtop[1] >= self.sett.screen_height * 2 or self.sett.player_dead:
            pygame.mixer.Sound("./audio/sfx/playerDeath.wav").play()
            self.sett.player_dead = False
            self.sett.reload_level = True
            self.sett.score = self.old_score

            # self.world_shift = -self.total_world_shift
            # self.total_world_shift = 0
            # self.current_x = 0
            # self.y_shift = -self.total_y_shift
            # self.total_y_shift = 0
            # self.player_sprite.rect = self.player_sprite.image.get_rect(center=self.player_spawn)
            # self.player_sprite.facing_right = True

            return True
        else:
            return False

    def run(self):
        died = self.get_death()

        self.sky.draw(self.display_surface, self.total_world_shift, self.total_y_shift)
        # self.clouds.draw(self.display_surface,self.world_shift, self.y_shift)

        '''
        self.bg_palms_sprites.update(self.world_shift, self.y_shift)
        self.bg_palms_sprites.draw(self.display_surface)
        '''

        self.big_tree_sprites.update(self.world_shift, self.y_shift)
        self.big_tree_sprites.draw(self.display_surface)
        self.small_tree_sprites.update(self.world_shift, self.y_shift)
        self.small_tree_sprites.draw(self.display_surface)

        self.dust_sprite.update(self.world_shift, self.y_shift)
        self.dust_sprite.draw(self.display_surface)

        self.terrain_sprites.update(self.world_shift, self.y_shift)
        self.terrain_sprites.draw(self.display_surface)

        self.platform_sprites.update(self.world_shift, self.y_shift)
        self.platform_sprites.draw(self.display_surface)

        self.decoration_sprites.update(self.world_shift, self.y_shift)
        self.decoration_sprites.draw(self.display_surface)

        '''

        self.enemy_sprites.update(self.world_shift, self.y_shift, self.player.sprite)
        self.constraint_sprites.update(self.world_shift, self.y_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        self.crate_sprites.update(self.world_shift, self.y_shift)
        self.crate_sprites.draw(self.display_surface)

        self.grass_sprites.update(self.world_shift, self.y_shift)
        self.grass_sprites.draw(self.display_surface)

        self.coin_sprites.update(self.world_shift, self.y_shift, self.player.sprite)
        self.coin_sprites.draw(self.display_surface)

        self.fg_palms_sprites.update(self.world_shift, self.y_shift)
        self.fg_palms_sprites.draw(self.display_surface)
        '''

        self.enemy_sprites.update(self.world_shift, self.y_shift, self.player.sprite)
        self.constraint_sprites.update(self.world_shift, self.y_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        self.small_orb_sprites.update(self.world_shift, self.y_shift)
        self.small_orb_sprites.draw(self.display_surface)
        self.big_orb_sprites.update(self.world_shift, self.y_shift)
        self.big_orb_sprites.draw(self.display_surface)

        if not died:
            self.scroll_x()
            self.scroll_y()

        if self.goal.sprite.update(self.world_shift, self.y_shift, self.player.sprite):
            self.sett.score += 10
            self.sett.set_level(self.next_level)
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.goal.draw(self.display_surface)
        self.player.draw(self.display_surface)

        # self.water.draw(self.display_surface, self.world_shift, self.y_shift)
        # self.void.draw(self.display_surface, self.world_shift, self.y_shift)

        if died:
            self.scroll_x()
            self.scroll_y()
