


def checkPositionalMovement(pieceType , currentPos , finalPos):
    if pieceType == "Pawn":
        if finalPos[0] == currentPos[0]:
            if currentPos[1] == '2' and finalPos[1] in '34' and challengerMove:
                return True
            elif currentPos[1] == '7' and finalPos[1] in '65' and challengerMove:
                return True

            if ourAI.color == 'w' and challengerMove:
                if int(finalPos[1]) - int(currentPos[1]) == -1:
                    return True
            elif ourAI.color == 'w' and not challengerMove:
                if int(finalPos[1]) - int(currentPos[1]) == 1:
                    return True
            elif ourAI.color == 'b' and challengerMove:
                if int(finalPos[1]) - int(currentPos[1]) == 1:
                    return True
            elif ourAI.color == 'b' and not challengerMove:
                if int(finalPos[1]) - int(currentPos[1]) == -1:
                    return True
        elif abs(int(finalPos[1]) - int(currentPos[1])) == 1 and abs(ord(finalPos[0]) - ord(currentPos[0])) == 1:
            if ourAI.color == 'w':
                if int(finalPos[1]) - int(currentPos[1]) == -1 and boardPosition[int(finalPos[1])][ord(finalPos[0]) - 97] != "Empty":
                    if boardPosition[int(finalPos[1])][ord(finalPos[0]) - 97][1] != boardPosition[int(currentPos[1])][ord(currentPos[0]) - 97][1]:
                        return True
            else:
                if int(finalPos[1]) - int(currentPos[1]) == 1 and boardPosition[int(finalPos[1])][ord(finalPos[0]) - 97] != "Empty":
                    if boardPosition[int(finalPos[1])][ord(finalPos[0]) - 97][1] != boardPosition[int(currentPos[1])][ord(currentPos[0]) - 97][1]:
                        return True
    elif pieceType == "Rook":
        if finalPos[0] == currentPos[0] or finalPos[1] == currentPos[1]:
            return True
    elif pieceType == "Bishop":
        if abs(int(finalPos[1]) - int(currentPos[1])) == abs(ord(finalPos[0]) - ord(currentPos[0])):
            return True
    elif pieceType == "Knight":
        if abs(int(finalPos[1]) - int(currentPos[1])) <= 2 and abs(ord(finalPos[0]) - ord(currentPos[0])) <= 2:
            if abs(int(finalPos[1]) - int(currentPos[1])) + abs(ord(finalPos[0]) - ord(currentPos[0])) == 3:
                return True
    elif pieceType == "Queen":
        if abs(int(finalPos[1]) - int(currentPos[1])) == abs(ord(finalPos[0]) - ord(currentPos[0])):
            return True
        elif finalPos[0] == currentPos[0] or finalPos[1] == currentPos[1]:
            return True
    elif pieceType == "King":
        if abs(int(finalPos[1]) - int(currentPos[1])) + abs(ord(finalPos[0]) - ord(currentPos[0])) == 1:
            return True
        elif abs(int(finalPos[1]) - int(currentPos[1])) == 1 and abs(ord(finalPos[0]) - ord(currentPos[0])) == 1:
            return True

    return False

def checkMoveValidity(str , boardPosition):
    if(len(str) != 4):
        return False
    elif(str[0] not in "abcdefgh" or str[2] not in "abcdefgh"):
        return False
    elif(str[1] not in "12345678" or str[3] not in "12345678" ):
        return False
    elif(str[0:2] == str[2:]):
        return False
    elif(boardPosition[int(str[1])][ord(str[0]) - 97] == "Empty"):
        return False
    elif(boardPosition[int(str[1])][ord(str[0]) - 97][1] == boardPosition[int(str[3])][ord(str[2]) - 97][1]):
        return False
    elif(not checkPositionalMovement(getPieceTypeFromBoard(str[0:2] , whitePieces , blackPieces) , str[0:2] , str[2:])):
        return False


    return True




