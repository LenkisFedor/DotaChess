from deck import Deck


class Disable:
    def __init__(self):
        self.is_disabled = False
        self.duration = 0
        self.duration_counter = 0

    @staticmethod
    def reset_disables(hero):
        for key in hero.disables:
            if Deck.move_counter >= hero.disables[key].duration_counter + hero.disables[key].duration:
                hero.disables[key].duration = 0
                hero.disables[key].duration_counter = 0
                hero.disables[key].is_disabled = False
