import pygame
import sys

from deck import Deck
from deck import HEROES_LIST
from heroes import is_hero_on_position
from heroes import is_heroes_in_area

BLUE = (135, 206, 250)
GRAY = (180, 180, 180)
DARK_GRAY = (47, 79, 79)
BLACK = (0, 0, 0)
RED = (180, 0, 0)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)

COLORS = [GRAY, BLACK]


def select_hero(screen, hero):
    hero.lvl_up()
    draw_hero_lvl(screen, hero)
    while hero.action_counter < 1:
        draw_spells_table(screen, hero)
        selection_frame = pygame.Rect(hero.rect.topleft[0], hero.rect.topleft[1], hero.rect.width, hero.rect.height)
        pygame.draw.rect(screen, BLUE, selection_frame, 2)
        draw_enemy_selection_frame(screen, hero)
        pygame.display.flip()
        while 1:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    pos = pygame.mouse.get_pos()
                    if is_hero_on_position(pos):
                        enemy = is_hero_on_position(pos)
                        if enemy in is_heroes_in_area(hero.rect.center, hero.range):
                            hero.attack(enemy)
                break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE and hero.action_counter < 1:
                    return
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3:
                    hero.cast_ability(event)
                    break
                if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_d or \
                        event.key == pygame.K_s:
                    hero.move(event)
                    break
                continue
        update(screen, HEROES_LIST)
    hero.move_counter += 1
    hero.action_counter = 0
    Deck.change_team()
    Deck.move_counter += 1


def draw_enemy_selection_frame(screen, hero):
    heroes_in_area = is_heroes_in_area(hero.rect.center, hero.range)
    for entry_hero in heroes_in_area:
        if entry_hero.team != hero.team:
            selection_frame = pygame.Rect(entry_hero.rect.topleft[0], entry_hero.rect.topleft[1],
                                          entry_hero.rect.width, entry_hero.rect.height)
            pygame.draw.rect(screen, RED, selection_frame, 2)


def draw_spells_table(screen, hero):
    i = 0
    for key in hero.spells:
        """Поле со способностями героев"""
        if hero.lvl > i:
            spell = pygame.image.load(f'Images/{hero.hero_name}/{key}.png')
            spell_rect = spell.get_rect()
            spell_rect.center = (93, 249 + 135 * i)
            screen.blit(spell, spell_rect)
            hero.spells[key].reset_cooldown(hero)
            if hero.spells[key].cooldown:
                cooldown_font = pygame.font.SysFont('arial black', 90)
                cooldown_text = cooldown_font.render(
                    f'{hero.spells[key].cooldown_counter + hero.spells[key].cooldown - Deck.move_counter}',
                    True, DARK_GRAY)
                cooldown_rect = cooldown_text.get_rect()
                cooldown_rect.center = spell_rect.center
                screen.blit(cooldown_text, cooldown_rect)
            i += 1


# def draw_spell_selection_frame(screen, hero):


def draw_health(screen, hero):
    heart = pygame.image.load(f'Images/HealthBar.png')
    heart_rect = heart.get_rect()
    heart_rect.center = (hero.rect.centerx, hero.rect.centery + 25)
    health_font = pygame.font.SysFont('verdana',  9, bold=True)
    health_text = health_font.render(f'{hero.health}', True, WHITE)
    health_rect = health_text.get_rect()
    health_rect.center = heart_rect.center
    screen.blit(heart, heart_rect)
    screen.blit(health_text, health_rect)


def draw_hero_lvl(screen, hero):
    lvl_font = pygame.font.SysFont('arial black', 10)
    lvl_text = lvl_font.render(f'LVL {hero.lvl}', True, GOLD)
    screen.blit(lvl_text, (hero.rect.centerx - 12, hero.rect.centery - 30))


def update(screen, heroes, bg_image=pygame.image.load('Images/Deck/Deck.png')):
    screen.blit(bg_image, [0, 0])
    Deck.create_deck(screen)
    for hero in heroes:
        if hero.health > 0:
            hero.draw()
            draw_health(screen, hero)
            draw_hero_lvl(screen, hero)
        if hero.spell_with_delay is not None:
            hero.cast_ability_with_delay(hero.spell_with_delay)
    pygame.display.flip()
