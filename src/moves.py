import cube

def rotateRight():
    cube.redSide = cube.redSide[::-1]
    cube.redSide = cube.redSide.transpose()

    tempGreen = [cube.greenSide[0][2],cube.greenSide[1][2],cube.greenSide[2][2]]
    tempWhite = [cube.whiteSide[0][2],cube.whiteSide[1][2],cube.whiteSide[2][2]]
    tempBlue = [cube.blueSide[2][0],cube.blueSide[1][0],cube.blueSide[0][0]]
    tempYellow = [cube.yellowSide[0][2],cube.yellowSide[1][2],cube.yellowSide[2][2]]

    tempWhite,tempBlue,tempYellow,tempGreen = tempGreen,tempWhite,tempBlue,tempYellow

    cube.greenSide[0][2],cube.greenSide[1][2],cube.greenSide[2][2] = tempGreen[0],tempGreen[1],tempGreen[2]
    cube.whiteSide[0][2],cube.whiteSide[1][2],cube.whiteSide[2][2] = tempWhite[0],tempWhite[1],tempWhite[2]
    cube.blueSide[2][0],cube.blueSide[1][0],cube.blueSide[0][0] = tempBlue[0],tempBlue[1],tempBlue[2]
    cube.yellowSide[0][2],cube.yellowSide[1][2],cube.yellowSide[2][2] = tempYellow[0],tempYellow[1],tempYellow[2]

def rotateLeft():
    cube.orangeSide = cube.orangeSide[::-1]
    cube.orangeSide = cube.orangeSide.transpose()

    tempGreen = [cube.greenSide[0][0],cube.greenSide[1][0],cube.greenSide[2][0]]
    tempWhite = [cube.whiteSide[0][0],cube.whiteSide[1][0],cube.whiteSide[2][0]]
    tempBlue = [cube.blueSide[2][2],cube.blueSide[1][2],cube.blueSide[0][2]]
    tempYellow = [cube.yellowSide[0][0],cube.yellowSide[1][0],cube.yellowSide[2][0]]

    tempWhite,tempBlue,tempYellow,tempGreen = tempBlue,tempYellow,tempGreen,tempWhite

    cube.greenSide[0][0],cube.greenSide[1][0],cube.greenSide[2][0] = tempGreen[0],tempGreen[1],tempGreen[2]
    cube.whiteSide[0][0],cube.whiteSide[1][0],cube.whiteSide[2][0] = tempWhite[0],tempWhite[1],tempWhite[2]
    cube.blueSide[2][2],cube.blueSide[1][2],cube.blueSide[0][2] = tempBlue[0],tempBlue[1],tempBlue[2]
    cube.yellowSide[0][0],cube.yellowSide[1][0],cube.yellowSide[2][0] = tempYellow[0],tempYellow[1],tempYellow[2]

def rotateUp():
    cube.whiteSide = cube.whiteSide[::-1]
    cube.whiteSide = cube.whiteSide.transpose()

    tempGreen = [cube.greenSide[0][0],cube.greenSide[0][1],cube.greenSide[0][2]]
    tempOrange = [cube.orangeSide[0][0],cube.orangeSide[0][1],cube.orangeSide[0][2]]
    tempBlue = [cube.blueSide[0][0],cube.blueSide[0][1],cube.blueSide[0][2]]
    tempRed = [cube.redSide[0][0],cube.redSide[0][1],cube.redSide[0][2]]

    tempGreen,tempOrange,tempBlue,tempRed = tempRed,tempGreen,tempOrange,tempBlue

    cube.greenSide[0][0],cube.greenSide[0][1],cube.greenSide[0][2] = tempGreen[0],tempGreen[1],tempGreen[2]
    cube.orangeSide[0][0],cube.orangeSide[0][1],cube.orangeSide[0][2] = tempOrange[0],tempOrange[1],tempOrange[2]
    cube.blueSide[0][0],cube.blueSide[0][1],cube.blueSide[0][2] = tempBlue[0],tempBlue[1],tempBlue[2]
    cube.redSide[0][0],cube.redSide[0][1],cube.redSide[0][2] = tempRed[0],tempRed[1],tempRed[2]