def filterForIllegalMove(possibleMoves , boardPosition):
    tempBoardPosition = boardPosition
    finalListOfMoves = []
    for moves in possibleMoves:
        if makeTheMoveOnBoard(moves[0:2] , moves[2:] , getPieceTypeFromBoard(moves[0:2] , whitePieces , blackPieces) , tempBoardPosition , whitePieces , blackPieces , False , ourAI):
            finalListOfMoves.append(moves)
        tempBoardPosition = boardPosition

        currentList = []
        if ourAI.color == "w":
            currentList = whitePieces
        else:
            currentList = blackPieces

        for pieces in currentList:
            if pieces != "Out":
                if pieces.Position == moves[2:]:
                    pieces.Position = moves[0:2]

    return finalListOfMoves



def getMoveForThePiece(pieceType , piecePosition , tempBoard ):
    boardPosition = tempBoard
    possibleMovesForPiece = []
    if pieceType == "Pawn":
        print("Pawn")
        if boardPosition[int(piecePosition[1])][ord(piecePosition[0]) - 97][1] == 'W':
            if piecePosition[1] == "2":
                if checkMoveValidity(piecePosition + piecePosition[0] + str(int(piecePosition[1]) + 2) , boardPosition):
                    if not checkIfMovingIsBlocked(piecePosition , piecePoint[0] + str(int(piecePoint[1]) + 2)):
                        possibleMovesForPiece.append(piecePosition + piecePosition[0] + str(int(piecePosition[1]) + 2))
            if checkMoveValidity(piecePosition + piecePosition[0] + str(int(piecePosition[1]) + 1) , boardPosition):
                print("Move Valid")
                if not checkIfMovingIsBlocked(piecePosition , piecePosition[0] + str(int(piecePosition[1]) + 1) , pieceType):
                    possibleMovesForPiece.append(piecePosition + piecePosition[0] + str(int(piecePosition[1]) + 1))
        else:
            if piecePosition[1] == "7":
                if checkMoveValidity(piecePosition + piecePosition[0] + str(int(piecePosition[1]) - 2)):
                    if not checkIfMovingIsBlocked(piecePosition , piecePoint[0] + str(int(piecePoint[1]) - 2)):
                        possibleMovesForPiece.append(piecePosition + piecePosition[0] + str(int(piecePosition[1]) - 2))
            if checkMoveValidity(piecePosition + piecePosition[0] + str(int(piecePosition[1]) - 1)):
                if not checkIfMovingIsBlocked(piecePosition , piecePoint[0] + str(int(piecePoint[1]) - 1)):
                    possibleMovesForPiece.append(piecePosition + piecePosition[0] + str(int(piecePosition[1]) - 1))
    elif pieceType == "Knight":
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) + 2) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) + 2) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) + 2))
        
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) + 2) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) + 2) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) + 2))
        
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) - 2) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) - 2) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) - 2))
        
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) - 2) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) - 2) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) - 2))
        
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) + 2) + str(int(piecePosition[1]) + 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 2) + str(int(piecePosition[1]) + 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) + 2) + str(int(piecePosition[1]) + 1))
        
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) - 2) + str(int(piecePosition[1]) + 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) - 2) + str(int(piecePosition[1]) + 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) - 2) + str(int(piecePosition[1]) + 1))
        
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) + 2) + str(int(piecePosition[1]) - 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 2) + str(int(piecePosition[1]) - 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) + 2) + str(int(piecePosition[1]) - 1))
        
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) - 2) + str(int(piecePosition[1]) - 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) - 2) + str(int(piecePosition[1]) - 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) - 2) + str(int(piecePosition[1]) - 1))
    elif pieceType == "Bishop":
        currentPos = piecePosition
        xIncr = 1
        yIncr = 1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)

        currentPos = piecePosition
        xIncr = 1
        yIncr = -1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)
        
        currentPos = piecePosition
        xIncr = -1
        yIncr = 1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)
        
        currentPos = piecePosition
        xIncr = -1
        yIncr = -1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)
    elif pieceType == "Rook":
        currentPos = piecePosition
        xIncr = 1
        yIncr = 0
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)

        currentPos = piecePosition
        xIncr = 0
        yIncr = 1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)
    elif pieceType == "Queen":
        currentPos = piecePosition
        xIncr = 1
        yIncr = 1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)

        currentPos = piecePosition
        xIncr = 1
        yIncr = -1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)
        
        currentPos = piecePosition
        xIncr = -1
        yIncr = 1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)
        
        currentPos = piecePosition
        xIncr = -1
        yIncr = -1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)
        
        currentPos = piecePosition
        xIncr = 1
        yIncr = 0
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)

        currentPos = piecePosition
        xIncr = 0
        yIncr = 1
        while checkMoveValidity(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr))
            currentPos = chr(ord(currentPos[0]) + xIncr) + str(int(currentPos[1]) + yIncr)
    elif pieceType == "King":
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) + 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) + 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) + 1))

        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) - 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) - 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) - 1))
        
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) + 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) + 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) + 1))

        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) - 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) - 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) - 1))

        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) + 0) + str(int(piecePosition[1]) + 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 0) + str(int(piecePosition[1]) + 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) + 0) + str(int(piecePosition[1]) + 1))

        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) + 0) + str(int(piecePosition[1]) - 1) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 0) + str(int(piecePosition[1]) - 1) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) + 0) + str(int(piecePosition[1]) - 1))
        
        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) + 0) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) + 0) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) + 1) + str(int(piecePosition[1]) + 0))

        if checkMoveValidity(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) + 0) , boardPosition):
            if not checkIfMovingIsBlocked(piecePosition , chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) + 0) , pieceType):
                possibleMovesForPiece.append(piecePosition + chr(ord(piecePosition[0]) - 1) + str(int(piecePosition[1]) + 0))

    boardPosition = tempBoard
    return possibleMovesForPiece
     
