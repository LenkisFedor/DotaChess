import random
import sys

import pygame

from sounds import Sound

BLUE = (135, 206, 250)
GRAY = (180, 180, 180)
DARK_GRAY = (47, 79, 79)
BLACK = (0, 0, 0)

COLORS = [GRAY, BLACK]

CELL_SIZE = 60

HEROES_LIST = []


class Deck(pygame.sprite.Sprite):
    team = random.randrange(0, 2, 1)

    current_hero_list = []

    move_counter = 0

    @staticmethod
    def change_team():
        Deck.team = 1 - Deck.team

    @staticmethod
    def create_deck(screen):
        if Deck.team == 0:
            team_font = pygame.font.SysFont('georgia', 35)
            team_text = team_font.render("DIRE", True, (180, 0, 0))
            text_rect = pygame.Rect(0, 0, team_text.get_width(), team_text.get_height())
            text_rect.center = (screen.get_rect().width - 95, screen.get_rect().centery + 7)
            dire_team_heroes = [hero for hero in Deck.current_hero_list if hero.team == 0 and
                                not hero.disables['stun'].is_disabled]
            if len(dire_team_heroes) == 0:
                winner_font = pygame.font.SysFont('georgia', 75)
                winner_text = winner_font.render("RADIANT VICTORY", True, (0, 180, 0))
                winner_rect = pygame.Rect(0, 0, winner_text.get_width(), winner_text.get_height())
                winner_rect.center = screen.get_rect().center
                Sound.play_winner_sound("radiant")
                screen.blit(winner_text, winner_rect)
                Deck.end_game(screen)
        else:
            team_font = pygame.font.SysFont('georgia', 27)
            team_text = team_font.render("RADIANT", True, (0, 180, 0))
            text_rect = pygame.Rect(0, 0, team_text.get_width(), team_text.get_height())
            text_rect.center = (screen.get_rect().width - 95, screen.get_rect().centery + 7)
            radiant_team_heroes = [hero for hero in Deck.current_hero_list if hero.team == 1 and
                                   not hero.disables['stun'].is_disabled]
            if len(radiant_team_heroes) == 0:
                winner_font = pygame.font.SysFont('georgia', 75)
                winner_text = winner_font.render("DIRE VICTORY", True, (180, 0, 0))
                winner_rect = pygame.Rect(0, 0, winner_text.get_width(), winner_text.get_height())
                winner_rect.center = screen.get_rect().center
                Sound.play_winner_sound("dire")
                screen.blit(winner_text, winner_rect)
                Deck.end_game(screen)
        screen.blit(team_text, text_rect)

    @staticmethod
    def end_game(screen):
        pygame.display.flip()
        end_mes_font = pygame.font.SysFont('sans', 35)
        end_mes_text = end_mes_font.render("Нажмите ESCAPE, или закройте окно", True, DARK_GRAY)
        end_mes_rect = pygame.Rect(0, 0, end_mes_text.get_width(), end_mes_text.get_height())
        end_mes_rect.center = (screen.get_rect().centerx, screen.get_rect().centery + 45)
        screen.blit(end_mes_text, end_mes_rect)
        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
