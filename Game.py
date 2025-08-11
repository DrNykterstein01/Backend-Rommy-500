import random
def electionPhase(players, deck):
    print("Fase de Elección")
    availableCards = deck.drawInElectionPhase(len(players))  #Sacamos las Cartas para la fase de elección
    random.shuffle(availableCards)  #Mezclamos las Cartas que se van a elegir para que no estén en el mismo orden

    elections = {}  #Creamos un diccionario para almacenar las elecciones de los jugadores antes de la ronda
    for player, Card in zip(players, availableCards):
        elections[player] = Card  #Asignamos la Carta elegida a cada jugador
        print(f"{player} ha elegido la Carta: {Card}") #Indicamos qué Carta fue elegida

    #Con lo siguiente, se determinará el turno de la ronda para los jugadores dependiendo del valor numérico de la Carta que eligió cada uno
    order = sorted(
        elections.items(),
        key = lambda item: Card.values.index(item[1].value),
        reverse = True
    )
    playerOrder = [player for player, _ in order]  #Obtenemos el orden de los jugadores según sus elecciones
    print("Orden de los jugadores:", playerOrder)
    return playerOrder
    #Devolvemos el orden de los jugadores para la ronda