# Modificable para mejor performance. Los valores elegidos son totalmente especulativos.
DicOfRiskToleranceByProbOfWinningEnvido = {
    0.4: 0,
    0.5: 2,
    0.6: 3,
    0.75: 4,
    0.8: 5,
    0.85: 7,
    0.95: 15,
}


def shouldEscalateEnvidoPoints(probOfWinningEnvido, gameScore, currentPointsAtPlay, lastEnvidoPointsAtPlay):
    # gameScore assumes [0] is the player making the desicion
    """ 
    Returns:
    -15 if should decline
    0 if should accept
    x if wants to escalate to x points.
    15 if falta envido.
     """
    if (gameScore[0]+currentPointsAtPlay > 15):
        # Evita regalar puntos extra cuando el falta envido acorta los posibles puntos que gana el otro.
        if (gameScore[0] >= gameScore[1]):
            return 15
        else:
            # Aceptando porque el otro es un pelotudo que no sabe sumar
            return 0

    if (gameScore[1]+lastEnvidoPointsAtPlay >= 15):
        return 0

    # Elige el valor mas cercano en el diccionaria de risktaking correspondiente a la probabilidad de ganar el envido
    desiredPoints = DicOfRiskToleranceByProbOfWinningEnvido[min(
        DicOfRiskToleranceByProbOfWinningEnvido, key=lambda x: abs(x-probOfWinningEnvido))]

    if (desiredPoints < currentPointsAtPlay):
        return -15
    elif (desiredPoints == currentPointsAtPlay):
        return 0
    else:
        return desiredPoints