def findAllPossibleValidMoves(team , boardPosition , oppTeam):
    possibleMoves = []

    for ele in team:
        if ele == "Out":
            pass
        else:
            pieceMoves = getMoveForThePiece(ele.pieceType , ele.Position , boardPosition)
            print(pieceMoves)
            for moves in pieceMoves:
                possibleMoves.append(moves)
            
    print(possibleMoves)
    return possibleMoves


def AnylizeBoardPosition(boardPosition):
    blackPoints = 0
    whitePoints = 0

    for i in range(9):
        if i == 0:
            pass 
        else:
            for j in range(8):
                if boardPosition[i][j] != "Empty":
                    if boardPosition[i][j][1] == "B":
                        pieceType = boardPosition[i][j][0]
                        if pieceType == "P":
                            blackPoints += 1
                        elif pieceType == "N":
                            blackPoints += 3
                        elif pieceType == "B":
                            blackPoints += 3
                        elif pieceType == "Q":
                            blackPoints += 10
                        elif pieceType == "R":
                            blackPoints += 5
                    else:
                        pieceType = boardPosition[i][j][0]
                        if pieceType == "P":
                            whitePoints += 1
                        elif pieceType == "N":
                            whitePoints += 3
                        elif pieceType == "B":
                            whitePoints += 3
                        elif pieceType == "Q":
                            whitePoints += 10
                        elif pieceType == "R":
                            whitePoints += 5
    
    if ourAI.color == "w":
        return whitePoints - blackPoints
    else:
        return blackPoints - whitePoints

    return 0 



    

def chooseTheBestMove(boardPosition , moveList):
    tempBoard = boardPosition
    moveChoiceWeight = []
    for moves in moveList:
        
        tempBoard = boardPosition
        makeTheMoveOnBoard(moves[0:2] , moves[2:] , getPieceTypeFromBoard(moves[0:2] , whitePieces ,blackPieces) , tempBoard , whitePieces , blackPieces , False , ourAI)
        moveChoiceWeight.append(AnylizeBoardPosition(tempBoard))

        currentList = []
        if ourAI.color == "w":
            currentList = whitePieces
        else:
            currentList = blackPieces

        for pieces in currentList:
            if pieces != "Out":
                if pieces.Position == moves[2:]:
                    pieces.Position = moves[0:2]

    n = 0
    for i in range(len(moveList)):
        if moveChoiceWeight[i] > moveChoiceWeight[n]:
            n = i
    return moveList[n]

