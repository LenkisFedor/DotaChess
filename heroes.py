from disables import Disable
from spells import *
from deck import HEROES_LIST
from deck import Deck
from sounds import Sound


def create_heroes_list(screen):
    references_to_children = [hero for hero in Hero.__subclasses__()]
    for i in range(3):
        for x in range(2):
            if not x:
                new_hero = references_to_children[i](screen, references_to_children[i].__name__, 0)
                new_hero.rect.centerx = new_hero.screen_rect.centerx - C_SIZE + C_SIZE * i
                new_hero.rect.centery = new_hero.screen_rect.top + C_SIZE / 2
            else:
                new_hero = references_to_children[-(i + 1)](screen, references_to_children[-(i + 1)].__name__, 1)
                new_hero.rect.centerx = new_hero.screen_rect.centerx - C_SIZE + C_SIZE * i
                new_hero.rect.centery = new_hero.screen_rect.bottom - C_SIZE / 2
            HEROES_LIST.append(new_hero)
    for hero in HEROES_LIST:
        Deck.current_hero_list.append(hero)


def is_hero_on_position(position):
    for hero in Deck.current_hero_list:
        if hero.rect.centerx + C_SIZE / 2 > position[0] > hero.rect.centerx - C_SIZE / 2 and \
                hero.rect.centery - C_SIZE / 2 < position[1] < hero.rect.centery + C_SIZE / 2:
            return hero
    return False


def is_heroes_in_area(area_center, area_radius):
    heroes_in_area = []
    for hero in Deck.current_hero_list:
        if area_center[0] - area_radius * C_SIZE <= hero.rect.centerx <= area_center[0] + area_radius * C_SIZE \
                and area_center[1] - area_radius * C_SIZE <= hero.rect.centery <= area_center[1] + area_radius * C_SIZE:
            heroes_in_area.append(hero)
    return heroes_in_area


