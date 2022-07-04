from miscelaneos import RanksDictionary
from operator import itemgetter
import copy


def functionScore(cardP1, cardP2):  # oponent wants to maximize
    dif = RanksDictionary[cardP1] - RanksDictionary[cardP2]
    if (dif == 0):
        return 39/2
    elif (dif > 0):
        return(dif)
    else:
        return(dif+39)


def whichCardMinimizesFunctionScore(myHand, othersHand):
    # output: para cada carta de handP1 un puntaje (normalizado a 1). Se debería de intentar minimizar ese puntaje
    """
    Inputs: Player has to be the one throwing the card first
    1) myHand: ls[x<=3] (cards I can throw)
    2) othersHand: ls[x<=3] (cards Other can throw)
     """

    puntajes = []
    for myCard in myHand:
        puntajes.append(max([functionScore(myCard, card)
                        for card in othersHand]))

    # Dando 1 si es la mejor, 0 si no
    return [(1 if punto == min(puntajes) else 0) for punto in puntajes]


def probOfWinningTrucoGivenHand(game):
    counterWins = 0

    for othersHand in game.possibleHandsP2:
        if P1HandWinsTruco(game, othersHand):
            counterWins += 1

    return counterWins/len(game.possibleHandsP2)


def P1WinsTrucoGivenThrownCard(game, handToPlayAgainst, cardToThrowFirst):
    handP1 = copy.deepcopy(game.handP1)
    handP2 = copy.deepcopy(handToPlayAgainst)
    currentTrucoScore = copy.deepcopy(game.currentTrucoScore)
    cardsInMesa = copy.deepcopy(game.cardsInMesa)
    currentTrucoStage = copy.deepcopy(game.currentTrucoStage)
    whoWonPrimera = copy.deepcopy(game.whoWonPrimera)
    isP1Turn = copy.deepcopy(game.isP1TrucoTurn)
    whoIsMano = copy.deepcopy(game.whoIsMano)

    while ((currentTrucoScore[0] < 2 and currentTrucoScore[1] < 2) or (currentTrucoScore[0] == 2 and currentTrucoScore[1] == 2 and whoWonPrimera is None)):
        if (isP1Turn):
            if (cardToThrowFirst is not None):
                cardToThrow = cardToThrowFirst
                cardToThrowFirst = None

            elif cardsInMesa[currentTrucoStage][1] is None:  # Tenes que iniciar
                _, idx = max((_, idx) for (idx, _) in enumerate(
                    whichCardMinimizesFunctionScore(handP1, handP2)))  # gets index of card which minimizes scoreLoss
                cardToThrow = handP1[idx]

            else:  # Tenes que responder
                auxiliarHand = copy.deepcopy(handP1)
                while(len(auxiliarHand) > 0):
                    _, idx = max((_, idx) for (idx, _) in enumerate(
                        whichCardMinimizesFunctionScore(auxiliarHand, [cardsInMesa[currentTrucoStage][1]])))  # gets index of card which minimizes scoreLoss
                    cardToThrow = auxiliarHand[idx]

                    # If pierde la RONDA tirando esa carta, entonces prueba con las otras.
                    if ((RanksDictionary[cardToThrow] < RanksDictionary[cardsInMesa[currentTrucoStage][1]] and currentTrucoScore[1] > 0)):
                        auxiliarHand.remove(cardToThrow)
                    else:
                        break

            handP1.remove(cardToThrow)
            cardsInMesa[currentTrucoStage][0] = cardToThrow
            isP1Turn = False

        else:  # juega P2
            if cardsInMesa[currentTrucoStage][0] is None:  # Tenes que iniciar
                _, idx = max((_, idx) for (idx, _) in enumerate(
                    whichCardMinimizesFunctionScore(handP2, handP1)))  # gets index of card which minimizes scoreLoss
                cardToThrow = handP2[idx]

            else:  # Tenes que responder
                auxiliarHand = copy.deepcopy(handP2)
                while(len(auxiliarHand) > 0):
                    _, idx = max((_, idx) for (idx, _) in enumerate(
                        whichCardMinimizesFunctionScore(auxiliarHand, [cardsInMesa[currentTrucoStage][0]])))  # gets index of card which minimizes scoreLoss
                    cardToThrow = auxiliarHand[idx]

                    # If pierde la RONDA tirando esa carta, entonces prueba con las otras.
                    if ((RanksDictionary[cardToThrow] < RanksDictionary[cardsInMesa[currentTrucoStage][0]] and currentTrucoScore[0] > 0)):
                        auxiliarHand.remove(cardToThrow)
                    else:
                        break

            handP2.remove(cardToThrow)
            cardsInMesa[currentTrucoStage][1] = cardToThrow
            isP1Turn = True

        # Actualizando trucoStage and points
        if (cardsInMesa[currentTrucoStage][0] is not None and cardsInMesa[currentTrucoStage][1] is not None):
            if RanksDictionary[cardsInMesa[currentTrucoStage][0]] > RanksDictionary[cardsInMesa[currentTrucoStage][1]]:
                currentTrucoScore[0] += 1
                isP1Turn = True

                if whoWonPrimera is None:
                    whoWonPrimera = True

            elif RanksDictionary[cardsInMesa[currentTrucoStage][0]] < RanksDictionary[cardsInMesa[currentTrucoStage][1]]:
                currentTrucoScore[1] += 1
                isP1Turn = False

                if whoWonPrimera is None:
                    whoWonPrimera = False
            else:
                currentTrucoScore[0] += 1
                currentTrucoScore[1] += 1
                isP1Turn = whoIsMano

            currentTrucoStage += 1

    if currentTrucoScore[0] == currentTrucoScore[1]:
        return whoIsMano  # Si empardan todas gana el que es mano

    if currentTrucoScore[0] > currentTrucoScore[1]:
        return True
    else:
        return False