def getAIMove():
    possibleMoves = []

    for i in range(8,0,-1):
        if(i == 0):
            pass
        else:
            for j in range(8):
                if(boardPosition[i][j] == "Empty"):
                    print(" '" , end = " ")
                else:
                    print(boardPosition[i][j] , end = " ")
            print()

    if ourAI.color == "w":
        possibleMoves = findAllPossibleValidMoves(whitePieces , boardPosition , blackPieces)
    else :
        possibleMoves = findAllPossibleValidMoves(blackPieces , boardPosition , whitePieces)

    print(len(possibleMoves))


    for i in range(8,0,-1):
        if(i == 0):
            pass
        else:
            for j in range(8):
                if(boardPosition[i][j] == "Empty"):
                    print(" '" , end = " ")
                else:
                    print(boardPosition[i][j] , end = " ")
            print()

    filterForIllegalMove(possibleMoves , boardPosition)

    for i in range(8,0,-1):
        if(i == 0):
            pass
        else:
            for j in range(8):
                if(boardPosition[i][j] == "Empty"):
                    print(" '" , end = " ")
                else:
                    print(boardPosition[i][j] , end = " ")
            print()

    print(len(possibleMoves))
    if len(possibleMoves) == 0:
        return "NONE"
    
    print(possibleMoves)
    moveCh = chooseTheBestMove(boardPosition , possibleMoves)
    # makeTheMoveOnBoard(possibleMoves[moveCh][0:2] , possibleMoves[moveCh][2:] , getPieceTypeFromBoard(possibleMoves[moveCh][2:] ,whitePieces , blackPieces) , boardPosition , whitePieces , blackPieces , False , ourAI)

    print(moveCh)
    return moveCh



def checkIfMovingIsBlocked(currentPos , finalPos , pieceType):
    if pieceType == "Knight":
        return False
    elif pieceType == "Pawn":
        print(currentPos , finalPos , pieceType)
        if currentPos[0] == finalPos[0] and boardPosition[int(finalPos[1])][ord(finalPos[0]) - 97] == "Empty":
            return False
        elif abs(ord(finalPos[0]) - ord(currentPos[0])) == 1:
            return False
    elif pieceType == "Bishop":
        xIncr = 1
        yIncr = 1
        if ord(finalPos[0]) - ord(currentPos[0]) < 0:
            yIncr = -1
        if int(finalPos[1]) - int(currentPos[1]) < 0:
            xIncr = -1
        for i in range(1 , abs(int(finalPos[1]) - int(currentPos[1]))):
            if boardPosition[int(currentPos[1]) + i*xIncr][ord(currentPos[0]) - 97 + i*yIncr] == "Empty":
                pass
            else:
                return True
        return False
    elif pieceType == "Rook":
        xIncr = 0
        yIncr = 0

        if ord(finalPos[0]) - ord(currentPos[0]) < 0:
            yIncr = -1
        elif ord(finalPos[0]) - ord(currentPos[0]) > 0:
            yIncr = 1
        else:
            yIncr = 0
        
        if int(finalPos[1]) - int(currentPos[1]) < 0:
            xIncr = -1
        elif int(finalPos[1]) - int(currentPos[1]) > 0:
            xIncr = 1
        else:
            xIncr = 0

        for i in range(1 , abs(int(finalPos[1]) - int(currentPos[1])) + abs(ord(finalPos[0]) - ord(currentPos[0]))):
            if boardPosition[int(currentPos[1]) + i*xIncr][ord(currentPos[0]) - 97 + i*yIncr] == "Empty":
                pass
            else:
                return True
        return False
    elif pieceType == "Queen":
        if int(finalPos[1]) == int(currentPos[1]) or ord(finalPos[0]) == ord(currentPos[0]):
            xIncr = 0
            yIncr = 0

            if ord(finalPos[0]) - ord(currentPos[0]) < 0:
                yIncr = -1
            elif ord(finalPos[0]) - ord(currentPos[0]) > 0:
                yIncr = 1
            else:
                yIncr = 0
            
            if int(finalPos[1]) - int(currentPos[1]) < 0:
                xIncr = -1
            elif int(finalPos[1]) - int(currentPos[1]) > 0:
                xIncr = 1
            else:
                xIncr = 0

            for i in range(1 , abs(int(finalPos[1]) - int(currentPos[1])) + abs(ord(finalPos[0]) - ord(currentPos[0]))):
                if boardPosition[int(currentPos[1]) + i*xIncr][ord(currentPos[0]) - 97 + i*yIncr] == "Empty":
                    pass
                else:
                    return True
            return False
        else:
            xIncr = 1
            yIncr = 1
            if ord(finalPos[0]) - ord(currentPos[0]) < 0:
                yIncr = -1
            if int(finalPos[1]) - int(currentPos[1]) < 0:
                xIncr = -1
            for i in range(1 , abs(int(finalPos[1]) - int(currentPos[1]))):
                if boardPosition[int(currentPos[1]) + i*xIncr][ord(currentPos[0]) - 97 + i*yIncr] == "Empty":
                    pass
                else:
                    return True
            return False
    else:
        return False

    return True

