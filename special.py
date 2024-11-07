import pygame


class Special:
    def __init__(self, abilityfunc, prefunc, postfunc, charge, max_charge, key, sett):
        super().__init__()
        self.can_use = True
        self.sett = sett
        self.abilityfunc = abilityfunc
        self.prefunc = prefunc
        self.postfunc = postfunc
        self.charge = charge
        self.max_charge = max_charge
        self.key = key

    def update(self):
        keys = pygame.key.get_pressed()

        pre = self.prefunc(self.charge, self.max_charge, self.key, keys, self.can_use)

        if pre == True or pre == False:
            self.can_use = pre

        if keys[self.key] and self.can_use and self.sett.charge[self.charge] >= self.max_charge:
            self.can_use = False
            self.sett.charge[self.charge] = 0
            self.abilityfunc(self.charge, self.max_charge, self.key, keys, self.can_use)

        post = self.postfunc(self.charge, self.max_charge, self.key, keys, self.can_use)

        if post == True or post == False:
            self.can_use = post