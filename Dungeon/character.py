import dice
import math

STATMAX = 10

def rollStat():
    return math.trunc(dice.roll(6, 3, 1) / 2)


class character:

    def __init__(self, nm="Hero", st=None, sp=None, co=None, sta=1, he=None, we=None, track=9):
        self.name =  nm
        self.strength = rollStat() if st == None else st
        self.speed = rollStat() if sp == None else sp
        self.constitution = rollStat() if co == None else co
        self.stamina = sta
        self.weapon = 6 if we == None else we
        self.health = 10 + self.constitution if he == None else he
        self.xp = 0
        self.level = 1
        self.track = track
    
    def attack(self):
        attack = []
        for i in range(self.stamina):
            attack.append(dice.roll(self.weapon, 1) + self.strength)
        return attack
    
    def levelUp(self, points):
        self.xp += points
        while self.xp >= 10:
            self.level += 1
            if dice.roll(20) == 20:
                self.weapon += 1
            self.health += dice.roll(10) + self.constitution
            self.stamina += self.level % 2 if self.stamina < 9 else 0
            statToIncrease = dice.roll(3)
            # Randomly level up one of the three stats
            if self.strength + self.speed + self.constitution < 30:
                match statToIncrease:
                    case 1:
                        if(self.strength >= STATMAX):
                            statToIncrease = dice.roll(2) + 1
                        else:
                            self.strength += 1
                    case 2:
                        if(self.speed >= STATMAX):
                            statToIncrease = 3 if dice.roll(2) == 2 else 1
                        else:
                            self.speed += 1
                    case 3:
                        if(self.constitution >= STATMAX):
                            statToIncrease = dice.roll(2)
                        else:
                            self.constitution += 1
                            self.health + self.level
            self.xp -= 10
    def levelUpTrack(self):
        self.track += 1

    def printStats(self):
        return f"""Name: {self.name} 
        Health: {self.health} 
        Stamina: {self.stamina}
        Weapon: {self.weapon}
        Strength: {self.strength} 
        Speed: {self.speed} 
        Constitution: {self.constitution}\n"""