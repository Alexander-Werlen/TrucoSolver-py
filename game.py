from envidoFunctions import *
from trucoFunctions import *
from funcionesBasicas import *
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
        # Empezar ronda
        handP1, handP2, currentDeck = repartir()
        # para usarlo en funciones invertir el orden como corresponda (se asume que el jugador evaluando la función es ls[0])
        trucoScore = [0, 0]
        cardsInMesa = [[None, None]]
        # Actualizando conocimiento de los jugadores
        knownHandOfP1 = [[], None]
        knownHandOfP2 = [[], None]

        possibleHandsOfP1 = [list(x) for x in itertools.combinations(
            currentDeck+handP1, 3)]
        possibleHandsOfP2 = [list(x) for x in itertools.combinations(
            currentDeck+handP2, 3)]

        # Jugando

        """ print(whoIsMano)
        print(handP1)
        print(handP2)

        print(myHandWinsTruco(handP1[:], handP2[:],
              [0, 0], whoIsMano, whoIsMano, cardsInMesa[:]))
        print(probOfWinningTrucoGivenHand(handP1[:], possibleHandsOfP2[:],
              [0, 0], whoIsMano, whoIsMano, cardsInMesa[:])) """

        gameScore = [15, 5]


if __name__ == "__main__":
    main()
