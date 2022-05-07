from envidoFunctions import *
from trucoFunctions import *
from funcionesBasicas import *
import random
import itertools


def main():

    # definiendo variables globales
    global score
    score = [0, 0]  # P1[0] P2[1]
    global knownHandOfP1
    global knownHandOfP2
    global possibleHandsOfP1
    global possibleHandsOfP2
    global handP1
    global handP2
    global currentDeck
    global whoIsMano

    # Defining who is mano. True is P1, False is P2
    P1plays = random.choice([True, False])
    whoIsMano = P1plays

    while(not gameEnded(score)):
        # Empezar ronda
        handP1, handP2, currentDeck = repartir()

        # Actualizando conocimiento de los jugadores
        knownHandOfP1 = [[], None]
        knownHandOfP2 = [[], None]

        possibleHandsOfP1 = [list(x) for x in itertools.combinations(
            currentDeck+handP1, 3)]
        possibleHandsOfP2 = [list(x) for x in itertools.combinations(
            currentDeck+handP2, 3)]

        # Jugando
        print(handP1)
        print(handP2)
        print(len(possibleHandsOfP1))
        print(len(possibleHandsOfP2))
        print(winsEnvido(handP1, handP2, whoIsMano))
        print(getProbOfMinimizingExpectedFunctionScore(handP1, possibleHandsOfP2))
        print(getProbOfMinimizingExpectedFunctionScore(handP2, possibleHandsOfP1))

        score = [15, 5]


if __name__ == "__main__":
    main()
