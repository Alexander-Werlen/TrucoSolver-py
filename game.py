from envidoFunctions import *
from trucoFunctions import *
from funcionesBasicas import *
from decisionMakingFunctions import *
import random
import itertools


def main():

    # definiendo variables globales
    global gameScore
    gameScore = [0, 0]  # P1[0] P2[1]
    global knownHandOfP1
    global knownHandOfP2
    global possibleHandsOfP1
    global possibleHandsOfP2
    global handP1
    global handP2
    global currentDeck
    global whoIsMano
    global trucoScore

    # Defining who is mano. True is P1, False is P2
    P1plays = random.choice([True, False])
    whoIsMano = P1plays

    while(not gameEnded(gameScore)):
        print("Empezó la partida")
        print("-----------------")
        # Empezar ronda
        handP1, handP2, currentDeck = repartir()
        # para usarlo en funciones invertir el orden como corresponda (se asume que el jugador evaluando la función es ls[0])
        trucoScore = [0, 0]
        cardsInMesa = [[None, None]]  # primera siempre es de P1, segunda de P2
        # Auxiliares
        whoWonPrimera = None
        isPlayingEnvido = False  # True if P1, False if P2
        envidoHasAlredyBeenPlayed = False
        lastEnvidoPointsAtPlay = 0
        envidoPointsAtPlay = 0
        trucoPointsAtPlay = 1
        # Actualizando conocimiento de los jugadores
        knownHandOfP1 = [[], None]
        knownHandOfP2 = [[], None]

        possibleHandsOfP1 = [list(x) for x in itertools.combinations(
            currentDeck+handP1, 3)]
        possibleHandsOfP2 = [list(x) for x in itertools.combinations(
            currentDeck+handP2, 3)]
        print("Your hand:")
        print(handP2)
        print("----------")

        # Jugando
        while ((trucoScore[0] < 2 and trucoScore[1] < 2) or (trucoScore[0] == 2 and trucoScore[1] == 2 and whoWonPrimera is None)):
            if (P1plays):
                # Decidiendo si cantar o no envido por primera vez
                if (cardsInMesa[0][0] == None and not isPlayingEnvido and not envidoHasAlredyBeenPlayed):
                    # Puede cantar envido por primera vez
                    P1probOfWinningEnvido = calculateProbabilityOfWinningEnvido(
                        handP1, possibleHandsOfP2, whoIsMano)

                    if (P1probOfWinningEnvido > 0.5):
                        print("P1 canta envido")
                        isPlayingEnvido = True
                        envidoHasAlredyBeenPlayed = True
                        lastEnvidoPointsAtPlay = 1
                        envidoPointsAtPlay = 2
                        P1plays = False  # Pasa el turno al otro jugador
                        continue  # Salta a la otra iteración del while loop para darle el turno al oponente

                # Tomando decisiones una vez que empezó el envido
                if(isPlayingEnvido):
                    P1probOfWinningEnvido = calculateProbabilityOfWinningEnvido(
                        handP1, possibleHandsOfP2, whoIsMano)
                    desiredEscalation = shouldEscalateEnvidoPoints(
                        P1probOfWinningEnvido, gameScore, envidoPointsAtPlay, lastEnvidoPointsAtPlay)

                    if (desiredEscalation < 0):  # Rechaza
                        print("P1 no quiere")

                        gameScore[1] += lastEnvidoPointsAtPlay
                        isPlayingEnvido = False
                        # Para determinar quien tiene que tirar carta en el truco no usamos P1Plays, sino que vemos quien no tiró carta en mesa.
                        continue

                    elif (desiredEscalation == 0):  # Acepta
                        print("P1 Quiere")
                        P1won, P1mayorEnvido, P2mayorEnvido = winsEnvido(
                            handP1, handP2, whoIsMano)

                        # Actualizando score
                        if (P1won):
                            gameScore[0] += envidoPointsAtPlay
                            print("P1 won")
                        else:
                            gameScore[1] += envidoPointsAtPlay
                            print("P2 won")

                        if (whoIsMano):
                            print("P1 tenía {puntos} puntos".format(
                                puntos=P1mayorEnvido))

                            knownHandOfP1[1] = P1mayorEnvido
                            if (not P1won):
                                knownHandOfP2[1] = P2mayorEnvido
                        else:
                            knownHandOfP2[1] = P2mayorEnvido
                            if (P1won):
                                print("P1 tenía {puntos} puntos".format(
                                    puntos=P1mayorEnvido))
                                knownHandOfP1[1] = P1mayorEnvido
                        # Actualizar posibles manos de cada jugador!!!!!!!!!
                        # Checkear si el juego terminó !!!!!
                        isPlayingEnvido = False
                        continue

                    elif (desiredEscalation > 0):  # Escala
                        print("P1 escala envido a {puntos}".format(
                            puntos=desiredEscalation))
                        lastEnvidoPointsAtPlay = envidoPointsAtPlay
                        envidoPointsAtPlay = desiredEscalation

                        P1plays = False
                        continue

            else:  # P2 plays

                # Decidiendo si cantar o no envido por primera vez
                if (cardsInMesa[0][1] == None and not isPlayingEnvido and not envidoHasAlredyBeenPlayed):
                    # Puede cantar envido por primera vez
                    if (input("Quieres cantar envido? (Y/N): ") == "Y"):
                        isPlayingEnvido = True
                        envidoHasAlredyBeenPlayed = True
                        lastEnvidoPointsAtPlay = 1
                        envidoPointsAtPlay = int(input("Cuantos puntos: "))
                        P1plays = True
                        continue

                if(isPlayingEnvido):
                    # acepta solo als mismas inputs que las que daría la f de desicion making
                    desiredEscalation = int(input("Desired escalation: "))

                    if (desiredEscalation < 0):  # Rechaza

                        gameScore[0] += lastEnvidoPointsAtPlay
                        isPlayingEnvido = False
                        # Para determinar quien tiene que tirar carta en el truco no usamos P1Plays, sino que vemos quien no tiró carta en mesa.
                        continue

                    elif (desiredEscalation == 0):  # Acepta
                        P1won, P1mayorEnvido, P2mayorEnvido = winsEnvido(
                            handP1, handP2, whoIsMano)

                        # Actualizando score
                        if (P1won):
                            gameScore[0] += envidoPointsAtPlay
                            print("P1 won")
                        else:
                            gameScore[1] += envidoPointsAtPlay
                            print("P2 won")

                        if (whoIsMano):
                            print("P1 tenía {puntos} puntos".format(
                                puntos=P1mayorEnvido))

                            knownHandOfP1[1] = P1mayorEnvido
                            if (not P1won):
                                knownHandOfP2[1] = P2mayorEnvido
                        else:
                            knownHandOfP2[1] = P2mayorEnvido
                            if (P1won):
                                print("P1 tenía {puntos} puntos".format(
                                    puntos=P1mayorEnvido))
                                knownHandOfP1[1] = P1mayorEnvido
                        # Actualizar posibles manos de cada jugador!!!!!!!!!
                        # Checkear si el juego terminó !!!!!
                        isPlayingEnvido = False
                        continue

                    elif (desiredEscalation > 0):  # Escala
                        print("Escalaste a {puntos}".format(
                            puntos=desiredEscalation))
                        lastEnvidoPointsAtPlay = envidoPointsAtPlay
                        envidoPointsAtPlay = desiredEscalation

                        P1plays = True
                        continue

            gameScore[1] = 15


if __name__ == "__main__":
    main()
