import math
import random

import pygame

import controls
from deck import CELL_SIZE as C_SIZE, Deck

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (47, 79, 79)
GRAY = (180, 180, 180)
BLUE = (135, 206, 250)
RED = (180, 0, 0)
DARK_RED = (128, 0, 0)
SPRING_GREEN = (0, 255, 127)
GOLD = (255, 215, 0)


def get_spell_pos(spell, hero):
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos_x = pygame.mouse.get_pos()[0]
                pos_y = pygame.mouse.get_pos()[1]
                pos_x = ((pos_x - 182) // C_SIZE) * C_SIZE + C_SIZE / 2 + 182
                pos_y = ((pos_y - 54) // C_SIZE) * C_SIZE + C_SIZE / 2 + 54
                pos = [pos_x, pos_y]
                if math.hypot(pos[0] - hero.rect.centerx, pos[1] - hero.rect.centery) <= \
                        spell.cast_range * C_SIZE:
                    return pos
                else:
                    continue


def heroes_in_spell_area(spell):
    heroes = [hero for hero in Deck.current_hero_list if pygame.sprite.collide_rect_ratio(1)(spell, hero)]
    unique_heroes = list(set(heroes))
    return unique_heroes


def hero_in_spell_position(spell_pos):
    for hero in Deck.current_hero_list:
        if hero.rect.center == spell_pos:
            return hero


def movement_in_direction(start_pos, pos, displacement):
    if pos[0] > start_pos[0]:
        start_pos[0] += displacement
    if pos[0] < start_pos[0]:
        start_pos[0] -= displacement
    if pos[1] > start_pos[1]:
        start_pos[1] += displacement
    if pos[1] < start_pos[1]:
        start_pos[1] -= displacement
    return start_pos


def movement_to_position(start_pos, intermediate_pos, end_pos, displacement):
    distance_x = end_pos[0] - start_pos[0]
    distance_y = end_pos[1] - start_pos[1]
    if distance_y == 0:
        if distance_x > 0:
            intermediate_pos[0] += displacement
        else:
            intermediate_pos[0] -= displacement
    elif distance_x == 0:
        if distance_y > 0:
            intermediate_pos[1] += displacement
        else:
            intermediate_pos[1] -= displacement
    else:
        distance_ratio = distance_x / distance_y
        intermediate_pos[0] += displacement * (distance_ratio / (distance_y / C_SIZE))
        intermediate_pos[1] += displacement * (distance_ratio / (distance_x / C_SIZE))
    return intermediate_pos


class Spell(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.cooldown = 0
        self.cooldown_counter = 0
        self.cast_range = 2
        self.damage = 100
        self.type = 'active'
        self.clock = pygame.time.Clock()

    def reset_cooldown(self, hero):
        if Deck.move_counter >= self.cooldown_counter + self.cooldown:
            self.cooldown = 0


class Light_Strike(Spell):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, C_SIZE * 2, C_SIZE * 2)

    def cast(self, hero):
        pos = get_spell_pos(self, hero)
        radius = 1
        while radius <= C_SIZE:
            pygame.draw.circle(hero.screen, (180, 0, 0), pos, radius)
            pygame.display.flip()
            radius += 0.1
            self.rect.center = pos
            self.cooldown = 5
        for enemy_hero in heroes_in_spell_area(self):
            if enemy_hero.team != hero.team:
                enemy_hero.health -= self.damage
                enemy_hero.disables['stun'].is_disabled = True
                enemy_hero.disables['stun'].duration = 4
                enemy_hero.disables['stun'].duration_counter = Deck.move_counter
        self.cooldown_counter = Deck.move_counter
        hero.action_counter += 1
        return


class Dragon_Slave(Spell):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, C_SIZE, C_SIZE)
        self.cast_range = 3
        self.damage = 250

    def cast(self, hero):
        enemy_heroes = []
        pos = get_spell_pos(self, hero)
        end_pos = [hero.rect.centerx, hero.rect.centery]
        self.rect.center = hero.rect.center
        radius = 1
        i = 0
        while radius <= C_SIZE / 2:
            self.clock.tick(30)
            self.rect.center = movement_to_position([hero.rect.centerx, hero.rect.centery], end_pos, pos, 10)
            pygame.draw.circle(hero.screen, (180, 0, 0), self.rect.center, radius)
            pygame.display.update()
            for enemy_hero in heroes_in_spell_area(self):
                if enemy_hero not in enemy_heroes and enemy_hero.team != hero.team:
                    enemy_heroes.append(enemy_hero)
            self.cooldown = 3
            i += 1
            radius += 1.6
            pygame.draw.circle(hero.screen, (180, 0, 0), self.rect.center, radius)
            pygame.display.update()
            if i % 3 == 0:
                controls.update(hero.screen, Deck.current_hero_list)
        for enemy_hero in enemy_heroes:
            enemy_hero.health -= self.damage
        self.cooldown_counter = Deck.move_counter
        hero.action_counter += 1
        return


class Laguna_Blade(Spell):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, C_SIZE * 2, C_SIZE * 2)
        self.cast_range = 3
        self.damage = 450
        self.color = (135, 206, 250)

    def cast(self, hero):
        i = 1
        pos = get_spell_pos(self, hero)
        self.rect.center = pos
        end_pos = [hero.rect.centerx, hero.rect.centery]
        if hero_in_spell_position(self.rect.center) and hero_in_spell_position(self.rect.center).team != hero.team:
            while end_pos != pos:
                self.clock.tick(30)
                pygame.draw.line(hero.screen, self.color, hero.rect.center, end_pos, i)
                pygame.display.flip()
                end_pos = movement_to_position([hero.rect.centerx, hero.rect.centery], end_pos, pos, 20)
            while i < 7:
                self.clock.tick(12)
                pygame.draw.line(hero.screen, self.color, hero.rect.center, end_pos, i)
                pygame.display.flip()
                i += 1
                self.cooldown = 11
            enemy_hero = hero_in_spell_position(self.rect.center)
            enemy_hero.health -= self.damage
            self.cooldown_counter = Deck.move_counter
            hero.action_counter += 1
            return


