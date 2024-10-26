import character
import dice
import json
import bard

OKCYAN = '\033[96m'
ENDC = '\033[0m'
MAGENTA = '\u001b[35m'
YELLOW = '\u001b[33m'

monsterList = []
position = 0

def rollInitiative(speed):
    return dice.roll(10) + speed

def fight(position, fighter1, fighter2):
    first = fighter1 if rollInitiative(fighter1.speed) > rollInitiative(fighter2.speed) else fighter2
    second = fighter2 if fighter1 == first else fighter1
    
    firstHp = first.health
    secondHp = second.health
    
    firstAttacks = []
    secondAttacks = []
    
    while firstHp > 0 and secondHp > 0:
        firstAttack = first.attack()
        firstAttacks += firstAttack
        secondHp -= sum(firstAttack)
        position = dandelion.writeAttack(position, firstAttack, firstHp, first.health, first.name == 'hero', first.track)
        if(secondHp > 0):
            secondAttack = second.attack()
            secondAttacks += secondAttack
            firstHp -= sum(secondAttack)
            position = dandelion.writeAttack(position, secondAttack, secondHp, second.health, second.name == 'hero', second.track)
    
    return [first.name if firstHp > 0 else second.name, position]

# This function is for a single sim attempt
def attemptSim(position):
    i = 0
    dandelion.writeChord(position)
    thisFight = fight(position, geralt, monsterList[i])
    position = thisFight[1]
    winner = thisFight[0]
    while i < len(monsterList) and winner == geralt.name:
        thisFight = fight(position, geralt, monsterList[i])
        position = thisFight[1]
        winner = thisFight[0]
        i += 1
    geralt.levelUp(2 ** i)
    return [i != len(monsterList), position]

# Lets initialize our character and bard
geralt = character.character()
dandelion = bard.bard();

# Read the monster data which is stored jin the monsters.json file
with open('dungeon-data/monsters.json') as monstersData:
    monstersDump = json.load(monstersData)
for key in monstersDump:
    monsterEntry = monstersDump[key]
    monster = character.character(monsterEntry['name'], monsterEntry['strength'], monsterEntry['speed'], monsterEntry['constitution'], monsterEntry['stamina'], monsterEntry['health'], monsterEntry['weapon'], monsterEntry['track'])
    monsterList.append(monster)
    dandelion.nameTrack(monster.track, monster.name)
    # dandelion.addSingleNote(monster.track)

# Lets initialize everything and simulate the first run
stats = geralt.printStats()
heroPrevLevel = geralt.level
dandelion.nameTrack(geralt.track, f'Hero Level: {geralt.level}')
attempts = 1
attempt = attemptSim(position)

# Lets check if somehow geralt leveled up
if geralt.level > heroPrevLevel:
    heroPrevLevel = geralt.level
    geralt.levelUpTrack()
    dandelion.nameTrack(geralt.track, f'Hero Level: {geralt.level}')
attemptSuccess = attempt[0]
position = attempt[1]

# Loop until the simulation is a success.
while attemptSuccess:
    attempts += 1
    attempt = attemptSim(position)
    attemptSuccess = attempt[0]
    position = attempt[1]
    if geralt.level > heroPrevLevel:
        stats += geralt.printStats()
        heroPrevLevel = geralt.level
        geralt.levelUpTrack()
        dandelion.nameTrack(geralt.track, f'Hero Level: {geralt.level}')

# Lets write some drums for rythm
dandelion.writeDrums(geralt.track + 1, position)

# Finally we print out the stats that we have accumulated and write the piece to a midi file
with open('herostats.txt', 'w') as herolog:
    herolog.write(stats)
dandelion.outPutScore();
