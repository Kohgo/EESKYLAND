import pygame

class Ui:

    def __init__(self, screen, player) -> None:
        self.screen = screen
        self.player = player

        self.font = pygame.font.SysFont('Arial', 18)
        self.big_font = pygame.font.SysFont('Arial', 32)

    def render(self, score):
        score_text = self.big_font.render(str(score), 1, (255, 255, 255))
        hp_text = self.font.render(str(self.player.hp), 1, (255, 255, 255))

        self.screen.blit(score_text, (self.screen.get_width() / 2 - score_text.get_width() / 2, score_text.get_height()))
        self.screen.blit(hp_text, (self.player.rect.x + self.player.width / 2 - hp_text.get_width() / 2, self.player.rect.y + self.player.height))