from miscelaneos import dicPossiblesFormasDeEscalarEnvido


def trucoVonNeumann(IamP1, x, pot, bet):
    # Si se reacciona a escalamiento llamar de nuevo para decidir si escalar tras aceptar
    """ 
    returns:
    true: if should bet or call
    false: if should check or fold 

    inputs:
    x: prob of winning truco
    pot: puntos del truco en juego
    bet: posible escalamiento de puntos
    IamP1: true si estás decidiendo escalar, false si estas reaccionando a un escalamiento
     """

    b = (2*bet**2+4*bet*pot+pot**2)/(2*bet**2+5*bet*pot+2*pot**2)
    c = 2*b-1
    a = (bet-bet*b)/(bet+pot)

    if (IamP1):
        return False if x > a and x < b else True
    else:
        return False if x < c else True


def calculateOptimalBet(pot):
    #Eligiendo la bet que maximisa al valor esperado del juego.
    return max(dicPossiblesFormasDeEscalarEnvido[pot], key=lambda bet: (bet-bet*((2*bet**2+4*bet*pot+pot**2)/(2*bet**2+5*bet*pot+2*pot**2)))/(bet+pot))


def envidoVonNeumann(IamP1, x, pot, bet):
    """ 
    returns:
    true: if should bet or call
    false: if should check or fold 
    ..., bet: None if doesn't matter, bet if wants to raise

    inputs:
    x: prob of winning envido
    pot: puntos del envido en juego
    bet: escalamiento de puntos (ya definido si estas reaccionando, None si tenes que calcularlo)
    IamP1: true si estás decidiendo escalar, false si estas reaccionando a un escalamiento
     """

    if (IamP1):
        if (pot == 0):
            # VonNeumann modificado
            # bets envido
            return (False, None) if x > 1/3 and x < 2/3 else (True, 2)

        elif (bet is None):
            # Calculamos bet optimo
            bet = calculateOptimalBet(pot)

            b = (2*bet**2+4*bet*pot+pot**2)/(2*bet**2+5*bet*pot+2*pot**2)
            c = 2*b-1
            a = (bet-bet*b)/(bet+pot)

            return (False, None) if x > a and x < b else (True, bet)

    else:
        if (pot == 1):
            # Von Neumann modificado
            return (False, None) if x < 2/3 else (True, None)

        else:
            b = (2*bet**2+4*bet*pot+pot**2)/(2*bet**2+5*bet*pot+2*pot**2)
            c = 2*b-1
            a = (bet-bet*b)/(bet+pot)

            return (False, None) if x < c else (True, None)
