import pygame
import os
import random


class Player:
    def __init__(self, screen):
        # stats
        self.hp = 100
        self.speed = 5
        self.width, self.height = 100, 100
        self.screen = screen
        self.start_pos = (self.screen.get_width()/2 -
                          self.width/2, self.screen.get_height()/2)

        # sprite and body
        self.very_damaged_sprite = pygame.transform.scale(pygame.image.load(
            os.path.join("assets", "player", "very_damaged.png")), (self.width, self.height))
        self.damaged_sprite = pygame.transform.scale(pygame.image.load(
            os.path.join("assets", "player", "damaged.png")), (self.width, self.height))
        self.base_sprite = pygame.transform.scale(pygame.image.load(
            os.path.join("assets", "player", "normal.png")), (self.width, self.height))
        self.engine_sprite = pygame.transform.scale(pygame.image.load(
            os.path.join("assets", "player", "engine.png")), (self.width, self.height))

        self.mask = pygame.mask.from_surface(self.base_sprite)
        self.rect = pygame.Rect(
            self.start_pos[0], self.start_pos[1], self.width, self.height)

        self.shoot_sound = [pygame.mixer.Sound(
            os.path.join('assets', 'audio', 'sfx_laser1.ogg')),
            pygame.mixer.Sound(
            os.path.join('assets', 'audio', 'sfx_laser2.ogg'))]
        self.hit_sound = pygame.mixer.Sound(
            os.path.join('assets', 'audio', 'sfx_hurt.wav'))

        self.bullets = []

    def update(self, ):
        self.input()

        for b in self.bullets:
            b.update()
            # delete bullets
            if b.rect.y < 0:
                self.bullets.remove(b)

    def render(self):
        if self.hp > 67:
            self.screen.blit(self.base_sprite, (self.rect.x, self.rect.y))
        elif self.hp <= 67 and self.hp > 33:
            self.screen.blit(self.damaged_sprite, (self.rect.x, self.rect.y))
        else:
            self.screen.blit(self.very_damaged_sprite,
                             (self.rect.x, self.rect.y))

        self.screen.blit(self.engine_sprite, (self.rect.x, self.rect.y))

    def shoot(self):
        self.shoot_sound[random.randint(0, 1)].play()
        b = Bullet(self.rect, self.screen)
        self.bullets.append(b)

    def take_damage(self):
        self.hit_sound.play()
        self.hp -= 5

    def reset(self):
        self.hp = 100
        self.bullets = []
        self.rect.x = self.start_pos[0]
        self.rect.y = self.start_pos[1]

    def input(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_d] and self.rect.x < self.screen.get_width() - self.width:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_s] and self.rect.y < self.screen.get_height() - self.height:
            self.rect.y += self.speed


class Meteor:
   def __init__(self, screen):
        # stats
        self.width, self.height = 40, 60
        self.velocity = random.randint(2, 5)
        self.screen = screen

        # เลือกรูปแบบสุ่ม
        sprite_name = random.choice(["meteor.png", "meteor2.png", "meteor3.png"])
        sprite_path = os.path.join("assets", sprite_name)
        self.sprite = pygame.transform.scale(
            pygame.image.load(sprite_path), (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.sprite)


        self.rect = pygame.Rect(random.randint(
            self.width, self.screen.get_width() - self.width), -10, self.width, self.height)

   def reset(self):
        self.rect.x = random.randrange(
            self.width, self.screen.get_width() - self.width, self.width)
        self.rect.y = -10
        self.velocity = random.randint(2, 5)

   def update(self):
        if self.rect.y > self.screen.get_height():
            self.reset()
        self.rect.y += self.velocity

   def render(self):
        self.screen.blit(self.sprite, (self.rect.x, self.rect.y))


class Bullet:
    def __init__(self, player_rect, screen):
        self.size = 6
        self.velocity = 10
        self.color = (255, 252, 87)
        self.screen = screen

        self.rect = pygame.Rect(
            player_rect.x + 48, player_rect.y, self.size, self.size)

    def update(self):
        self.rect.y -= self.velocity

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
