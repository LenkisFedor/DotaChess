import pygame
import controls
import sys
from deck import Deck
from disables import Disable
from heroes import create_heroes_list
from heroes import is_hero_on_position
from sounds import Sound

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dota Chess")

    Sound.play_background_music()
    
    create_heroes_list(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    hero = is_hero_on_position(pos)
                    if hero and hero.team == Deck.team:
                        Disable.reset_disables(hero)
                        if not hero.disables['stun'].is_disabled:
                            controls.select_hero(screen, hero)
        controls.update(screen, Deck.current_hero_list)


run()