def bestCardToThrow(game):
    probs = []

    for card in game.handP1:
        counterWins = 0
        for othersHand in game.possibleHandsP2:
            if P1WinsTrucoGivenThrownCard(game, copy.deepcopy(othersHand), card):
                counterWins += 1
        probs.append((card, counterWins/len(game.possibleHandsP2)))

    return max(probs, key=itemgetter(1))[0]


def P1HandWinsTruco(game, handToPlayAgainst):
    handP1 = copy.deepcopy(game.handP1)
    handP2 = copy.deepcopy(handToPlayAgainst)
    currentTrucoScore = copy.deepcopy(game.currentTrucoScore)
    cardsInMesa = copy.deepcopy(game.cardsInMesa)
    currentTrucoStage = copy.deepcopy(game.currentTrucoStage)
    whoWonPrimera = copy.deepcopy(game.whoWonPrimera)
    isP1Turn = copy.deepcopy(game.isP1TrucoTurn)
    whoIsMano = copy.deepcopy(game.whoIsMano)

    while ((currentTrucoScore[0] < 2 and currentTrucoScore[1] < 2) or (currentTrucoScore[0] == 2 and currentTrucoScore[1] == 2 and whoWonPrimera is None)):
        if (isP1Turn):
            if cardsInMesa[currentTrucoStage][1] is None:  # Tenes que iniciar
                idx = whichCardMinimizesFunctionScore(handP1, handP2).index(1)
                cardToThrow = handP1[idx]

            else:  # Tenes que responder
                auxiliarHand = copy.deepcopy(handP1)
                while(len(auxiliarHand) > 0):
                    idx = whichCardMinimizesFunctionScore(
                        auxiliarHand, [cardsInMesa[currentTrucoStage][1]]).index(1)

                    cardToThrow = auxiliarHand[idx]

                    # If pierde la RONDA tirando esa carta, entonces prueba con las otras.
                    if ((RanksDictionary[cardToThrow] < RanksDictionary[cardsInMesa[currentTrucoStage][1]] and currentTrucoScore[1] > 0)):
                        auxiliarHand.remove(cardToThrow)
                    else:
                        break

            handP1.remove(cardToThrow)
            cardsInMesa[currentTrucoStage][0] = cardToThrow
            isP1Turn = False

        else:  # juega P2
            if cardsInMesa[currentTrucoStage][0] is None:  # Tenes que iniciar
                idx = whichCardMinimizesFunctionScore(handP2, handP1).index(1)
                cardToThrow = handP2[idx]

            else:  # Tenes que responder
                auxiliarHand = copy.deepcopy(handP2)
                while(len(auxiliarHand) > 0):
                    idx = whichCardMinimizesFunctionScore(
                        auxiliarHand, [cardsInMesa[currentTrucoStage][0]]).index(1)
                    cardToThrow = auxiliarHand[idx]

                    # If pierde la RONDA tirando esa carta, entonces prueba con las otras.
                    if ((RanksDictionary[cardToThrow] < RanksDictionary[cardsInMesa[currentTrucoStage][0]] and currentTrucoScore[0] > 0)):
                        auxiliarHand.remove(cardToThrow)
                    else:
                        break

            handP2.remove(cardToThrow)
            cardsInMesa[currentTrucoStage][1] = cardToThrow
            isP1Turn = True

        # Actualizando trucoStage and points
        if (cardsInMesa[currentTrucoStage][0] is not None and cardsInMesa[currentTrucoStage][1] is not None):
            if RanksDictionary[cardsInMesa[currentTrucoStage][0]] > RanksDictionary[cardsInMesa[currentTrucoStage][1]]:
                currentTrucoScore[0] += 1
                isP1Turn = True

                if whoWonPrimera is None:
                    whoWonPrimera = True

            elif RanksDictionary[cardsInMesa[currentTrucoStage][0]] < RanksDictionary[cardsInMesa[currentTrucoStage][1]]:
                currentTrucoScore[1] += 1
                isP1Turn = False

                if whoWonPrimera is None:
                    whoWonPrimera = False
            else:
                currentTrucoScore[0] += 1
                currentTrucoScore[1] += 1
                isP1Turn = whoIsMano

            currentTrucoStage += 1

    if currentTrucoScore[0] == currentTrucoScore[1]:
        return whoIsMano  # Si empardan todas gana el que es mano

    if currentTrucoScore[0] > currentTrucoScore[1]:
        return True
    else:
        return False
