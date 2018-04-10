import time
board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]]
majorScale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
majorOrMinor = ['major', 'minor', 'minor', 'major', 'major', 'minor']
chromatic = ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#']
major = True
suspended = False
sus2 = True
augmented = False
capo = 0
tuning = ['G', 'C', 'E', 'A']        

def getEmptyBoard():
    return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def setCapoTuning():
    global tuning
    if (capo == 0):
        tuning = ['G', 'C', 'E', 'A']        
    else:
        tuning = [chromatic[(findIndexInChromatic('G') + capo)], chromatic[(findIndexInChromatic('C') + capo)], chromatic[(findIndexInChromatic('E') + capo)], chromatic[(findIndexInChromatic('A') + capo)]]
##    return tuning

def setFifthInterval():
    if (augmented == True):   
        fifthInterval = 8
    else:
        fifthInterval = 7
    return fifthInterval

def setThirdInterval():
    if (major == True):   
        if (suspended == True):
            if (sus2 == True):
                thirdInterval = 2
            else:
                thirdInterval = 5
        else:
            thirdInterval = 4
    else:
        thirdInterval = 3
    return thirdInterval

def getChordName():
    if (major == True):
        if (augmented == True):
            return "aug"
        elif (suspended == True):
            if (sus2 == True):
                return "sus2"
            else:
                return "sus4"
        else:
            return "maj"
    else:
            return "m"

def findIndexInChromatic(note):
    for i in range(len(chromatic)): 
        if note == chromatic[i]:
            return i
    return -1

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

def getTriadForChord(startingNote):
    startingNotePos = findIndexInChromatic(startingNote)
    thirdInterval = setThirdInterval()
    #print(thirdInterval)
    fifthInterval = setFifthInterval()
    leftInArray = (len(chromatic) - startingNotePos)
    #print(leftInArray)
    # find notes in chord based on how much space is left in chromatic[]
    if leftInArray > thirdInterval:
        secondNote = chromatic[startingNotePos + thirdInterval]
    if leftInArray > fifthInterval:
        thirdNote = chromatic[startingNotePos + fifthInterval]
    else:
        thirdNote = chromatic[fifthInterval - leftInArray]
        secondNote = chromatic[thirdInterval - leftInArray]
    # assemble array of major triad
    chordValues = [startingNote, secondNote, thirdNote]
    return chordValues

# finds notes to play for each chord based on notes in major chord    
def updateFretBoardFromChord(fretBoard, chordValues):
    # import chord values
    setCapoTuning()
    #print(tuning)
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
                fretBoard[currentString][capo] = 1
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
                            fretBoard[currentString][minDifference + capo] = 1
                            value = stringStartingNotePos + minDifference
                            # makes sure value is not out of range of array
                            if (value == 12):
                                value = 0
                            #notesOnFretboard[currentString] = (chromatic[value])
    #print(notesOnFretboard)
    for i in range(len(tuning)):
        print(fretBoard[i])
    return fretBoard

# changes all desired notes to "1" values    
def updateFretBoard(fretBoard, idxForStrings):
    for i in range (len(tuning)):
        for j in range (len(chromatic)+1):
            if j == idxForStrings[i]:
                # prints desired note coord. values
                #print(i,j)
                fretBoard[i][j] = 1
    return fretBoard

# finds the four main chords in the key,
# assigns each chord a color,
# runs through each tab at a given timeframe
def displayMajorChords(baseNote):
    global major
    fromBaseNotePosition = 0
    value = 0
    print(baseNote + getChordName())
    baseIndex = findIndexInChromatic(baseNote)  
    fretBoard = updateFretBoardFromChord(getEmptyBoard(), getTriadForChord(baseNote))
    time.sleep(1)
    #print(color[0])
    for i in range(1,4):
        distFromBaseNotePos = (i - 1) * 2 + 5
        if ((baseIndex + distFromBaseNotePos) > 11):
            value = ((baseIndex + distFromBaseNotePos) - len(fretBoard[0]))
        else:
            value = baseIndex + distFromBaseNotePos
        if (distFromBaseNotePos == 9):
            major = False
        print(chromatic[value] + getChordName())

        fretBoard = updateFretBoardFromChord(getEmptyBoard(), getTriadForChord(chromatic[value]))
        #print(color[i])
        #setLEDStripFromBoard(fretBoard)
        time.sleep(1)
            
    major = True

def displayAllChords(baseNote):
    global major
    majorOrMinorValue = 0
    baseNotePos = findIndexInChromatic(baseNote)
    for i in range(len(majorScale)):
        if (majorScale[i] == 1):
            chordPos = i
            if (majorOrMinor[majorOrMinorValue] == 'major'):
                major = True
            else:
                major = False
            if ((i + baseNotePos) > len(board[0]) - 1):
                chordPos = chordPos + baseNotePos - len(chromatic)
            else:
                chordPos += baseNotePos
            print(chromatic[chordPos] + getChordName())
            updateFretBoardFromChord(getEmptyBoard(), getTriadForChord(chromatic[chordPos]))
            majorOrMinorValue += 1
            if (majorOrMinorValue == len(majorOrMinor)):
                break

def displaySingleChord(rootNote):
    updateFretBoardFromChord(getEmptyBoard(), getTriadForChord(rootNote))

#def applyFretBoardToUkulele():

#setCapoTuning()
#displayAllChords('A')
displayMajorChords('G')
#displaySingleChord('G#')
