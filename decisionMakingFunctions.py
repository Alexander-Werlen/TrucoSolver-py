from GTO.vonNeumannModels import envidoVonNeumann, trucoVonNeumann


def shouldEscalateTrucoPoints(probWinTruco, gamescore, trucoPointsAtBet, trucoPointsAtPlay):
    """ 
    Returns:
    -15 if should decline
    0 if should accept
    x if wants to escalate to x points.
     """
    wantsToAccept = trucoVonNeumann(
        False, probWinTruco, trucoPointsAtPlay, trucoPointsAtBet)

    if (wantsToAccept):
        if (trucoPointsAtBet == 4):
            return 0
        wantsToRaise = envidoVonNeumann(
            True, probWinTruco, trucoPointsAtBet, None)
        if (wantsToRaise):
            desiredPoints = trucoPointsAtBet+1
        else:
            desiredPoints = 0
    else:
        desiredPoints = -15

    return desiredPoints


def shouldEscalateEnvidoPoints(probOfWinningEnvido, gameScore, envidoPointsAtBet, envidoPointsAtPlay, gameContext):
    # gameScore assumes [0] is the player making the desicion
    """ 
    Returns:
    -15 if should decline
    0 if should accept
    x if wants to escalate to x points.
    15 if falta envido.
     """
    if (gameScore[0]+envidoPointsAtPlay >= 15):
        # Evita regalar puntos extra cuando el falta envido acorta los posibles puntos que gana el otro.
        if (gameScore[0] >= gameScore[1]):
            return 15
        else:
            # Aceptando porque el otro es un pelotudo que no sabe sumar
            return 0

    if (gameScore[1]+envidoPointsAtPlay >= 15):
        return 0

    wantsToAccept, _ = envidoVonNeumann(
        False, probOfWinningEnvido, envidoPointsAtPlay, envidoPointsAtBet)

    if (wantsToAccept):
        if (gameContext.onFaltaEnvido):
            return 0
        wantsToRaise, bet = envidoVonNeumann(
            True, probOfWinningEnvido, envidoPointsAtBet, None)
        if (wantsToRaise):
            desiredPoints = bet
        else:
            desiredPoints = 0
    else:
        desiredPoints = -15

    return desiredPoints