def eliminatePieceFromList(eliminationList , piecePos):
    print("Eliminating the Piece from the board")
    for i in range(16):
        if eliminationList[i] != "Out":
            if eliminationList[i].Position == piecePos:
                eliminationList[i] = "Out"
    
    

def isCheck(currentPos , finalPos , pieceType , boardPosition):
    if pieceType == "Pawn":
            if abs(ord(currentPos[0]) - ord(finalPos[0])) == 1 and abs(int(currentPos[1]) - int(finalPos[1])) == 1:
                pieceColor = boardPosition[int(currentPos[1])][ord(currentPos[0]) - 97][1]
                if(pieceColor == "W"):
                    if int(finalPos[1]) - int(currentPos[1]) == 1:
                        print(f"Check from the {pieceType}")
                        return True
                    else:
                        return False
                else:
                    if int(finalPos[1]) - int(currentPos[1]) == -1:
                        print(f"Check from the {pieceType}")
                        return True
                    else:
                        return False
            return False
    elif checkPositionalMovement(pieceType=pieceType , currentPos=currentPos , finalPos=finalPos):
        print(f"Possible for piece on {currentPos} to come the {finalPos}")
        if not checkIfMovingIsBlocked(currentPos=currentPos , finalPos=finalPos, pieceType=pieceType):
            print(currentPos , " " , finalPos)
            print(f"Check From the {pieceType}")
            return True 
    
    return False

def lookForCheckBoardAnalysis(boardPosition , attackingTeam , defendingTeamKingPos):
    print(f"Color of attacking Team {attackingTeam}")
    print("Started Checking if move is Legal")
    for i in range(9):
        if(i == 0):
            pass
        else:
            for j in range(8):
                if boardPosition[i][j] != "Empty":
                    if boardPosition[i][j][1] == attackingTeam:
                        if isCheck(chr(97+j) + str(i) , defendingTeamKingPos , getPieceTypeFromBoard(chr(97+j) + str(i) , whitePieces , blackPieces) ,boardPosition):
                            return True
                
    
    return False

def makeTheMoveOnBoard(currentPos , finalPos , pieceType , boardPosition , whitePieces , blackPieces , isOpponentMoving , ourAI):
    if(checkIfMovingIsBlocked(currentPos , finalPos , pieceType)):
        print("Movement is Blocked")
        return False
    
    
    if(boardPosition[int(finalPos[1])][ord(finalPos[0]) - 97] != "Empty"):
        if(ourAI.color == 'w'):
            eliminatePieceFromList(whitePieces , finalPos)
        else:
            eliminatePieceFromList(blackPieces , finalPos)

    print("Updating Board")

    boardPosition[int(finalPos[1])][ord(finalPos[0]) - 97] = boardPosition[int(currentPos[1])][ord(currentPos[0]) - 97]
    boardPosition[int(currentPos[1])][ord(currentPos[0]) - 97] = "Empty"


    defendingTeam = blackPieces
    attackingTeam = whitePieces

    currentList = []
    
    if ourAI.color == "w":
        if isOpponentMoving:
            attackingTeam = "W"
            defendingTeam = blackPieces
            currentList = blackPieces
        else:
            attackingTeam = "B"
            defendingTeam = whitePieces
            currentList = whitePieces
    else:
        if isOpponentMoving:
            attackingTeam = "B"
            defendingTeam = whitePieces
            currentList = whitePieces
        else:
            attackingTeam = "W"
            defendingTeam = blackPieces
            currentList = blackPieces

    for pieces in currentList:
        if pieces.Position == currentPos:
            pieces.Position = finalPos
    
    if lookForCheckBoardAnalysis(boardPosition , attackingTeam , defendingTeam[15].Position):
        print("Deupdating Board")
        print("Cant Place this Move On the Board , the King Is Vulnerable to check form The Opposite site")
        boardPosition[int(currentPos[1])][ord(currentPos[0]) - 97] = boardPosition[int(finalPos[1])][ord(finalPos[0]) - 97]
        boardPosition[int(finalPos[1])][ord(finalPos[0]) - 97] = "Empty"
        for pieces in currentList:
            if pieces != "Out":
                if pieces.Position == finalPos:
                    pieces.Position = currentPos
        return False

    print("Done Checking the board All fine No Illegal Move")

    


    return True


