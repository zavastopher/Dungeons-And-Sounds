import random

def roll(die, numOfDie=1, dropLowest=0):
    random.seed()

    results = []
    for i in range(0, numOfDie):
        results.append(random.randrange(die) + 1)
    results.sort()
    roll = 0
    for i in range(0, numOfDie - dropLowest):
        roll += results[i]
    return roll