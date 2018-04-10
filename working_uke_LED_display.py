import time

from neopixel import *


# LED strip configuration:
LED_COUNT      = 17      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN       = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
strip.begin()

board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
majorScale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
tuning = ['G', 'C', 'E', 'A']
chromatic = ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#']
major = True

def fretBoardToLEDStrip(fretBoard):
    LEDStrip = []
    for i in range(0, len(board[0])):
        if (i % 2 != 0):
            LEDStrip.append(fretBoard[0][i])
            LEDStrip.append(fretBoard[1][i])
            LEDStrip.append(fretBoard[2][i])
            LEDStrip.append(fretBoard[3][i])
            
        else:
            LEDStrip.append(fretBoard[3][i])
            LEDStrip.append(fretBoard[2][i])
            LEDStrip.append(fretBoard[1][i])
            LEDStrip.append(fretBoard[0][i])
            
    return LEDStrip
        

def clearPixels():
    for i in range(0, LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def getEmptyBoard():
    clearPixels()
    return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
def setLEDStripFromBoard(fretBoard, color = Color(255, 255, 255)):
    #[print(str(fret)) for fret in fretBoard]
    LEDStrip = fretBoardToLEDStrip(fretBoard)
    print(LEDStrip)
    clearPixels()
    for i in range(0,len(LEDStrip)):
        if (LEDStrip[i] == 1):
            strip.setPixelColor(i, color)
        strip.show()
    # find given note's position in array
    
def findIndexInChromatic(note):
    for i in range(len(chromatic)): 
        if note == chromatic[i]:
            return i
    return -1

def getMajorOrMinor(major):
    if (major):   
        thirdInterval = 4
    else:
        thirdInterval = 3
    return thirdInterval

def displayMajorChords(base):
    fretBoard = getEmptyBoard()
    fretBoard = updateFretBoardFromChord(fretBoard, getTriadForChord(base))
    setLEDStripFromBoard(fretBoard)
    time.sleep(1)

    fretBoard = getEmptyBoard() 

    baseIndex = findIndexInChromatic(base)
    fretBoard = updateFretBoardFromChord(fretBoard, getTriadForChord(chromatic[baseIndex + 5]))
    setLEDStripFromBoard(fretBoard)
    time.sleep(1)

    fretBoard = getEmptyBoard() 
    
    fretBoard = updateFretBoardFromChord(fretBoard, getTriadForChord(chromatic[baseIndex + 7]))
    setLEDStripFromBoard(fretBoard)
    time.sleep(1)

# startingNote = one of the tuning in array
# noteDesired = implicit
def getDistanceForString(startingNote, noteDesired):
    startingNotePos = 0
    desiredNotePos = 0
    # find given note's position in array
    for i in range(len(chromatic)): 
        if startingNote == chromatic[i]:
            startingNotePos = i
            break
    # find desired note's position in array
    for i in range(len(chromatic)):
        if noteDesired == chromatic[i]:
            desiredNotePos = i
    # return difference between starting and desired note positions
    posDifference = desiredNotePos - startingNotePos
    if posDifference < 0:
        posDifference = len(chromatic) + posDifference
    return posDifference

# finds the notes in each major chord
def getTriadForChord(startingNote):
    startingNotePos = findIndexInChromatic(startingNote)
    thirdInterval = getMajorOrMinor()
    fifthInterval = 7
    leftInArray = len(chromatic) - startingNotePos
    #print(leftInArray)
    # find notes in chord based on how much space is left in chromatic[]
    if leftInArray > 3:
        thirdInterval = chromatic[startingNotePos + thirdInterval]
    if leftInArray > 7:
        fifthInterval = chromatic[startingNotePos + fifthInterval]
    else:
        fifthInterval = chromatic[7 - leftInArray]
        thirdInterval = chromatic[3 - leftInArray]
    # assemble array of major triad
    chordValues = [startingNote, thirdInterval, fifthInterval]
    return chordValues

# finds notes to play for each chord based on notes in major chord    
def updateFretBoardFromChord(fretBoard, chordValues):
    # import chord values
    print(chordValues)
    notesOnFretboard = [0,0,0,0]
    #run a for loop to check each string
    for currentString in range (len(tuning)):               # string...tuning[G, C, E, A]
        minDifference = len(chromatic)
        # this loop checks to see if any strings
        # already match up with a chordValue
        for i in range (len(chordValues)):      # i...chordValues[G B D]
            if tuning[currentString] == chordValues[i]:
                #notesOnFretboard[currentString] = chordValues[i]
                fretBoard[currentString][0] = 1
                break
            else:
                # finds positions of triad notes within chromatic array
                for j in range(len(chromatic)):
                    if chordValues[i] == chromatic[j]:
                        notePosOfPossibleNote = j
                        break
                        # find difference in startingNotePos and original currentString note position
                for k in range(len(chromatic)):
                    if  tuning[currentString] == chromatic[k]:
                        #print(chromatic[9])
                        stringStartingNotePos = k
                        #print(k, j)
                        difference = notePosOfPossibleNote - stringStartingNotePos
                        if (difference < 0):
                            difference += len(chromatic)
                        if (difference < minDifference):
                            minDifference = difference
                        #print("string", currentString, "note pos in chromatic", k , "minimum difference", minDifference)
                        # uses smallest difference value to find next proper note on 
                        if (i == len(chordValues) - 1):
                            fretBoard[currentString][minDifference] = 1
                            value = stringStartingNotePos + minDifference
                            # makes sure value is not out of range of array
                            if (value == 12):
                                value = 0
                            #notesOnFretboard[currentString] = (chromatic[value])
    return fretBoard

# noteDesired = implicit
def getAllNotes(noteDesired):
    idxForStrings = [0, 0, 0, 0]
    for i in range (len(tuning)):
        idxForStrings[i] = getDistanceForString(tuning[i], noteDesired)
    return idxForStrings

# changes all desired notes to "1" values    
def updateFretBoard(fretBoard, idxForStrings):
    for i in range (len(tuning)):
        for j in range (len(chromatic)+1):
            if j == idxForStrings[i]:
                # prints desired note coord. values
                #print(i,j)
                fretBoard[i][j] = 1
    return fretBoard

# test: finding all notes of G
#print(str(getAllNotes('G'))) # expect [0, 7, 3, 10]

##print(len(board))
##print(len(board[0]))

# test: display correct coord. of G notes
#updateFretBoard(getAllNotes('D'))

#pFretBoard(board)

# test: display Chord note names and best notes for chord
##for chords in range(len(chromatic)):
#print(str(getNotesOnUkulele(getChordNotes(chromatic[chords]))))# expect [G, D, G, B]

displayMajorChords('A#')