def getPieceTypeFromBoard(str , whitePieces , blackPieces):
    pieceName = boardPosition[int(str[1])][ord(str[0]) - 97][0]
    if pieceName == "K":
        return "King"
    elif pieceName == "Q":
        return "Queen"
    elif pieceName == "R":
        return "Rook"
    elif pieceName == "B":
        return "Bishop"
    elif pieceName == "P":
        return "Pawn"
    elif pieceName == "N":
        return "Knight"
        



    



class ChessAI:
    def make_move(self) -> str:
        move = getAIMove()
        if move == "NONE":
            pass
        else:
            for i in range(8,0,-1):
                if(i == 0):
                    pass
                else:
                    for j in range(8):
                        if(boardPosition[i][j] == "Empty"):
                            print(" '" , end = " ")
                        else:
                            print(boardPosition[i][j] , end = " ")
                    print()
            print("Making Move on Board")
            print(move)
            if makeTheMoveOnBoard(move[0:2] , move[2:] , getPieceTypeFromBoard(move[0:2] , whitePieces , blackPieces) , boardPosition , whitePieces , blackPieces , False , ourAI):
                pass
        return move

    def add_move(self, move: str) -> None:
        if(checkMoveValidity(str=move , boardPosition=boardPosition) == False):
            return False
        if not makeTheMoveOnBoard(currentPos=move[0:2] , finalPos=move[2:] , pieceType = getPieceTypeFromBoard(move[0:2] , whitePieces , blackPieces) ,boardPosition=boardPosition ,whitePieces=whitePieces , blackPieces=blackPieces , isOpponentMoving=True , ourAI=ourAI):
            print("Cant Make the Move on Board")
            return False
        return True
        

    def check_for_draw(self):
        if AnylizeBoardPosition(boardPosition) <= 0:
            return True
        else:
            return False
        
    def __init__(self, color: str):
	    self.color = color # either "w" or "b"



class Piece:
    Position = ""
    pieceType = ""

    def __init__(self , Position = "" , pieceType = ""):
         self.Position = Position
         self.pieceType = pieceType




boardPosition = [["", "", "", "", "", "", "", ""], ["RW", "NW", "BW", "QW", "KW", "BW", "NW", "RW"], ["PW", "PW", "PW", "PW", "PW", "PW", "PW", "PW"], ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"], ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"], ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"], ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"], ["PB", "PB", "PB", "PB", "PB", "PB", "PB", "PB"] ,["RB", "NB", "BB", "QB", "KB", "BB", "NB", "RB"]]
whitePieces = [Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("","")]
blackPieces = [Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("",""),Piece("","")]



for i in range(16):
    if i <= 7:
        whitePieces[i].Position = chr(97 + i) + "2"
        whitePieces[i].pieceType = "Pawn"
    elif i > 7 and i <= 9 :
        whitePieces[i].Position = chr(96 + 3*(i-7)) + "1"
        whitePieces[i].pieceType = "Bishop"
    elif i > 9 and i <= 11:
        whitePieces[i].Position = chr(93 + 5*(i-9)) + "1"
        whitePieces[i].pieceType = "Knight"
    elif i > 11 and i <= 13:
        whitePieces[i].Position = chr(90 + 7*(i-11)) + "1"
        whitePieces[i].pieceType = "Rook"
    elif i == 14:
        whitePieces[i].Position = "d1"
        whitePieces[i].pieceType = "Queen"
    else:
        whitePieces[i].Position = "e1"
        whitePieces[i].pieceType = "King"