class Stifling_Dagger(Spell):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 2, 2)
        self.cast_range = 4
        self.damage = 150
        self.color = DARK_GRAY

    def cast(self, hero):
        pos = get_spell_pos(self, hero)
        self.rect.center = [hero.rect.centerx, hero.rect.centery]
        end_pos = [hero.rect.centerx, hero.rect.centery]
        if hero_in_spell_position((int(pos[0]), int(pos[1]))) and\
                hero_in_spell_position((int(pos[0]), int(pos[1]))).team != hero.team:
            enemy_hero = hero_in_spell_position((int(pos[0]), int(pos[1])))
            while not pygame.sprite.collide_rect(self, enemy_hero):
                self.clock.tick(30)
                pygame.draw.circle(hero.screen, self.color, self.rect.center, 3)
                pygame.display.flip()
                self.rect.center = movement_to_position([hero.rect.centerx, hero.rect.centery], end_pos, pos, 10)
                pygame.draw.circle(hero.screen, self.color, self.rect.center, 3)
                pygame.display.update()
                controls.update(hero.screen, Deck.current_hero_list)
            enemy_hero = hero_in_spell_position((pos[0], pos[1]))
            self.damage = Coup_de_Grace().cast(enemy_hero)
            enemy_hero.health -= self.damage
            self.cooldown = 3
            self.cooldown_counter = Deck.move_counter
            hero.action_counter += 1
            return


class Phantom_Strike(Spell):
    def __init__(self):
        super().__init__()
        self.cast_range = 3

    def cast(self, hero):
        pos = get_spell_pos(self, hero)
        any_hero = hero_in_spell_position((pos[0], pos[1]))
        if hero_in_spell_position((pos[0], pos[1])):
            hero.move_to_hero(any_hero)
        self.cooldown = 5
        hero.action_counter -= 1
        self.cooldown_counter = Deck.move_counter
        return


class Coup_de_Grace(Spell):
    def __init__(self):
        super().__init__()
        self.damage = 150
        self.type = 'passive'

    def cast(self, enemy_hero):
        self.damage = 150
        damage = random.randrange(0, 5, 1)
        if damage == 0:
            radius = 1
            self.damage = 450
            while radius <= C_SIZE / 2:
                pygame.draw.circle(enemy_hero.screen, DARK_RED, enemy_hero.rect.center, radius, width=2)
                pygame.display.flip()
                radius += 1
                pygame.draw.circle(enemy_hero.screen, DARK_RED, enemy_hero.rect.center, radius, width=2)
                pygame.display.flip()
                if radius % 3 == 0:
                    controls.update(enemy_hero.screen, Deck.current_hero_list)
        return self.damage


class Magic_Missile(Spell):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, C_SIZE * 2, C_SIZE * 2)
        self.cast_range = 3
        self.color = DARK_GRAY

    def cast(self, hero):
        pos = get_spell_pos(self, hero)
        self.rect.center = pos
        end_pos = [hero.rect.centerx, hero.rect.centery]
        if hero_in_spell_position(self.rect.center) and hero_in_spell_position(self.rect.center).team != hero.team:
            while end_pos != pos:
                self.clock.tick(30)
                pygame.draw.circle(hero.screen, self.color, end_pos, 6)
                pygame.display.flip()
                end_pos = movement_to_position([hero.rect.centerx, hero.rect.centery], end_pos, pos, 10)
                self.cooldown = 3
                pygame.draw.circle(hero.screen, self.color, end_pos, 6)
                pygame.display.update()
                controls.update(hero.screen, Deck.current_hero_list)
            enemy_hero = hero_in_spell_position(self.rect.center)
            enemy_hero.health -= self.damage
            enemy_hero.disables['stun'].is_disabled = True
            enemy_hero.disables['stun'].duration = 2
            enemy_hero.disables['stun'].duration_counter = Deck.move_counter
            self.cooldown_counter = Deck.move_counter
            hero.action_counter += 1
            return


