from miscelaneos import *
from envidoFunctions import *
from trucoFunctions import *
from funcionesBasicas import *
from decisionMakingFunctions import *
from GTO.vonNeumannModels import trucoVonNeumann, envidoVonNeumann
import random
import itertools


class Game:
    def __init__(self):
        self.output = self.OutputManager(self)
        self.output.informarInicioJuego()

        self.gameScore = [0, 0]
        self.cardsInMesa = [[None, None], [None, None], [None, None]]
        self.whoIsMano = random.choice([True, False])

    class OutputManager(object):
        def __init__(self, game_object):
            self.game = game_object

        def informarInicioJuego():
            print("-----------------")
            print("Empezo la partida")
            print("-----------------")

        def informarInicioNuevaRonda(self):
            print("-----------------")
            print("Empezo nueva ronda")
            print("Puntaje actual:")
            print(self.game.gameScore)
            print("-----------------")

        def informarWhoWon(self, whoWon):
            print("-----------------")
            print("Partida finalizada. " + whoWon + " gana.")
            print("Puntaje final:")
            print(self.game.gameScore)
            print("-----------------")

        def informarManoP2(self):
            print("-----------------")
            print("Your hand:")
            print(self.game.handP2)
            print("-----------------")

        def informarEscalaPuntosEnvido(self):
            print("-----------------")
            if (self.game.onFaltaEnvido):
                print("{jugador} escalates to falta envido".format(
                    jugador="P1" if self.game.isP1Turn else "P2"))
            else:
                print("{jugador} escalates to {puntos}".format(
                    puntos=self.game.envidoPointsAtBet, jugador="P1" if self.game.isP1Turn else "P2"))
            print("-----------------")

        def informarCantoPuntosEnvido(self, puntosP1, puntosP2, p1Won):
            print("-----------------")
            if (p1Won):
                print("P1 gana {atPLay} con {p1}.".format(
                    atPlay=self.game.envidoPointsAtPlay, p1=puntosP1))
            else:
                if (self.game.whoIsMano):
                    print("P2 gana {atPLay} con {p2} puntos contra {p1}.".format(
                        atPlay=self.game.envidoPointsAtPlay, p2=puntosP2, p1=puntosP1))
                else:
                    print("P2 gana {atPLay} con {p2}.".format(
                        atPlay=self.game.envidoPointsAtPlay, p2=puntosP2))
            print("-----------------")

    def checkIfGameEnded(self):
        # Should check if game ended every time points are added to the score
        if (self.gameScore[0] > 14):
            self.output.informarWhoWon("P1")
            exit()
        elif (self.gameScore[1] > 14):
            self.output.informarWhoWon("P2")
            exit()

    def checkIfShouldStartNewRound(self):
        if ((self.currentTrucoScore[0] >= 2 or self.currentTrucoScore[1] >= 2)
                and not (self.currentTrucoScore[0] == 2 and self.currentTrucoScore[1] == 2 and self.whoWonPrimera is None)):
            self.shouldStartNewRound = True

    def giveControlToTheOtherPlayer(self):
        self.isP1Turn = not self.isP1Turn

    def actualizarPossibleHandsOfP2(self):
        return

    def faltaEnvidoPoints(self):
        return min([15-self.gameScore[0], 15-self.gameScore[1]])

    def canP1StartEnvido(self):
        if (not self.envidoAlreadyWasPlayed and not self.decisionAboutEnvidoBetHasToBeMade and self.cardsInMesa[0][0] == None):
            return True
        else:
            return False

    def canP2StartEnvido(self):
        if (not self.envidoAlreadyWasPlayed and not self.decisionAboutEnvidoBetHasToBeMade and self.cardsInMesa[0][1] == None):
            return True
        else:
            return False

    def startEnvidoExchange(self, initialBet):
        if (initialBet not in EnvidoPuntosPorApuesta.values()):
            raise ValueError("Puntos de bet no validos.")

        if (initialBet == 15):
            self.onFaltaEnvido = True
            self.envidoPointsAtBet = self.faltaEnvidoPoints()
        else:
            self.envidoPointsAtBet = initialBet

        self.envidoPointsAtPlay = 1
        self.decisionAboutEnvidoBetHasToBeMade = True
        self.giveControlToTheOtherPlayer()

    def escalateEnvidoExchange(self, bet):
        if (bet not in dicPossiblesFormasDeEscalarEnvido[self.envidoPointsAtPlay]):
            raise ValueError("Puntos de bet no validos. Tried to escalate envido to {bet} from {atPlay}".format(
                bet=str(bet), atPlay=str(self.envidoPointsAtPlay)))
        if (self.onFaltaEnvido):
            raise Exception(
                "Tried to escalate envido points when already playing for falta envido.")
        if (not self.decisionAboutEnvidoBetHasToBeMade):
            raise Exception(
                "Tried to escalate envido while not in envido exchange.")

        self.envidoPointsAtPlay = self.envidoPointsAtBet

        if (bet == 15):
            self.envidoPointsAtBet = self.faltaEnvidoPoints()
            self.onFaltaEnvido = True
        else:
            self.envidoPointsAtBet = bet

        self.output.informarEscalaPuntosEnvido()
        self.giveControlToTheOtherPlayer()

    def endEnvidoExchange(self, acceptsBet):

        if (not acceptsBet):
            self.gameScore[1 if self.isP1Turn else 0] += self.envidoPointsAtPlay

        else:
            self.envidoPointsAtPlay = self.envidoPointsAtBet

            p1Wins, P1points, P2points = winsEnvido(
                self.handP1, self.handP2, self.whoIsMano)

            # Decidiendo si actualizar informacion de manos conocidas
            if (not self.whoIsMano or not p1Wins):
                self.knownHandOfP2[1] = P2points
                self.actualizarPossibleHandsOfP2()

            if (p1Wins):
                self.gameScore[0] += self.envidoPointsAtPlay
            else:
                self.gameScore[1] += self.envidoPointsAtPlay

            self.output.informarCantoPuntosEnvido(
                P1points, P2points, p1Wins)

        self.checkIfGameEnded()
        self.decisionAboutEnvidoBetHasToBeMade = False
        self.envidoAlreadyWasPlayed = True
        # dando control a quien sea mano para continuar juego
        self.isP1Turn = self.whoIsMano

    def escalateTruco(self, bet):
        if (bet != dicPossiblesFormasDeEscalarTruco[self.trucoPointsAtPlay]):
            raise ValueError("Puntos de bet no validos. Tried to escalate truco to {bet} from {atPlay}".format(
                bet=str(bet), atPlay=str(self.trucoPointsAtPlay)))

        self.trucoPointsAtPlay = self.trucoPointsAtBet
        self.trucoPointsAtBet = bet

        self.output.informarTrucoEscalation()

    def startNewRound(self):
        self.output.informarInicioNuevaRonda()
        self.shouldStartNewRound = False

        self.cardsInMesa = [[None, None], [None, None], [None, None]]
        self.currentTrucoStage = 0
        self.whoWonPrimera = None
        self.currentTrucoScore = [0, 0]
        self.decisionAboutTrucoBetHasToBeMade = False
        self.trucoPointsAtPlay = 1
        self.trucoPointsAtBet = 1
        self.envidoAlreadyWasPlayed = False
        self.decisionAboutEnvidoBetHasToBeMade = False
        self.envidoPointsAtPlay = 0
        self.envidoPointsAtBet = 0
        self.onFaltaEnvido = False

        self.whoIsMano = not self.whoIsMano  # invirtiendo quien es mano
        self.isP1Turn = self.whoIsMano

        self.handP1, self.handP2, self.currentDeck = repartir()

        self.knownHandOfP2 = [[], None]  # [[cards], puntosEnvido]
        self.possibleHandsP2 = [list(x) for x in itertools.combinations(
            currentDeck+handP2, 3)]