class Hero(pygame.sprite.Sprite):

    def __init__(self, screen, hero_name, team):
        pygame.sprite.Sprite.__init__(self)
        """"Инициализация героя"""
        self.hero_name = hero_name
        self.screen = screen
        self.image = pygame.image.load(f'Images/{hero_name}/{hero_name}.png')
        self.rect = self.image.get_rect()
        self.screen_rect = pygame.Rect(0, 0, 660, 660)
        self.screen_rect.center = self.screen.get_rect().center
        self.action_counter = 0
        self.move_counter = 0
        self._health = 1000
        self.max_health = 1000
        self.team = team
        self.spells = []
        self.spell_with_delay = None
        self.count = 0
        self.lvl = 1
        self.range = 1
        self.damage = 100
        self.disables = {'blind': Disable(), 'stun': Disable()}

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new):
        self._health = new
        if self._health < 1:
            Deck.current_hero_list.remove(self)
        if self._health > self.max_health:
            self._health = self.max_health

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < len(Deck.current_hero_list):
            self.count += 1
            return Deck.current_hero_list[self.count - 1]

    def move_to_hero(self, hero):
        if self.rect.centerx < hero.rect.centerx:
            if not is_hero_on_position((hero.rect.center[0] - C_SIZE, hero.rect.center[1])):
                self.rect.center = (hero.rect.center[0] - C_SIZE, hero.rect.center[1])
            elif not is_hero_on_position((hero.rect.center[0], hero.rect.center[1] - C_SIZE)):
                self.rect.center = (hero.rect.center[0], hero.rect.center[1] - C_SIZE)
            elif not is_hero_on_position((hero.rect.center[0], hero.rect.center[1] + C_SIZE)):
                self.rect.center = (hero.rect.center[0], hero.rect.center[1] + C_SIZE)
        elif self.rect.centery < hero.rect.centery:
            if not is_hero_on_position((hero.rect.center[0], hero.rect.center[1] - C_SIZE)):
                self.rect.center = (hero.rect.center[0], hero.rect.center[1] - C_SIZE)
            elif not is_hero_on_position((hero.rect.center[0] + C_SIZE, hero.rect.center[1])):
                self.rect.center = (hero.rect.center[0] + C_SIZE, hero.rect.center[1])
            elif not is_hero_on_position((hero.rect.center[0] - C_SIZE, hero.rect.center[1])):
                self.rect.center = (hero.rect.center[0] - C_SIZE, hero.rect.center[1])
        elif self.rect.centerx > hero.rect.centerx:
            if not is_hero_on_position((hero.rect.center[0] + C_SIZE, hero.rect.center[1])):
                self.rect.center = (hero.rect.center[0] + C_SIZE, hero.rect.center[1])
            elif not is_hero_on_position((hero.rect.center[0], hero.rect.center[1] - C_SIZE)):
                self.rect.center = (hero.rect.center[0], hero.rect.center[1] - C_SIZE)
            elif not is_hero_on_position((hero.rect.center[0], hero.rect.center[1] + C_SIZE)):
                self.rect.center = (hero.rect.center[0], hero.rect.center[1] + C_SIZE)
        elif self.rect.centery > hero.rect.centery:
            if not is_hero_on_position((hero.rect.center[0], hero.rect.center[1] + C_SIZE)):
                self.rect.center = (hero.rect.center[0], hero.rect.center[1] + C_SIZE)
            elif not is_hero_on_position((hero.rect.center[0] + C_SIZE, hero.rect.center[1])):
                self.rect.center = (hero.rect.center[0] + C_SIZE, hero.rect.center[1])
            elif not is_hero_on_position((hero.rect.center[0] - C_SIZE, hero.rect.center[1])):
                self.rect.center = (hero.rect.center[0] - C_SIZE, hero.rect.center[1])

    def move(self, event):

        def move_right():
            self.rect.move_ip(C_SIZE, 0)
            self.action_counter += 1
            self.draw()

        def move_left():
            self.rect.move_ip(-C_SIZE, 0)
            self.action_counter += 1
            self.draw()

        def move_top():

            self.rect.move_ip(0, -C_SIZE)
            self.action_counter += 1
            self.draw()

        def move_bottom():
            self.rect.move_ip(0, C_SIZE)
            self.action_counter += 1
            self.draw()

        if event.key == pygame.K_d and self.rect.right < self.screen_rect.right and \
                not is_hero_on_position((self.rect.center[0] + C_SIZE, self.rect.center[1])):
            move_right()
        if event.key == pygame.K_a and self.rect.left > self.screen_rect.left and \
                not is_hero_on_position((self.rect.center[0] - C_SIZE, self.rect.center[1])):
            move_left()
        if event.key == pygame.K_w and self.rect.top > self.screen_rect.top and \
                not is_hero_on_position((self.rect.center[0], self.rect.center[1] - C_SIZE)):
            move_top()
        if event.key == pygame.K_s and self.rect.bottom < self.screen_rect.bottom and \
                not is_hero_on_position((self.rect.center[0], self.rect.center[1] + C_SIZE)):
            move_bottom()

        Sound.play_hero_move_sound(self)

    def draw(self):
        """Отрисовка героя"""
        self.screen.blit(self.image, self.rect)

    def attack(self, hero):
        if hero.team != self.team:
            self.action_counter += 1
            Sound.play_hero_attack_sound(self)
            if not self.disables['blind'].is_disabled:
                hero.health -= self.damage

    def cast_ability(self, event):
        i = 1
        for key in self.spells:
            if i == 1 and event.key == pygame.K_1 and self.spells[key].type != 'passive' and\
                    self.spells[key].cooldown == 0:
                self.spells[key].cast(self)
            if i == 2 and event.key == pygame.K_2 and self.spells[key].type != 'passive' and\
                    self.spells[key].cooldown == 0:
                self.spells[key].cast(self)
            if i == 3 and event.key == pygame.K_3 and self.spells[key].type != 'passive' and\
                    self.spells[key].cooldown == 0:
                self.spells[key].cast(self)
            i += 1

    def cast_ability_with_delay(self, spell):
        if spell.delay + spell.delay_counter <= Deck.move_counter:
            self.spell_with_delay = None
            spell.cast_with_delay(self)

    def lvl_up(self):
        if self.move_counter == 2:
            Sound.play_hero_level_up_sound(self)
            self.lvl = 2
        if self.move_counter == 5:
            Sound.play_hero_level_up_sound(self)
            self.lvl = 3


