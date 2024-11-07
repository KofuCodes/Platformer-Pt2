import pygame
from tiles import AnimatedTile
from random import randint
import math

class Enemy(AnimatedTile):
    def __init__(self,pos,sizex,sizey,sett):
        super().__init__(pos,sizex, sizey,'./graphics/enemy', sett)
        self.deathSound = pygame.mixer.Sound("./audio/sfx/enemyKill.wav")
        self.scoreUp = pygame.mixer.Sound("./audio/sfx/pickupCoin.wav")
        self.rect.y += (sizex * sett.tile_size_mult) - self.image.get_size()[1]
        self.floor = self.rect.y
        self.speed = 0.1
        self.sett = sett

    def move(self):
        if self.frame_index > 1:
            self.rect.x += 2 * math.copysign(1, self.speed)
        else:
            self.rect.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)
        
    def reverse(self):
        self.speed *= -1

    def collision(self, player):
        if self.rect.colliderect(player.rect):
            if player.is_attacking:
                self.deathSound.play()
                self.scoreUp.play()
                self.kill()
            else:
                # Player collides with the enemy from the side or below
                if not self.sett.invincible and self.sett.health > 0:
                    player.hitSound.play()  # Play the hit sound
                    self.sett.health -= 1  # Decrease health by 1
                    self.sett.invincible = True  # Set invincible to True
                    self.sett.invincibility_start_time = pygame.time.get_ticks()  # Record the start time
                    if self.sett.health <= 0:
                        self.sett.player_dead = True  # Player dies if health is 0
                        self.sett.health = 0  # Ensure health does not go negative

    def update(self,x_shift,y_shift,player):
        self.floor += y_shift
        self.rect.x += x_shift
        self.rect.y += y_shift
        self.animate()
        self.move()
        self.reverse_image()
        self.collision(player)