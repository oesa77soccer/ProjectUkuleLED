import time
board = [[0 for col in range(11)] for row in range(4)]
majorScale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
majorOrMinor = ['major', 'minor', 'minor', 'major', 'major', 'minor']
chromatic = ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#']

          #maj/m   sus    aug     7#
chordAdj = [True, False, False, False]
capo = 0
tun = ['G', 'C', 'E', 'A']

def getEmptyBoard():
    return [[0 for col in range(11)] for row in range(4)]

def setCapoTuning(capo):
    for i in range (len(tun)):
        index = (findIndexInList(tun[i], chromatic) + capo)
        if index >= len(chromatic):
            index -= len(chromatic)
        tun[i] = chromatic[index]
    return tun

def setFifthInterval(adj):
    if (adj[2] == True):   
        fifthInterval = 8
    else:
        fifthInterval = 7
    return fifthInterval

def setThirdInterval(adj):
    if (adj[0] == True):   
        if (adj[1] == True):
            thirdInterval = 2
        else:
            thirdInterval = 4
    else:
        thirdInterval = 3
    return thirdInterval

def getChordName(adj):
    if (adj[0] == True):
        if (adj[1] == True):
            return "aug"
        elif (adj[2] == True):
            return "sus"
        else:
            return "maj"
    else:
            return "m"
        
def printFretBoard(board):
    for i in range(len(board)):
        print(tun[i], board[i])
    
def findIndexInList(note, lis):
    for i in range(len(lis)): 
        if note == lis[i]:
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
    startingNotePos = findIndexInList(startingNote, chromatic)
    thirdInterval = setThirdInterval(chordAdj)
    #print(thirdInterval)
    fifthInterval = setFifthInterval(chordAdj)
    leftInArray = (len(chromatic) - startingNotePos)

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

def findTriadNotePosition(string):
    for i in range(len(chromatic)):
        if string == chromatic[i]:
            pos = i
            return pos 

# finds notes to play for each chord based on notes in major chord    
def updateFretBoardFromChord(fretBoard, chordValues, capo):
    tuning = setCapoTuning(capo)
    print(chordValues)
    notesOnFretboard = [0,0,0,0]
    
    #run a for loop to check each string
    for i in range (len(tuning)):               # string...tuning[G, C, E, A] ## [E, A, D, G, B, E]
        currentString = tuning[i]    ## if two strings are the same in tuning (ex. guitars) it only finds the first 
        if (currentString in chordValues):
            fretBoard[i][0] = 1
        else:
            currentNoteIndex = findIndexInList(currentString, chromatic)
            minDifference = len(chromatic)

            for chordValueNote in chordValues:      # chordValueNote...chordValues[C E G]
                
                currentStringChromIndex = findIndexInList(chordValueNote, chromatic)
                difference = currentStringChromIndex - currentNoteIndex
                if (difference < 0):
                    difference += len(chromatic)
                if (difference < minDifference):
                    minDifference = difference
                                
            fretBoard[i][minDifference] = 1

    printFretBoard(fretBoard)
    return fretBoard

# changes all desired notes to "1" values    
def updateFretBoard(fretBoard, idxForStrings):
    for i in range (len(tuning)):
        for j in range (len(chromatic)+1):
            if j == idxForStrings[i]:
                # prints desired note coord. values
                fretBoard[i][j] = 1
    return fretBoard

# finds the four main chords in the key,
# assigns each chord a color,
# runs through each tab at a given timeframe
def displayMajorChords(baseNote):
    fromBaseNotePosition = [5, 7, 9]
    value = 0
    print(baseNote + getChordName(chordAdj))
    
    baseIndex = findIndexInList(baseNote, chromatic)
    fretBoard = updateFretBoardFromChord(getEmptyBoard(), getTriadForChord(baseNote), capo)

    for i in range(0,3):
        time.sleep(1)
        distFromBaseNotePos = fromBaseNotePosition[i]
        if ((baseIndex + distFromBaseNotePos) > len(chromatic)-1):
            value = ((baseIndex + distFromBaseNotePos) - len(chromatic))
        else:
            value = baseIndex + distFromBaseNotePos
        if (distFromBaseNotePos == 9):
            chordAdj[0] = False
        print(chromatic[value] + getChordName(chordAdj))

        fretBoard = updateFretBoardFromChord(getEmptyBoard(), getTriadForChord(chromatic[value]), capo)
            
def displayAllChords(baseNote):
    majorOrMinorValue = 0                  
    baseNotePos = findIndexInList(baseNote, chromatic)
    for i in range(len(majorScale)):
        if (majorScale[i] == 1):
            chordPos = i
            if (majorOrMinor[majorOrMinorValue] == 'major'):
                chordAdj[0] = True
            else:
                chordAdj[0] = False
                
            if ((i + baseNotePos) > len(board[0]) - 1):
                chordPos = chordPos + baseNotePos - len(chromatic)
            else:
                chordPos += baseNotePos
                
            print(chromatic[chordPos] + getChordName(chordAdj))
            updateFretBoardFromChord(getEmptyBoard(), getTriadForChord(chromatic[chordPos]), capo)
            majorOrMinorValue += 1
            if (majorOrMinorValue == len(majorOrMinor)):
                break
            
def updateFretBoardFromNote(board, note):
    chromNoteIndex = findIndexInList(note, chromatic)
    ## iterates through each string
    for string in range(len(tun)):
        
        stringNoteIndex = findIndexInList(tun[string], chromatic)
        value = chromNoteIndex - stringNoteIndex
        if (value == len(board[0]) or value == -1):
            continue
        if (value < 0):
            value += 1
        board[string][value] = 1
    return board

def displayAllNotes(listOfNotes):
    print('Display all notes of:', listOfNotes)
    fretBoard = getEmptyBoard()
    listOfNotes = listOfNotes.split()
    for note in listOfNotes:
        fretBoard = updateFretBoardFromNote(fretBoard, note)
    printFretBoard(fretBoard)

def displaySingleChord(rootNote):
    updateFretBoardFromChord(getEmptyBoard(), getTriadForChord(rootNote), capo)

#displayAllChords('G')
#displayMajorChords('E')
#displaySingleChord('F')
displayAllNotes('A B C D E F G')