def main():

    # definiendo variables globales
    global gameScore
    gameScore = [0, 0]  # P1[0] P2[1]
    #global knownHandOfP1
    global knownHandOfP2
    #global possibleHandsOfP1
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
        print("Empezó la ronda")
        print("-----------------")
        # Empezar ronda
        handP1, handP2, currentDeck = repartir()
        # para usarlo en funciones invertir el orden como corresponda (se asume que el jugador evaluando la función es ls[0])
        trucoScore = [0, 0]
        cardsInMesa = [[None, None]]  # primera siempre es de P1, segunda de P2
        # Auxiliares
        whoWonPrimera = None
        isPlayingEnvido = False  # True if P1, False if P2
        decisionAboutTrucoBetHasToBeMade = False
        envidoHasAlredyBeenPlayed = False
        envidoPointsAtPlay = 0
        envidoPointsAtBet = 0
        trucoPointsAtPlay = 1
        # Actualizando conocimiento de los jugadores
        #knownHandOfP1 = [[], None]
        knownHandOfP2 = [[], None]

        #possibleHandsOfP1 = [list(x) for x in itertools.combinations(currentDeck+handP1, 3)]
        possibleHandsOfP2 = [list(x) for x in itertools.combinations(
            currentDeck+handP2, 3)]
        print("Your hand:")
        print(handP2)
        print("----------")

        # Jugando
        while (((trucoScore[0] < 2 and trucoScore[1] < 2) or (trucoScore[0] == 2 and trucoScore[1] == 2 and whoWonPrimera is None)) and not gameEnded(gameScore)):
            if (P1plays):
                # Decidiendo si cantar o no envido por primera vez
                if (cardsInMesa[0][0] == None and not isPlayingEnvido and not envidoHasAlredyBeenPlayed):
                    # Puede cantar envido por primera vez
                    P1probOfWinningEnvido = calculateProbabilityOfWinningEnvido(
                        handP1, possibleHandsOfP2, whoIsMano)

                    if ((envidoVonNeumann(True, P1probOfWinningEnvido, envidoPointsAtPlay, None))[0]):
                        print("P1 canta envido")
                        isPlayingEnvido = True
                        envidoHasAlredyBeenPlayed = True
                        envidoPointsAtPlay = 1
                        envidoPointsAtBet = 2
                        P1plays = False  # Pasa el turno al otro jugador
                        continue  # Salta a la otra iteración del while loop para darle el turno al oponente

                # Tomando decisiones una vez que empezó el envido
                if(isPlayingEnvido):
                    P1probOfWinningEnvido = calculateProbabilityOfWinningEnvido(
                        handP1, possibleHandsOfP2, whoIsMano)
                    desiredEscalation = shouldEscalateEnvidoPoints(
                        P1probOfWinningEnvido, gameScore, envidoPointsAtBet, envidoPointsAtPlay)

                    if (desiredEscalation < 0):  # Rechaza
                        print("P1 no quiere")

                        gameScore[1] += envidoPointsAtPlay
                        isPlayingEnvido = False
                        # Para determinar quien tiene que tirar carta en el truco no usamos P1Plays, sino que vemos quien no tiró carta en mesa.
                        continue

                    elif (desiredEscalation == 0):  # Acepta
                        print("P1 Quiere")
                        P1won, P1mayorEnvido, P2mayorEnvido = winsEnvido(
                            handP1, handP2, whoIsMano)

                        # Actualizando score
                        if (P1won):
                            gameScore[0] += envidoPointsAtBet
                            print("P1 won")
                        else:
                            gameScore[1] += envidoPointsAtBet
                            print("P2 won")

                        if (whoIsMano):
                            print("P1 tenía {puntos} puntos".format(
                                puntos=P1mayorEnvido))

                            #knownHandOfP1[1] = P1mayorEnvido
                            if (not P1won):
                                knownHandOfP2[1] = P2mayorEnvido
                        else:
                            knownHandOfP2[1] = P2mayorEnvido
                            if (P1won):
                                print("P1 tenía {puntos} puntos".format(
                                    puntos=P1mayorEnvido))
                                #knownHandOfP1[1] = P1mayorEnvido
                        # Actualizar posibles manos de cada jugador!!!!!!!!!
                        # Checkear si el juego terminó !!!!!
                        isPlayingEnvido = False
                        continue

                    elif (desiredEscalation > 0):  # Escala
                        print("P1 escala envido a {puntos}".format(
                            puntos=desiredEscalation))
                        envidoPointsAtPlay = envidoPointsAtBet
                        envidoPointsAtBet = desiredEscalation

                        P1plays = False
                        continue

                if (decisionAboutTrucoBetHasToBeMade):
                    probWinTruco = probOfWinningTrucoGivenHand(
                        handP1, possibleHandsOfP2, trucoScore, True, whoIsMano, cardsInMesa, whoWonPrimera)

                else:  # ronda truco
                    probWinTruco = probOfWinningTrucoGivenHand(
                        handP1, possibleHandsOfP2, trucoScore, True, whoIsMano, cardsInMesa, whoWonPrimera)

            else:  # P2 plays

                # Decidiendo si cantar o no envido por primera vez
                if (cardsInMesa[0][1] == None and not isPlayingEnvido and not envidoHasAlredyBeenPlayed):
                    # Puede cantar envido por primera vez
                    if (input("Quieres cantar envido? (Y/N): ") == "Y"):
                        isPlayingEnvido = True
                        envidoHasAlredyBeenPlayed = True
                        envidoPointsAtPlay = 1
                        envidoPointsAtBet = int(input("Cuantos puntos: "))
                        P1plays = True
                        continue

                if(isPlayingEnvido):
                    # acepta solo als mismas inputs que las que daría la f de desicion making
                    desiredEscalation = int(input("Desired escalation: "))

                    if (desiredEscalation < 0):  # Rechaza

                        gameScore[0] += envidoPointsAtPlay
                        isPlayingEnvido = False
                        # Para determinar quien tiene que tirar carta en el truco no usamos P1Plays, sino que vemos quien no tiró carta en mesa.
                        continue

                    elif (desiredEscalation == 0):  # Acepta
                        P1won, P1mayorEnvido, P2mayorEnvido = winsEnvido(
                            handP1, handP2, whoIsMano)

                        # Actualizando score
                        if (P1won):
                            gameScore[0] += envidoPointsAtBet
                            print("P1 won")
                        else:
                            gameScore[1] += envidoPointsAtBet
                            print("P2 won")

                        if (whoIsMano):
                            print("P1 tenía {puntos} puntos".format(
                                puntos=P1mayorEnvido))

                            #knownHandOfP1[1] = P1mayorEnvido
                            if (not P1won):
                                knownHandOfP2[1] = P2mayorEnvido
                        else:
                            knownHandOfP2[1] = P2mayorEnvido
                            if (P1won):
                                print("P1 tenía {puntos} puntos".format(
                                    puntos=P1mayorEnvido))
                                #knownHandOfP1[1] = P1mayorEnvido
                        # Actualizar posibles manos de cada jugador!!!!!!!!! (conviene hacerlo siempre al principio de cada iteración del while)
                        isPlayingEnvido = False
                        continue

                    elif (desiredEscalation > 0):  # Escala
                        print("Escalaste a {puntos}".format(
                            puntos=desiredEscalation))
                        envidoPointsAtPlay = envidoPointsAtBet
                        envidoPointsAtBet = desiredEscalation

                        P1plays = True
                        continue

            gameScore[1] = 15


if __name__ == "__main__":
    main()
