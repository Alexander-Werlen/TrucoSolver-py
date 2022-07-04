from miscelaneos import deck
from envidoFunctions import calculateEnvidoPoints
import random
import copy


def repartir():
    # returns handP1, handP2, deckOfCardsLeft

    currentDeck = copy.deepcopy(deck)
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


def handIsPossible(handToCheck, knownHandOfOponent):
    # Returns True if hand is possible given the conditions of the knownHand. False if not

    if (calculateEnvidoPoints(copy.deepcopy(handToCheck) + knownHandOfOponent[0]) != knownHandOfOponent[1]):
        return False

    return True


def actualizarPossibleHands(othersPossibleHands, knownHandOfOponent):
    # Returns lista actualizada de posibles manos de oponente.
    """ 
    Inputs:
    1) othersPossibleHands: ls[x] donde x es mano posible el oponente previo a actualizar
    2) knownHandOfOponent: ls[[x<=3], puntosEnvido]
     """

    return [hand for hand in othersPossibleHands if handIsPossible(hand, knownHandOfOponent)]