def rotateDown():
    cube.yellowSide = cube.yellowSide[::-1]
    cube.yellowSide = cube.yellowSide.transpose()

    tempGreen = [cube.greenSide[2][0],cube.greenSide[2][1],cube.greenSide[2][2]]
    tempOrange = [cube.orangeSide[2][0],cube.orangeSide[2][1],cube.orangeSide[2][2]]
    tempBlue = [cube.blueSide[2][0],cube.blueSide[2][1],cube.blueSide[2][2]]
    tempRed = [cube.redSide[2][0],cube.redSide[2][1],cube.redSide[2][2]]

    tempGreen,tempOrange,tempBlue,tempRed = tempOrange,tempBlue,tempRed,tempGreen

    cube.greenSide[2][0],cube.greenSide[2][1],cube.greenSide[2][2] = tempGreen[0],tempGreen[1],tempGreen[2]
    cube.orangeSide[2][0],cube.orangeSide[2][1],cube.orangeSide[2][2] = tempOrange[0],tempOrange[1],tempOrange[2]
    cube.blueSide[2][0],cube.blueSide[2][1],cube.blueSide[2][2] = tempBlue[0],tempBlue[1],tempBlue[2]
    cube.redSide[2][0],cube.redSide[2][1],cube.redSide[2][2] = tempRed[0],tempRed[1],tempRed[2]

def rotateFront():
    cube.greenSide = cube.greenSide[::-1]
    cube.greenSide = cube.greenSide.transpose()

    tempWhite = [cube.whiteSide[2][0],cube.whiteSide[2][1],cube.whiteSide[2][2]]
    tempOrange = [cube.orangeSide[2][2],cube.orangeSide[1][2],cube.orangeSide[0][2]]
    tempYellow = [cube.yellowSide[0][0],cube.yellowSide[0][1],cube.yellowSide[0][2]]
    tempRed = [cube.redSide[0][0],cube.redSide[1][0],cube.redSide[2][0]]

    tempWhite,tempOrange,tempYellow,tempRed = tempOrange,tempYellow,tempRed,tempWhite

    cube.whiteSide[2][0],cube.whiteSide[2][1],cube.whiteSide[2][2] = tempWhite[0],tempWhite[1],tempWhite[2]
    cube.orangeSide[0][2],cube.orangeSide[1][2],cube.orangeSide[2][2] = tempOrange[0],tempOrange[1],tempOrange[2]
    cube.yellowSide[0][2],cube.yellowSide[0][1],cube.yellowSide[0][0] = tempYellow[0],tempYellow[1],tempYellow[2]
    cube.redSide[0][0],cube.redSide[1][0],cube.redSide[2][0] = tempRed[0],tempRed[1],tempRed[2]

def rotateBack():
    cube.blueSide = cube.blueSide[::-1]
    cube.blueSide = cube.blueSide.transpose()

    tempWhite = [cube.whiteSide[0][0],cube.whiteSide[0][1],cube.whiteSide[0][2]]
    tempOrange = [cube.orangeSide[0][0],cube.orangeSide[1][0],cube.orangeSide[2][0]]
    tempYellow = [cube.yellowSide[2][2],cube.yellowSide[2][1],cube.yellowSide[2][0]]
    tempRed = [cube.redSide[0][2],cube.redSide[1][2],cube.redSide[2][2]]

    tempWhite,tempOrange,tempYellow,tempRed = tempRed,tempWhite,tempOrange,tempYellow

    cube.whiteSide[0][0],cube.whiteSide[0][1],cube.whiteSide[0][2] = tempWhite[0],tempWhite[1],tempWhite[2]
    cube.orangeSide[2][0],cube.orangeSide[1][0],cube.orangeSide[0][0] = tempOrange[0],tempOrange[1],tempOrange[2]
    cube.yellowSide[2][0],cube.yellowSide[2][1],cube.yellowSide[2][2] = tempYellow[0],tempYellow[1],tempYellow[2]
    cube.redSide[0][2],cube.redSide[1][2],cube.redSide[2][2] = tempRed[0],tempRed[1],tempRed[2]

def rotateRight2():
    for i in range(2):
        rotateRight()

def rotateLeft2():
    for i in range(2):
        rotateLeft()

def rotateUp2():
    for i in range(2):
        rotateUp()

def rotateDown2():
    for i in range(2):
        rotateDown()
    
def rotateFront2():
    for i in range(2):
        rotateFront()

def rotateBack2():
    for i in range(2):
        rotateBack()

def rotateRight3():
    for i in range(3):
        rotateRight()

def rotateLeft3():
    for i in range(3):
        rotateLeft()

def rotateUp3():
    for i in range(3):
        rotateUp()

def rotateDown3():
    for i in range(3):
        rotateDown()
    
def rotateFront3():
    for i in range(3):
        rotateFront()

def rotateBack3():
    for i in range(3):
        rotateBack()