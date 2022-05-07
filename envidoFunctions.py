from miscelaneos import PaloDeCartaDictionary, EnvidoValuesDictionary


def calculateEnvidoPoints(hand):
    hasEnvido = False
    mayorEnvido = 0

    if (PaloDeCartaDictionary[hand[0]] == PaloDeCartaDictionary[hand[1]]):
        hasEnvido = True
        mayorEnvido = EnvidoValuesDictionary[hand[0]
                                             ] + EnvidoValuesDictionary[hand[1]]

    if (PaloDeCartaDictionary[hand[1]] == PaloDeCartaDictionary[hand[2]]):
        hasEnvido = True
        newEnvidoValue = EnvidoValuesDictionary[hand[1]
                                                ] + EnvidoValuesDictionary[hand[2]]

        if(newEnvidoValue > mayorEnvido):
            mayorEnvido = newEnvidoValue

    if (PaloDeCartaDictionary[hand[2]] == PaloDeCartaDictionary[hand[0]]):
        hasEnvido = True
        newEnvidoValue = EnvidoValuesDictionary[hand[2]
                                                ] + EnvidoValuesDictionary[hand[0]]

        if(newEnvidoValue > mayorEnvido):
            mayorEnvido = newEnvidoValue

    if (not hasEnvido):
        for i in range(3):
            newEnvidoValue = EnvidoValuesDictionary[hand[i]]
            if(newEnvidoValue > mayorEnvido):
                mayorEnvido = newEnvidoValue
    else:
        mayorEnvido += 20

    return mayorEnvido


def winsEnvido(myHand, othersHand, IamMano):
    # Inputs: myHand=list of my 3 cards, othersHand=list of others 3 cards, IamMano=bool true if myHand is mano, false if not.
    # Output: true if myHand wins, false if othersHand wins  ;  miMayorEnvido ; othersMayorEnvido

    miMayorEnvido = calculateEnvidoPoints(myHand)
    othersMayorEnvido = calculateEnvidoPoints(othersHand)

    # Determining who wins

    if (miMayorEnvido == othersMayorEnvido):
        if (IamMano):
            return True, miMayorEnvido, othersMayorEnvido  # myHand Wins
        else:
            return False, miMayorEnvido, othersMayorEnvido

    elif(miMayorEnvido > othersMayorEnvido):
        return True, miMayorEnvido, othersMayorEnvido
    else:
        return False, miMayorEnvido, othersMayorEnvido


# Reescribir para que de input se den las posibles manos del oponente en vez de hacer esa operación acá adentro con la carta que mostró
def calculateProbabilityOfWinningEnvido(myHand, othersPossibleHands, IamMano):
    # Inputs: myHand= lista de tus cartas; othersPossibleHands= lista de posibles manos del oponente; IamMano= bool True if myHand is mano, False if not

    possibleCardsLeft = copy.copy(deck)

    # Redundante porque lo podría hacer en otro lado
    for i in range(3):
        possibleCardsLeft.remove(myHand[i])

    for i in range(len(othersKnownHand)):
        possibleCardsLeft.remove(othersKnownHand[i])

    othersPossibleHands = [list(x) for x in itertools.combinations(
        possibleCardsLeft, 3-len(othersKnownHand))]

    # Si sabemos una carta entonces la ponemos en la lista de posibles manos porque no la estabamos teniendo en cuenta.
    if (othersKnownHand):
        for i in othersPossibleHands:
            i.append(othersKnownHand[0])

    winsCounter = 0
    for mano in othersPossibleHands:
        if (winsEnvido(myHand, mano, IamMano)[0]):
            winsCounter += 1

    return winsCounter/(len(othersPossibleHands))
