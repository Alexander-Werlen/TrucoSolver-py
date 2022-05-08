from miscelaneos import RanksDictionary


def functionScore(cardP1, cardP2):  # oponent wants to maximize
    dif = RanksDictionary[cardP1] - RanksDictionary[cardP2]
    if (dif > 0):
        return(dif)
    else:
        # Funcion a revisar para conseguir mejor performance. Pero creo que está bien
        return(dif+39)


# Generalizar para que de igual la cantidad de cartas que tiene cada mano
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
    return [1 if punto == min(puntajes) else 0 for punto in puntajes]


def getProbOfMinimizingExpectedFunctionScore(myHand, othersPossibleHands):
    # Returns list of Probability of each card of having the least Escore. Best is the highest
    """
    Assumes you are the one throwing first
     """
    timesCardIsBest = [0 for _ in myHand]

    for possibleHand in othersPossibleHands:
        for i, punto in enumerate(whichCardMinimizesFunctionScore(myHand, possibleHand)):
            timesCardIsBest[i] += punto

    # Normalizando valores a 1
    return [float(x)/sum(timesCardIsBest) for x in timesCardIsBest]


def probOfWinningTrucoGivenHand(myHand, othersPossibleHands, trucoScore, myTurn, IamMano, cardsInMesa, IwonPrimera=None):
    counterWins = 0

    for othersHand in othersPossibleHands:
        if myHandWinsTruco(myHand[:], othersHand[:], trucoScore[:], myTurn, IamMano, cardsInMesa[:], IwonPrimera):
            counterWins += 1

    return counterWins/len(othersPossibleHands)


def myHandWinsTruco(myHand, othersHand, trucoScore, myTurn, IamMano, cardsInMesa, IwonPrimera=None):

    while ((trucoScore[0] < 2 and trucoScore[1] < 2) or (trucoScore[0] == 2 and trucoScore[1] == 2 and IwonPrimera is None)):
        if (myTurn):
            # Si me toca tirar carta antes que el oponente elegimos para tirar la carta que miminice ScoreLoss
            if cardsInMesa[-1][1] is None:
                _, idx = max((_, idx) for (idx, _) in enumerate(
                    whichCardMinimizesFunctionScore(myHand, othersHand)))  # gets index of card which minimizes scoreLoss
                cardToThrow = myHand[idx]

            else:
                auxiliarHand = myHand[:]
                while(len(auxiliarHand) > 0):
                    _, idx = max((_, idx) for (idx, _) in enumerate(
                        whichCardMinimizesFunctionScore(auxiliarHand, [cardsInMesa[-1][1]])))  # gets index of card which minimizes scoreLoss
                    cardToThrow = auxiliarHand[idx]

                    # If pierde la RONDA tirando esa carta, entonces prueba con las otras.
                    if ((RanksDictionary[cardToThrow] < RanksDictionary[cardsInMesa[-1][1]] and trucoScore[1] > 0)):
                        auxiliarHand.remove(cardToThrow)
                    else:
                        break

            myHand.remove(cardToThrow)
            cardsInMesa[-1][0] = cardToThrow
            myTurn = False  # Termina el turno

        else:
            # Juega other
            if cardsInMesa[-1][0] is None:
                _, idx = max((_, idx) for (idx, _) in enumerate(
                    whichCardMinimizesFunctionScore(othersHand, myHand)))  # gets index of card which minimizes scoreLoss
                cardToThrow = othersHand[idx]

            else:
                auxiliarHand = othersHand[:]
                while(len(auxiliarHand) > 0):
                    _, idx = max((_, idx) for (idx, _) in enumerate(
                        whichCardMinimizesFunctionScore(auxiliarHand, [cardsInMesa[-1][0]])))  # gets index of card which minimizes scoreLoss
                    cardToThrow = auxiliarHand[idx]

                    # If pierde la RONDA tirando esa carta, entonces prueba con las otras.
                    if ((RanksDictionary[cardToThrow] < RanksDictionary[cardsInMesa[-1][0]] and trucoScore[0] > 0)):
                        auxiliarHand.remove(cardToThrow)
                    else:
                        break

            othersHand.remove(cardToThrow)
            cardsInMesa[-1][1] = cardToThrow
            myTurn = True  # Termina el turno

        if (cardsInMesa[-1][0] is not None and cardsInMesa[-1][1] is not None):
            if RanksDictionary[cardsInMesa[-1][0]] > RanksDictionary[cardsInMesa[-1][1]]:
                trucoScore[0] += 1
                myTurn = True

                if IwonPrimera is None:
                    IwonPrimera = True
            elif RanksDictionary[cardsInMesa[-1][0]] < RanksDictionary[cardsInMesa[-1][1]]:
                trucoScore[1] += 1
                myTurn = False

                if IwonPrimera is None:
                    IwonPrimera = False
            else:
                trucoScore[0] += 1
                trucoScore[1] += 1
                myTurn = IamMano

            cardsInMesa.append([None, None])

    if trucoScore[0] == trucoScore[1]:
        return IamMano  # Si empardan todas gana el que es mano

    if trucoScore[0] > trucoScore[1]:
        return True
    else:
        return False
