import random

import pygame


class Sound:
    @staticmethod
    def play_background_music():
        pygame.mixer.music.load('Sounds/Defaults/Music_default_laning_01_layer_01.mp3')
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1, 0.0)

    @staticmethod
    def play_winner_sound(team):
        # winner_sound = pygame.mixer.Sound(f'Sounds/Defaults/Music_default_{team}_win.mp3')
        pygame.mixer.music.load(f'Sounds/Defaults/Music_default_{team}_win.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

    @staticmethod
    def play_hero_move_sound(hero):
        number = random.randrange(1, 6, 1)
        move_sound = pygame.mixer.Sound(f'Sounds/Move/{hero.__class__.__name__}_move_0{number}_ru.mp3')
        move_sound.set_volume(0.1)
        move_sound.play()

    @staticmethod
    def play_hero_level_up_sound(hero):
        number = random.randrange(1, 4, 1)
        move_sound = pygame.mixer.Sound(f'Sounds/LvlUp/{hero.__class__.__name__}_level_0{number}_ru.mp3')
        move_sound.set_volume(0.1)
        move_sound.play()

    @staticmethod
    def play_hero_attack_sound(hero):
        number = random.randrange(1, 4, 1)
        move_sound = pygame.mixer.Sound(f'Sounds/Attack/{hero.__class__.__name__}_attack_0{number}_ru.mp3')
        move_sound.set_volume(0.1)
        move_sound.play()

    @staticmethod
    def play_spell_cast_sound(hero):
        move_sound = pygame.mixer.Sound(f'Sounds/Attack/{hero.__class__.__name__}_attack_0_ru.mp3')
        move_sound.set_volume(0.1)
        move_sound.play()