for i in range(16):
    if i <= 7:
        blackPieces[i].Position = chr(97 + i) + "7"
        blackPieces[i].pieceType = "Pawn"
    elif i > 7 and i <= 9 :
        blackPieces[i].Position = chr(96 + 3*(i-7)) + "8"
        blackPieces[i].pieceType = "Bishop"
    elif i > 9 and i <= 11:
        blackPieces[i].Position = chr(93 + 5*(i-9)) + "8"
        blackPieces[i].pieceType = "Knight"
    elif i > 11 and i <= 13:
        blackPieces[i].Position = chr(90 + 7*(i-11)) + "8"
        blackPieces[i].pieceType = "Rook"
    elif i == 14:
        blackPieces[i].Position = "d8"
        blackPieces[i].pieceType = "Queen"
    else:
        blackPieces[i].Position = "e8"
        blackPieces[i].pieceType = "King"



piecePoint = {'Queen' : 10 , "Rook" : 5 , "Bishop" : 3 , "Knight" : 3 , "Pawn" : 1 , "King" : 100}

blackIllegalCount = 2
whiteIllegalCount = 50




challengerMove = True


ourAIColor = input("Enter The Color For AI (w/b) :  ")
ourAI = ChessAI(ourAIColor)

if ourAIColor == "w":
    makeTheMoveOnBoard("e2" , "e4" , "Pawn" , boardPosition , whitePieces , blackPieces , False , ourAI)


print()
print("To Resign Please Put The Input As : Resign")
print("To Ask For a Draw Please Put The Input As : Draw")
print()


gameWinner  = "our 'Challenger'"
gameON = True

while gameON:

    challengerMove = True
    
    for i in range(8,0,-1):
        if(i == 0):
            pass
        else:
            for j in range(8):
                if(boardPosition[i][j] == "Empty"):
                    print(" '" , end = " ")
                else:
                    print(boardPosition[i][j] , end = " ")
            print()

    print()
    print()

    while True:
        userMove = input("Enter Your Move : ")
        if(userMove == "Resign"):
            print()
            print("The Challenger has Resigned!!")
            gameWinner = "our 'AI'"
            gameON = False
            break
        elif(userMove == "Draw"):
            print()
            print("The Challenger Has Asked For A Draw")
            if(ourAI.check_for_draw()):
                print("The Draw Has Been Accepted By The AI , Smart Choice By The AI")
                gameWinner = "Draw"
                gameON = False
                break
            else:
                print("The Draw Has Been Neglected By The AI , Maybe The Challenger Would Have To Try Harder")
                print()
        else:
            if(not ourAI.add_move(userMove)):
                print()
                print(f"It's An Illegal Move Given By The Challenge")
                if ourAI.color == 'w':
                    blackIllegalCount -= 1
                    if(blackIllegalCount == 0):
                        gameWinner = "our 'AI'"
                        gameON = False
                        print("Unfortunately The Illegal Move Counter Has Been Up for The Challenger")
                        print("Better Luck Next Time , Kiddo !!")
                        print()
                        break
                else:
                    whiteIllegalCount -= 1
                    if(whiteIllegalCount == 0):
                        gameWinner = "our 'AI'"
                        gameON = False
                        print("Unfortunately The Illegal Move Counter Has Been Up for The Challenger")
                        print("Better Luck Next Time , Kiddo !!")
                        print()
                        break
                print()
                
            else:
                break

    challengerMove = False    
    if(gameON):
        ourAI.make_move()


    

print()
if(gameWinner != "Draw"):
    print(f"Winner of this game is {gameWinner}")
else:
    print("This Game Has Come To A Draw , Congrats To Both The Challenger And Our AI")
print("Thanks For Playing !!")