class Vengeance_Aura(Spell):
    def __init__(self):
        super().__init__()
        self.type = 'passive'

    def cast(self, hero):
        hero.damage = 50
        self.cooldown = 1
        return

    def reset_cooldown(self, hero):
        pass


class Nether_Swap(Spell):
    def __init__(self):
        super().__init__()
        self.range = 4

    def cast(self, hero):
        pos = get_spell_pos(self, hero)
        self.rect.center = pos
        if hero_in_spell_position((pos[0], pos[1])):
            any_hero = hero_in_spell_position(self.rect.center)
            any_hero.rect.center = hero.rect.center
            hero.rect.center = pos
        self.cooldown = 5
        self.cooldown_counter = Deck.move_counter
        return


class Wraithfire_Blast(Spell):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, C_SIZE * 2, C_SIZE * 2)
        self.cast_range = 3
        self.color = SPRING_GREEN

    def cast(self, hero):
        pos = get_spell_pos(self, hero)
        self.rect.center = pos
        end_pos = [hero.rect.centerx, hero.rect.centery]
        if hero_in_spell_position(self.rect.center) and hero_in_spell_position(self.rect.center).team != hero.team:
            while end_pos != pos:
                self.clock.tick(30)
                pygame.draw.circle(hero.screen, self.color, end_pos, 6)
                pygame.display.flip()
                end_pos = movement_to_position([hero.rect.centerx, hero.rect.centery], end_pos, pos, 10)
                self.cooldown = 3
                pygame.draw.circle(hero.screen, self.color, end_pos, 6)
                pygame.display.update()
                controls.update(hero.screen, Deck.current_hero_list)
            enemy_hero = hero_in_spell_position(self.rect.center)
            enemy_hero.health -= self.damage
            enemy_hero.disables['stun'].is_disabled = True
            enemy_hero.disables['stun'].duration = 4
            enemy_hero.disables['stun'].duration_counter = Deck.move_counter
            self.cooldown_counter = Deck.move_counter
            hero.action_counter += 1
            return


class Mortal_Strike(Spell):
    def __init__(self):
        super().__init__()
        self.damage = 100
        self.type = 'passive'

    def cast(self, enemy_hero):
        self.damage = 100
        damage = random.randint(0, 3)
        if damage == 0:
            radius = 1
            self.damage = 300
            while radius <= C_SIZE / 2:
                pygame.draw.circle(enemy_hero.screen, DARK_RED, enemy_hero.rect.center, radius, width=2)
                pygame.display.flip()
                radius += 1
                pygame.draw.circle(enemy_hero.screen, DARK_RED, enemy_hero.rect.center, radius, width=2)
                pygame.display.flip()
                if radius % 3 == 0:
                    controls.update(enemy_hero.screen, Deck.current_hero_list)
        return self.damage


class Reincarnation(Spell):
    def __init__(self):
        super().__init__()
        self.type = 'passive'
        self.delay = 0
        self.delay_counter = 0

    def cast(self, hero):
        self.rect.center = hero.rect.center
        self.cooldown = 15
        self.cooldown_counter = Deck.move_counter
        self.delay = 2
        self.delay_counter = Deck.move_counter
        hero.spell_with_delay = self
        return

    def cast_with_delay(self, hero):
        hero.health = 1250
        Deck.current_hero_list.append(hero)
        self.cooldown = 15
        return


class Take_Aim(Spell):
    def __init__(self):
        super().__init__()
        self.type = 'passive'


class Headshot(Spell):
    def __init__(self):
        super().__init__()
        self.type = 'passive'
        self.damage = 100

    def cast(self, self_hero, enemy_hero):
        self.damage = 100
        damage = random.randrange(0, 5, 1)
        pos1 = [enemy_hero.rect.centerx, enemy_hero.rect.centery]
        pos2 = [self_hero.rect.centerx, self_hero.rect.centery]
        if damage < 2:
            radius = 1
            self.damage = 150
            enemy_hero.rect.center = movement_in_direction(pos1, pos2, -C_SIZE)
            while radius <= C_SIZE / 4:
                pygame.draw.circle(enemy_hero.screen, WHITE, enemy_hero.rect.center, radius, width=2)
                pygame.display.flip()
                radius += 1
                pygame.draw.circle(enemy_hero.screen, WHITE, enemy_hero.rect.center, radius, width=2)
                pygame.display.flip()
                if radius % 3 == 0:
                    controls.update(enemy_hero.screen, Deck.current_hero_list)
        return self.damage


