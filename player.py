import pygame
from support import import_folder
from special import Special

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, sett):
        super().__init__()
        self.dashSound = pygame.mixer.Sound("./audio/sfx/dash.ogg")
        self.jumpSound = pygame.mixer.Sound("./audio/sfx/jump.ogg")
        self.hitSound = pygame.mixer.Sound("./audio/sfx/hit.ogg")
        self.attackSound = pygame.mixer.Sound("./audio/sfx/attack.ogg")

        self.sett = sett
        
        # Add text input state
        self.entering_level = False
        self.level_input = ""
        self.font = pygame.font.Font(None, 36)

        self.import_character_assets()

        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.image = pygame.transform.scale(self.image, (22 * sett.tile_size_mult, 22 * sett.tile_size_mult))
        self.rect = self.image.get_rect(topleft=pos)

        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.y_speed = 1
        self.gravity = 0.8
        self.gravity_mod = 1
        self.has_gravity = 1
        self.jump_speed = -16

        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.on_tree_left = False
        self.on_tree_right = False

        self.jumps = 2
        self.can_jump = True
        
        self.is_attacking = False
        self.attack_cooldown = 500  # milliseconds
        self.last_attack_time = 0
        self.attack_frame_index = 0
        self.attack_speed = 0.2
        self.attack_hitbox = pygame.Rect(0, 0, 100, 100)

        self.specials = []
        self.load_specials()

    def load_specials(self):
        def dashability(charge, max_charge, key, keys, can_use):
            self.dashSound.play()
            self.has_gravity = False
            self.sett.charge[charge] = 0
            if self.facing_right:
                self.direction.x = 3
            else:
                self.direction.x = -3

        def dashpre(charge, max_charge, key, keys, can_use):
            if (not can_use) and -1 <= self.direction.x <= 1:
                self.has_gravity = True
            return None

        def dashpost(charge, max_charge, key, keys, can_use):
            if (not keys[key]) and 1 >= self.direction.x >= -1:
                self.has_gravity = True
                return True
            return None

        self.specials.append(Special(dashability, dashpre, dashpost, 'dash', 120, pygame.K_c, self.sett))

    def handle_level_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.level_input:  # Only process if there's actual input
                    self.sett.set_level(self.level_input)
                self.entering_level = False
                self.level_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.level_input = self.level_input[:-1]
            elif event.unicode.isdigit() or event.unicode.isalpha():
                self.level_input += event.unicode

    def draw_level_input(self):
        if self.entering_level:
            # Create a background rect
            input_surface = self.font.render(self.level_input + "_", True, (255, 255, 255))
            input_rect = input_surface.get_rect(center=(self.display_surface.get_width() // 2, 
                                                      self.display_surface.get_height() // 2))
            
            # Draw background
            padding = 10
            bg_rect = pygame.Rect(input_rect.x - padding, 
                                input_rect.y - padding,
                                input_rect.width + (padding * 2), 
                                input_rect.height + (padding * 2))
            pygame.draw.rect(self.display_surface, (0, 0, 0), bg_rect)
            pygame.draw.rect(self.display_surface, (255, 255, 255), bg_rect, 2)
            
            # Draw text
            self.display_surface.blit(input_surface, input_rect)

    def import_character_assets(self):
        character_path = "./graphics/character/"
        self.animations = {"idle": [], "run": [], "jump": [], "fall": [], "attack": [], "hit": []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder("./graphics/character/dust_particles/run/")

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.status == 'attack':
                self.is_attacking = False

        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (22 * self.sett.tile_size_mult, 22 * self.sett.tile_size_mult))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        if self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def run_dust_animation(self):
        if self.status == "run" and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(-6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(20, 10)
                flipped_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_particle, pos)

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.is_attacking = True
            self.last_attack_time = current_time
            self.attackSound.play()
            if self.facing_right:
                self.attack_hitbox.topleft = self.rect.topright
            else:
                self.attack_hitbox.topright = self.rect.topleft

    def get_input(self):
        if self.entering_level:
            return
            
        keys = pygame.key.get_pressed()

        if self.direction.x > 0 and self.on_right:
            self.direction.x = 0
        elif self.direction.x < 0 and self.on_left:
            self.direction.x = 0

        if keys[pygame.K_RIGHT]:
            if self.direction.x == -1 or self.direction.x == 0:
                self.direction.x = 1
            elif self.direction.x < 1:
                self.direction.x += 0.1
            elif self.direction.x > 1:
                self.direction.x -= 0.1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            if self.direction.x == 1 or self.direction.x == 0:
                self.direction.x = -1
            elif self.direction.x > -1:
                self.direction.x -= 0.1
            elif self.direction.x < -1:
                self.direction.x += 0.1
            self.facing_right = False
        else:
            if self.direction.x >= -1 and self.direction.x <= 1:
                self.direction.x = 0
            elif self.direction.x < -1:
                self.direction.x += 0.1
            elif self.direction.x > 1:
                self.direction.x -= 0.1

        if self.on_ground or (self.on_left and not self.on_tree_left) or (self.on_right and not self.on_tree_right):
            self.jumps = 2

        if keys[pygame.K_z] and (
                self.on_ground or self.on_left or self.on_right or self.jumps > 0) and self.can_jump:
            if self.jumps > 0:
                self.can_jump = False
                self.jump()
                if self.on_left and not self.on_ground:
                    self.direction.x = 1.5
                if self.on_right and not self.on_ground:
                    self.direction.x = -1.5
                self.create_jump_particles(self.rect.midbottom)
                self.jumps -= 1

        if not keys[pygame.K_z]:
            self.can_jump = True

        if keys[pygame.K_x]:
            self.attack()

        if keys[pygame.K_0]:
            self.entering_level = True
            self.level_input = ""

    def get_status(self):
        if self.is_attacking:
            self.status = 'attack'
        elif self.sett.invincible:
            self.status = 'hit'
        elif self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity:
            self.status = 'fall'
        elif self.direction.x == 0:
            self.status = 'idle'
        else:
            self.status = 'run'

    def apply_gravity(self):
        if self.direction.y > self.gravity:
            self.direction.y += self.gravity * self.gravity_mod
        else:
            self.direction.y += self.gravity
        if self.has_gravity:
            self.rect.y += self.direction.y * self.y_speed
        else:
            self.direction.y = 0

    def jump(self):
        self.jumpSound.play()
        self.direction.y = self.jump_speed

    def update(self):
        for spec in self.specials:
            spec.update()
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.draw_level_input()