class Veng(Hero):
    def __init__(self, screen, hero_name, team):
        super().__init__(screen, hero_name, team)
        self.spells = {'magic_missile': Magic_Missile(),
                       'vengeance_aura': Vengeance_Aura(),
                       'nether_swap': Nether_Swap()}
        self._health = 750
        self.max_health = 750
        self.range = 2

    @property
    def health(self):
        return self._health

    @Hero.health.setter
    def health(self, new):
        self._health = new
        if self._health < 1:
            if self.spells['vengeance_aura'].cooldown == 0:
                self._health = 750
                self.spells['vengeance_aura'].cast(self)
            else:
                Deck.current_hero_list.remove(self)
        if self._health > self.max_health:
            self._health = self.max_health


class Lina(Hero):

    def __init__(self, screen, hero_name, team):
        super().__init__(screen, hero_name, team)
        self.spells = {'dragon_slave': Dragon_Slave(), 'light_strike': Light_Strike(), 'laguna_blade': Laguna_Blade()}
        self.range = 2


class PhantomAssassin(Hero):
    def __init__(self, screen, hero_name, team):
        super().__init__(screen, hero_name, team)
        self.range = 1
        self.damage = 150
        self.spells = {'stifling_dagger': Stifling_Dagger(),
                       'phantom_strike': Phantom_Strike(),
                       'coup_de_grace': Coup_de_Grace()}

    def attack(self, hero):
        if hero.team != self.team:
            self.action_counter += 1
            hero.health -= self.spells['coup_de_grace'].cast(hero)


class WraithKing(Hero):
    def __init__(self, screen, hero_name, team):
        super().__init__(screen, hero_name, team)
        self.spells = {'wraithfire_blast': Wraithfire_Blast(),
                       'mortal_strike': Mortal_Strike(),
                       'reincarnation': Reincarnation()}
        self._health = 1250
        self.max_health = 1250
        self.range = 1

    def attack(self, hero):
        if hero.team != self.team:
            self.action_counter += 1
            hero.health -= self.spells['mortal_strike'].cast(hero)

    @property
    def health(self):
        return self._health

    @Hero.health.setter
    def health(self, new):
        self._health = new
        if self._health < 1:
            if self.spells['reincarnation'].cooldown == 0:
                # self._health = 1250
                self.spells['reincarnation'].cast(self)
                Deck.current_hero_list.remove(self)
            else:
                Deck.current_hero_list.remove(self)
        if self._health > self.max_health:
            self._health = self.max_health


class Sniper(Hero):
    def __init__(self, screen, hero_name, team):
        super().__init__(screen, hero_name, team)
        self.spells = {'take_aim': Take_Aim(),
                       'headshot': Headshot(),
                       'assassinate': Assassinate()}
        self.range = 3
        self.health = 750
        self.max_health = 750

    def attack(self, hero):
        if hero.team != self.team:
            self.action_counter += 1
            hero.health -= self.spells['headshot'].cast(self, hero)


class Kotl(Hero):
    def __init__(self, screen, hero_name, team):
        super().__init__(screen, hero_name, team)
        self.spells = {'blinding_light': Blinding_Light(),
                       'illuminate': Illuminate(),
                       'recall': Recall()}
        self.range = 2
        self.health = 750
        self.max_health = 750




