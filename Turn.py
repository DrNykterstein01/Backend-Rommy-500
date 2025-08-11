def drawCard(player, round, fromDiscards = False, indexDiscards = None):
    if fromDiscards and indexDiscards is not None: #Si se indica que se quiere sacar una carta del montón de descartes y se proporciona un índice válido
        takenCards = round.discards[indexDiscards:] #Tomamos las cartas desde el índice especificado hasta el final
        round.discards = round.discards[:indexDiscards]  #Con esto quitamos la carta de la pila de descartes
        round.hands[player].extend(takenCards)  #Añadimos la carta a la mano del jugador
    else:
        card = round.pile.pop()  #Sacamos la última carta del mazo
        round.hands[player].append(card)  #Añadimos la carta a la mano del jugador

def discardCard(player, round, card):
    round.hands[player].remove(card)  #Quitamos la carta de la mano del jugador
    round.discards.append(card)  #Añadimos la carta al montón de descartes


def refillDeck(round):
    if len(round.pile) == 0:  #Si el mazo se queda sin cartas, sacamos las cartas del montón de descartes y las ponemos en el mazo
        round.pile = round.discards[:-1]
        round.discards = round.discards[-1:]  #Dejamos la última carta del montón de descartes como la única carta en el montón de descartes