import random as random
import itertools

""" 
Notacion:
<numero de la carta><primera letra del palo de la carta>
     
"""

RanksDictionary = {
    "1e": 1,
    "1b": 2,
    "7e": 3,
    "7o": 4,
    "3c": 5,
    "3o": 5,
    "3b": 5,
    "3e": 5,
    "2c": 6,
    "2o": 6,
    "2b": 6,
    "2e": 6,
    "1c": 7,
    "1o": 7,
    "12c": 8,
    "12o": 8,
    "12b": 8,
    "12e": 8,
    "11c": 9,
    "11o": 9,
    "11b": 9,
    "11e": 9,
    "10c": 10,
    "10o": 10,
    "10b": 10,
    "10e": 10,
    "7c": 11,
    "7b": 11,
    "6c": 12,
    "6o": 12,
    "6b": 12,
    "6e": 12,
    "5c": 13,
    "5o": 13,
    "5b": 13,
    "5e": 13,
    "4c": 14,
    "4o": 14,
    "4b": 14,
    "4e": 14

}

EnvidoValuesDictionary = {
    "12c": 0,
    "12o": 0,
    "12b": 0,
    "12e": 0,
    "11c": 0,
    "11o": 0,
    "11b": 0,
    "11e": 0,
    "10c": 0,
    "10o": 0,
    "10b": 0,
    "10e": 0,
    "1c": 1,
    "1o": 1,
    "1b": 1,
    "1e": 1,
    "2c": 2,
    "2o": 2,
    "2b": 2,
    "2e": 2,
    "3c": 3,
    "3o": 3,
    "3b": 3,
    "3e": 3,
    "7c": 7,
    "7o": 7,
    "7b": 7,
    "7e": 7,
    "6c": 6,
    "6o": 6,
    "6b": 6,
    "6e": 6,
    "5c": 5,
    "5o": 5,
    "5b": 5,
    "5e": 5,
    "4c": 4,
    "4o": 4,
    "4b": 4,
    "4e": 4

}

PaloDeCartaDictionary = {
    # c:1, o:2, b:3, e:4
    "12c": 1,
    "12o": 2,
    "12b": 3,
    "12e": 4,
    "11c": 1,
    "11o": 2,
    "11b": 3,
    "11e": 4,
    "10c": 1,
    "10o": 2,
    "10b": 3,
    "10e": 4,
    "1c": 1,
    "1o": 2,
    "1b": 3,
    "1e": 4,
    "2c": 1,
    "2o": 2,
    "2b": 3,
    "2e": 4,
    "3c": 1,
    "3o": 2,
    "3b": 3,
    "3e": 4,
    "7c": 1,
    "7o": 2,
    "7b": 3,
    "7e": 4,
    "6c": 1,
    "6o": 2,
    "6b": 3,
    "6e": 4,
    "5c": 1,
    "5o": 2,
    "5b": 3,
    "5e": 4,
    "4c": 1,
    "4o": 2,
    "4b": 3,
    "4e": 4
}

deck = [
    "1e",
    "1b",
    "7e",
    "7o",
    "3c",
    "3o",
    "3b",
    "3e",
    "2c",
    "2o",
    "2b",
    "2e",
    "1c",
    "1o",
    "12c",
    "12o",
    "12b",
    "12e",
    "11c",
    "11o",
    "11b",
    "11e",
    "10c",
    "10o",
    "10b",
    "10e",
    "7c",
    "7b",
    "6c",
    "6o",
    "6b",
    "6e",
    "5c",
    "5o",
    "5b",
    "5e",
    "4c",
    "4o",
    "4b",
    "4e"
]


def repartir():

    currentDeck = deck[:]
    handP1 = []
    handP2 = []

    # Choosing cards
    givingCardToP1 = True
    for i in range(6):
        newCard = random.choice(currentDeck)
        currentDeck.remove(newCard)

        if (givingCardToP1):
            handP1.append(newCard)
        else:
            handP2.append(newCard)

        givingCardToP1 = not givingCardToP1

    return handP1, handP2, currentDeck


def calculateProbabilityOfWinningEnvido(myHand, othersKnownHand, IamMano):

    # Inputs: myHand= lista de tus cartas; othersKnownHand= lista de las cartas que mostró el oponente; IamMano= bool True if myHand is mano, False if not

    possibleCardsLeft = deck[:]

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


def winsEnvido(myHand, othersHand, IamMano):
    # Inputs: myHand=list of my 3 cards, othersHand=listo of others 3 cards, IamMano=bool true if myHand is mano, false if not.
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


###
iters = 100
counterWins = 0
playedCounter = 0
suma = 0

for i in range(iters):
    handP1, handP2, currentDeck = repartir()

    if(calculateProbabilityOfWinningEnvido(handP1, [], True) > 0.1):
        playedCounter += 1

        if(winsEnvido(handP1, handP2, True)[0]):
            counterWins += 1


print(playedCounter)
print(counterWins/playedCounter)
