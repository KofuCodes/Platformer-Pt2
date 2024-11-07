import pygame
from support import import_folder
import tkinter as tk
from special import Special


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, sett):
        super().__init__()
        self.dashSound = pygame.mixer.Sound("./audio/sfx/dash.wav")
        self.jumpSound = pygame.mixer.Sound("./audio/sfx/jump.wav")
        self.hitSound = pygame.mixer.Sound("./audio/sfx/hit.wav")
        self.attackSound = pygame.mixer.Sound("./audio/sfx/attack.wav")

        self.sett = sett

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

        # self.can_dash = True

        '''        if (not self.can_dash) and -1 <= self.direction.x <= 1:
            self.has_gravity = True

        if keys[pygame.K_LSHIFT] and self.can_dash and self.sett.charge['dash'] >= 120:
            self.can_dash = False
            self.has_gravity = False
            self.sett.charge['dash'] = 0
            if self.facing_right:
                self.direction.x = 3
            else:
                self.direction.x = -3

        if (not keys[pygame.K_LSHIFT]) and 1 >= self.direction.x >= -1:
            self.can_dash = True
            self.has_gravity = True'''

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
                self.is_attacking = False  # Reset attack status after animation completes

        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (22 * self.sett.tile_size_mult, 22 * self.sett.tile_size_mult))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # Update the rect position based on the new image
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
            self.attackSound.play()  # Play the attack sound
            # Update the attack hitbox position based on the player's facing direction
            if self.facing_right:
                self.attack_hitbox.topleft = self.rect.topright
            else:
                self.attack_hitbox.topright = self.rect.topleft


    def get_input(self):
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

        if keys[pygame.K_x]:  # Assuming 'X' is for attacking
            self.attack()

        if keys[pygame.K_0]:
            frame = tk.Tk()
            frame.title("TextBox Input")
            frame.geometry('100x50')

            frame.focus()

            inputtxt = tk.Text(frame,
                               height=1,
                               width=10)

            inputtxt.pack()

            inputtxt.focus()

            def keyup(e):
                if e.keycode == 13:
                    new_level()

            inputtxt.bind("<KeyRelease>", keyup)

            def new_level():
                inp = inputtxt.get(1.0, "end-1c")
                self.sett.set_level(inp.replace("\n", ""))
                frame.destroy()

            printButton = tk.Button(frame, text="Set Level", command=new_level)
            printButton.pack()

            frame.mainloop()

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