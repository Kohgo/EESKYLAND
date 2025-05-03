import pygame
import os


class Lose:

    def __init__(self, screen, change_scene, reset) -> None:
        self.hint = 'press ENTER to start'
        self.message = 'You lost'
        self.font = pygame.font.SysFont('Arial', 12)
        self.big_font = pygame.font.SysFont('Arial', 32)
        self.screen = screen

        self.change_scene = change_scene
        self.reset = reset
        self.start_sound = pygame.mixer.Sound(
            os.path.join('assets', 'audio', 'sfx_start.ogg'))

    def input(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RETURN]:
            pygame.mixer.music.play(-1)
            self.start_sound.play()
            self.reset()
            self.change_scene('game')

    def render(self):
        hint_text = self.font.render(self.hint, 1, (255, 255, 255))
        lose_text = self.big_font.render(self.message, 2, (255, 255, 255))

        bg = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height()))
        bg.set_alpha(100)
        bg.fill((28, 28, 28))

        self.screen.blit(bg, (0, 0))
        self.screen.blit(hint_text, (self.screen.get_width(
        ) / 2 - hint_text.get_width() / 2, self.screen.get_height() / 2 + 100))
        self.screen.blit(lose_text, (self.screen.get_width(
        ) / 2 - lose_text.get_width() / 2, self.screen.get_height() / 2 - 100))

    def update(self):
        self.input()
        self.render()


class Start:

    def __init__(self, screen, change_scene, background) -> None:
        self.hint = 'press ENTER to start'
        self.title = 'Space Pew Pew'
        self.font = pygame.font.SysFont('Arial', 12)
        self.big_font = pygame.font.SysFont('Arial', 32)

        self.background = background
        self.screen = screen

        self.change_scene = change_scene

        self.start_sound = pygame.mixer.Sound(
            os.path.join('assets', 'audio', 'sfx_start.ogg'))

    def input(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RETURN]:
            self.start_sound.play()
            pygame.mixer.music.play(-1)
            self.change_scene('game')

    def render(self):
        self.screen.blit(self.background, (0, 0))

        hint_text = self.font.render(self.hint, 1, (255, 255, 255))
        title_text = self.big_font.render(self.title, 2, (255, 255, 255))

        bg = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height()))
        bg.set_alpha(100)
        bg.fill((28, 28, 28))

        self.screen.blit(bg, (0, 0))
        self.screen.blit(hint_text, (self.screen.get_width(
        ) / 2 - hint_text.get_width() / 2, self.screen.get_height() / 2 + 100))
        self.screen.blit(title_text, (self.screen.get_width(
        ) / 2 - title_text.get_width() / 2, self.screen.get_height() / 2 - 100))

    def update(self):
        self.input()
        self.render()
