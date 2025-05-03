import pygame
import sys
import os
import entity
import scenes
import ui


class Game:
    def __init__(self):
        self.status = 'start'
        self.score = 0

        # background
        self.background = pygame.image.load(
            os.path.join('assets', 'background.png'))
        self.background_rect = pygame.Rect(0, 0, 1, 1)
        self.background_rect_loop = pygame.Rect(
            0, -self.background.get_height(), 1, 1)
        self.background_speed = 1

        # entities
        self.meteors = []
        for i in range(5):
            self.meteors.append(entity.Meteor(screen))
        self.player = entity.Player(screen)

        # scenes
        self.lose = scenes.Lose(screen, self.change_scene, self.reset_game)
        self.start = scenes.Start(screen, self.change_scene, self.background)
        self.ui = ui.Ui(screen, self.player)

        # audio
        pygame.mixer.music.load(os.path.join('assets', 'audio', 'music.mp3'))
        self.lose_sound = pygame.mixer.Sound(
            os.path.join('assets', 'audio', 'sfx_lose.ogg'))
        self.explode_sound = pygame.mixer.Sound(
            os.path.join('assets', 'audio', 'sfx_explosion.wav'))

    def change_scene(self, scene):
        self.status = scene

    def change_score(self, amount):
        self.score += amount

    def check_game_over(self):
        if self.player.hp <= 0:
            pygame.mixer.music.fadeout(100)
            self.lose_sound.play()
            self.change_scene('lose')

    def reset_game(self):
        self.score = 0
        self.player.reset()

        for m in self.meteors:
            m.reset()

    def handele_collision(self):
        # player collision
        for m in self.meteors:
            if m.mask.overlap(self.player.mask, (self.player.rect.x - m.rect.x, self.player.rect.y - m.rect.y)):
                m.reset()
                self.player.take_damage()

        # bullet collision
        for b in self.player.bullets:
            for m in self.meteors:
                if m.rect.colliderect(b.rect):
                    m.reset()
                    self.explode_sound.play()
                    self.change_score(1)

                    # temp fix for a collision error
                    if b in self.player.bullets:
                        self.player.bullets.remove(b)

    def scrolling_background(self):
        if self.background_rect.y <= self.background.get_height():
            self.background_rect.y += self.background_speed
        else:
            self.background_rect.y = self.background_rect_loop.y - self.background.get_height()

        if self.background_rect_loop.y <= self.background.get_height():
            self.background_rect_loop.y += self.background_speed
        else:
            self.background_rect_loop.y = self.background_rect.y - self.background.get_height()

    def render(self):
        screen.blit(self.background,
                    (self.background_rect.x, self.background_rect.y))
        screen.blit(self.background, (self.background_rect_loop.x,
                    self.background_rect_loop.y))

        for b in self.player.bullets:
            b.render()

        self.player.render()

        for m in self.meteors:
            m.render()

        self.ui.render(self.score)

    def update(self):
        match self.status:
            case 'start':
                self.start.update()
            case 'lose':
                self.lose.update()
            case 'game':
                self.player.update()
                self.scrolling_background()
                for m in self.meteors:
                    m.update()
                self.handele_collision()
                self.check_game_over()


# pygame setup
pygame.init()
pygame.font.init()
pygame.mixer.pre_init()
pygame.display.set_caption("Space pew pew")

screen_width, screen_height = 270, 480

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.player.shoot()
    game.render()
    game.update()

    pygame.display.update()
    clock.tick(60)
