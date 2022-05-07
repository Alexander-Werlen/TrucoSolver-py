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