class Assassinate(Spell):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.cast_range = 6
        self.damage = 300
        self.color = (240, 230, 140)
        self.delay = 0
        self.delay_counter = 0
        self.enemy_hero = None

    def cast(self, hero):
        pos = get_spell_pos(self, hero)
        self.rect.center = [hero.rect.centerx, hero.rect.centery]
        if hero_in_spell_position((int(pos[0]), int(pos[1]))) and\
                hero_in_spell_position((int(pos[0]), int(pos[1]))).team != hero.team:
            self.enemy_hero = hero_in_spell_position((int(pos[0]), int(pos[1])))
            hero.action_counter += 1
            self.delay = 2
            self.delay_counter = Deck.move_counter
            hero.spell_with_delay = self
            return

    def cast_with_delay(self, hero):
        self.cooldown = 5
        pos = [self.enemy_hero.rect.centerx, self.enemy_hero.rect.centery]
        end_pos = [hero.rect.centerx, hero.rect.centery]
        while not pygame.sprite.collide_rect(self, self.enemy_hero):
            self.clock.tick(120)
            pygame.draw.circle(hero.screen, self.color, end_pos, 5)
            pygame.display.flip()
            self.rect.center = movement_to_position([hero.rect.centerx, hero.rect.centery], end_pos, pos, 10)
            pygame.draw.circle(hero.screen, self.color, end_pos, 5)
            pygame.display.update()
            controls.update(hero.screen, Deck.current_hero_list)
        enemy_hero = hero_in_spell_position(self.enemy_hero.rect.center)
        enemy_hero.health -= self.damage
        self.cooldown_counter = Deck.move_counter
        return


class Blinding_Light(Spell):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, C_SIZE * 3, C_SIZE * 3)

    def cast(self, hero):
        pos = get_spell_pos(self, hero)
        radius = 1
        while radius <= C_SIZE * 1.5:
            pygame.draw.circle(hero.screen, WHITE, pos, radius, 4)
            pygame.display.flip()
            radius += 1.5
            self.rect.center = pos
            self.cooldown = 5
            if radius % 2 == 0:
                controls.update(hero.screen, Deck.current_hero_list)
        for enemy_hero in heroes_in_spell_area(self):
            pos1 = [enemy_hero.rect.centerx, enemy_hero.rect.centery]
            pos2 = [self.rect.centerx, self.rect.centery]
            if enemy_hero.team != hero.team:
                enemy_hero.rect.center = movement_in_direction(pos1, pos2, -C_SIZE)
                enemy_hero.disables['blind'].is_disabled = True
                enemy_hero.disables['blind'].duration = 4
                enemy_hero.disables['blind'].duration_counter = Deck.move_counter
        self.cooldown_counter = Deck.move_counter
        hero.action_counter += 1
        return


class Illuminate(Spell):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, C_SIZE * 3, C_SIZE)
        self.cast_range = 4

    def cast(self, hero):
        any_heroes = []
        pos = get_spell_pos(self, hero)
        end_pos = [hero.rect.centerx, hero.rect.centery]
        self.rect.center = hero.rect.center
        radius = 1
        i = 0
        while radius <= C_SIZE:
            self.clock.tick(30)
            self.rect.center = movement_to_position([hero.rect.centerx, hero.rect.centery], end_pos, pos, 10)
            pygame.draw.circle(hero.screen, WHITE, self.rect.center, radius)
            pygame.display.update()
            for any_hero in heroes_in_spell_area(self):
                if any_hero not in any_heroes:
                    any_heroes.append(any_hero)
            self.cooldown = 6
            i += 1
            radius += 2.5
            pygame.draw.circle(hero.screen, WHITE, self.rect.center, radius)
            pygame.display.update()
            if i % 3 == 0:
                controls.update(hero.screen, Deck.current_hero_list)
        for any_hero in any_heroes:
            if any_hero.team != hero.team:
                any_hero.health -= self.damage
            if any_hero.team == hero.team and hero != any_hero:
                any_hero.health += self.damage
        self.cooldown_counter = Deck.move_counter
        hero.action_counter += 1
        return


class Recall(Spell):
    def __init__(self):
        super().__init__()
        self.cast_range = 10

    def cast(self, hero):
        pos = get_spell_pos(self, hero)
        self.rect.center = pos
        if hero_in_spell_position((pos[0], pos[1])):
            alias_hero = hero_in_spell_position(self.rect.center)
            if alias_hero.team == hero.team:
                alias_hero.move_to_hero(hero)
        self.cooldown = 5
        hero.action_counter -= 1
        self.cooldown_counter = Deck.move_counter
        return
