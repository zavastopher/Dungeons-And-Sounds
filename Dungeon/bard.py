import midiutil
import dice
import math

SCALELENGTH = 7
PHRASEDURATION = 4
NOTEDEFAULT = .5
TRACK = 25
VOLUME = 100

root = dice.roll(11) + 59


# Define Major 
def makeMajorScale(root):
    return [root, root + 2, root + 4, root + 5,  root + 7, root + 9, root + 11]    
def makeDorianScale(root):
    return [root, root + 2, root + 3, root + 5, root + 7, root + 8, root + 11]
def makeMinorScale(root):
    return [root, root + 2, root + 3, root + 5,  root + 7, root + 8, root + 10]

def buildChord(scale, root):
    if len(scale) > 7:
        return ValueError
    scaleLen = len(scale)
    return [scale[root - 1], scale[(root + 1) % scaleLen], scale[(root + 3) % scaleLen],  scale[(root + 5) % scaleLen]]

class bard:
    channels = 0
    time = 0
    tempo = 120
    duration = 0
    score = None
    root = 0
    heroScale = None
    villianScale = None

    def __init__(self):
        self.root = dice.roll(11) 
        self.heroScale = makeMajorScale(root)
        self.villianScale = makeMinorScale(root)
        self.score = midiutil.MIDIFile(TRACK)
        self.score.addTrackName(8, 0, 'Chords')
        for idx in range(TRACK):
            self.score.addTempo(idx + 1, self.time, self.tempo)

    def outPutScore(self):
        with open('simulation.mid', 'wb') as outputfile:
            self.score.writeFile(outputfile)
    
    def writeAttack(self, start, attack, health, maxHealth, heroStatus, channel):
        position = start;
        # phraseDuration = PHRASEDURATION
        noteLength = NOTEDEFAULT
        noteVolume = math.trunc((health / maxHealth) * VOLUME)
        for i in range(len(attack)):
            octave = math.trunc(attack[i] / SCALELENGTH) * 12
            pitch = (self.heroScale[attack[i] % SCALELENGTH] if heroStatus else self.heroScale[attack[i] % SCALELENGTH]) + octave
            self.score.addNote(channel, 1,  pitch, position, noteLength, noteVolume)
            position += noteLength
        return position
    
    def addSingleNote(self, channel):
        self.score.addNote(TRACK, channel, self.villianScale[0], 0, 1, 10)
    
    def writeDrums(self, channel, position):
        for chann in range(4):
            i = 0
            self.score.addTrackName(chann + channel, 0, f'Drum Track {chann + 1}')
            while i < position:
                rythm = dice.roll(chann + 1)
                beat = 1/rythm
                for idx in range(rythm):
                    self.score.addNote(chann + channel, 1, 60, i + (idx * beat), beat, VOLUME)
                i += 1
    
    def nameTrack(self, track, name):
        self.score.addTrackName(track, 0, name)

    def writeChord(self, position):
        root = dice.roll(7)
        chord = buildChord(self.heroScale, root)
        self.score.addNote(8, 1, chord[0], position, 1, 60)
        self.score.addNote(8, 1, chord[1], position, 1, 60)
        self.score.addNote(8, 1, chord[2], position, 1, 60)
