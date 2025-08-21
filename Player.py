import pygame
from Round import Round
from Card import Card
class Player:

    def __init__(self, id, name):
        self.playerId = id
        self.playerName = name
        self.playerPoints = 0
        self.Hand = False
        self.playerTurn = False
        self.playerHand = [] # Lista que contendrá las cartas del jugador.
        self.playerCardsPos = {} # Atributo experimental, para conocer la posición de cada carta lógica.
        self.playerCardsSelect = [] # Atributo experimental, para guardar las cartas selecc. para un movimiento.
        self.downHand = False
        #self.playerBuy = False
        self.playerPass = False # Atrib. experimental, para saber si pasó de la carta descartada.

    def chooseCard(self, clickPos):
        
        # Creamos un bucle para recorrer los índices de las cartas en la mano del jugador. 
        for c in range(len(self.playerHand)):

            # Verificamos si hay un click sobre una carta que no ha sido seleccionada previamente.
            # NOTA: La posición de cada carta física está asociada con el índice de la carta lógica
            #       en la mano del jugador. De esta forma, se evitan problemas si hay cartas repetidas.
            
            # "Si el jugador hizo click en un rectángulo, y la carta lógica asociada al índice del rectán.
            # no está entre las seleccionadas..."
            if self.playerCardsPos[c].collidepoint(clickPos) and self.playerHand[c] not in self.playerCardsSelect:
                card = self.playerHand[c]
                print(f"Carta marcada: {card}")
                self.playerCardsSelect.append(card)
            # Verificamos si hay un click sobre una carta que ya ha sido seleccionada previamente.
            # NOTA: En este condicional verificamos qué carta seleccionó el jugador, en caso de que
            #       tenga dos o más cartas iguales en su mano.
            elif self.playerCardsPos[c].collidepoint(clickPos) and self.playerHand[c] in self.playerCardsSelect:
                card = self.playerHand[c] # Guardamos la carta asociada a la posición en que clickeó.

                countsOcurSelec = self.playerCardsSelect.count(card)          # Contamos las ocurrencias de dicha carta en las seleccionadas.
                countsOcurHand = self.playerHand.count(card)                  # Contamos las ocurrencias de dicha carta en la mano del jugador.
                if countsOcurSelec != countsOcurHand:                         # Si los conteos son distintos, entonces el jugador tiene repetida la carta.
                    indexOcur = 0                                             # Var. de control para buscar el índice de la carta en la mano del jugador.
                    sameIndex = False                                         # Var. de control para saber si el jugador clickeó el mismo índice.
                    for i in range(countsOcurSelec):                          # Bucle para cada una de las ocurrencias de la carta entre las seleccionadas.
                        indexOcur = self.playerHand.index(card, indexOcur,-1) # Identificamos el índice de la primera ocurrencia en la mano del jugador (desde el índice de indexOcur hasta el último).
                        if c == indexOcur:                                    # Verificamos si el índice clickeado corresponde al de la primera ocurrencia.
                            sameIndex = True                                  # Si los índices coinciden, el jugador clickeó en una misma posición dos veces (una misma carta).
                        else:
                            indexOcur += 1

                            # Si los índices son distintos y aún quedan ocurrencias en las seleccionadas, reanudamos la búsqueda del índice
                            # de la siguiente ocurrencia de la carta partiendo del índice siguiente al de la ocurrencia previa (por eso indexOcur += 1).

                    if sameIndex:                                             # Si resulta que el jugador clickeó dos veces en el mismo índice (posición)...
                        print(f"Carta desmarcada: {card}")
                        self.playerCardsSelect.remove(card)                   # Eliminamos las cartas de las seleccionadas.
                    else:
                        print(f"Carta marcada: {card}")                       # Si el jugador no hizo click en la misma posición, está marcando otra carta con el mismo valor.
                        self.playerCardsSelect.append(card)                   # Añadimos la carta a las seleccionadas.
                else:
                    print(f"Carta desmarcada: {card}")
                    self.playerCardsSelect.remove(card)                       # Si el conteo inicial de ocurrencias es el mismo en ambas listas, no hay repeticiones de la carta; por tanto, la eliminamos.

    def takeCard(self, card): #Esto solo agregará la carta a la playerHand del jugador, independientemente de si la toma del mazo o del descarte (eso se manejará en otro archivo)
        self.playerHand.append(card)
        
    # Mét. para descartar una carta de la playerHand del jugador. Sólo se ejecuta si el jugador tiene una única
    # carta seleccionada previamente.
    def discardCard(self):

        # Verificamos la cantidad de cartas seleccionadas.
        if len(self.playerCardsSelect) == 2:

            # Si seleccionó dos y la primera es un Joker, se retorna una lista con ambas cartas.
            if self.playerCardsSelect[0].joker:

                cardDiscarted = self.playerCardsSelect.pop()
                jokerDiscarted = self.playerCardsSelect.pop()
                self.playerHand.remove(cardDiscarted)
                self.playerHand.remove(jokerDiscarted)

                return [jokerDiscarted, cardDiscarted]
            # Si seleccionó dos y la segunda es un Joker, volvemos a retornar ambas cartas.
            elif self.playerCardsSelect[1].joker:

                jokerDiscarted = self.playerCardsSelect.pop()
                cardDiscarted = self.playerCardsSelect.pop()
                self.playerHand.remove(jokerDiscarted)
                self.playerHand.remove(cardDiscarted)

                return [cardDiscarted, jokerDiscarted]
        # Si el jugador sólo seleccionó una carta para descartar, retornamos dicha carta.
        elif len(self.playerCardsSelect) == 1:

            cardDiscarted = self.playerCardsSelect.pop()
            self.playerHand.remove(cardDiscarted)

            return [cardDiscarted]
        # Si el jugador no seleccionó ninguna carta, retornamos None.
        else:
            return None
    
    def canGetOff(self):
        trios = self.findTrios()
        straights = self.findStraight()
        armedTrio = []

        for trio in trios:
            for straight in straights:
                # Esto nos permitirá verificar si 
                # COMPARTEN LA MISMA INSTANCIA de carta (no solo mismo valor y palo)
                conflict = any(c1.id == c2.id for c1 in trio for c2 in straight if c1 != c2)
                for card1 in trio:
                    armedTrio.append(card1)
                    for card2 in straight:
                        if card1.id == card2.id:
                            armedTrio.remove(card1)
                result = None

                if not conflict and len(armedTrio) >= 3 and len(straight) >= 4:
                    print(f"El jugador {self.playerName} SI se puede bajar con:")
                    print(f"Trío: {[str(c) for c in armedTrio]}")
                    print(f"Seguidilla: {[str(c) for c in straight]}")
                    result = True
                else:
                    print(f"El jugador {self.playerName} NO se puede bajar aún.")
                    result = False
        return result


                
    
    def findTrios(self):
        #Se utilizará para identificar tríos en la mano del jugador.
        trios = [] # Lista para almacenar los tríos encontrados en la mano del jugador
        cardsPerValue = {} # Diccionario para almacenar las cartas por valor
        jokers = [] # Cartas jokers
        for card in self.playerHand:
            if card.joker: # Si la carta es un joker, la añadimos a la lista de jokers
                jokers.append(card)
            else:
                if card.value not in cardsPerValue: # Si el valor de la carta no se encuentra en el diccionario, lo creamos
                    cardsPerValue[card.value] = []
                cardsPerValue[card.value].append(card) # Añadimos la carta a la lista correspondiente en el diccionario

        for value, cards in cardsPerValue.items():
            if len(cards) >= 3:
                trios.append(cards) # Si hay al menos 3 cartas del mismo valor, las añadimos a la lista de tríos
            elif len(cards) == 2 and len(jokers) >= 1:
                trios.append(cards) # Si hay 2 cartas del mismo valor y 1 joker, las añadimos a la lista de tríos
                trios.append([jokers[0]])
        validTrios = []
        for trio in trios: #Regla para que no haya más de un joker por trío
            jokerQuantity = sum(1 for card in trio if card.joker)
            if jokerQuantity <= 1:
                validTrios.append(trio)
        return validTrios
    
    def findStraight(self):
        straights = []  # Lista para almacenar seguidillas encontradas
        jokers = [card for card in self.playerHand if card.joker]
        noJokerCards = [card for card in self.playerHand if card.joker == False]

        # Agrupar cartas por palo
        cardsPerType = {}
        for card in noJokerCards:
            if card.type not in cardsPerType:
                cardsPerType[card.type] = []
            cardsPerType[card.type].append(card)

        # Ordenamos las cartas según su valor dentro de cada palo
        for palo, cards in cardsPerType.items():
            cards.sort(key=lambda c: Card.values.index(c.value))
        
            # Caso especial: As bajo (A, 2, 3...)
            hasA = any(c.value == "A" for c in cards)
            if hasA:
                # Si A está junto con 2 o 3, tratamos el As como índice -1 para que vaya al inicio
                if any(c.value in ["2", "3", "4"] for c in cards):
                    sortedCards = sorted(cards, key=lambda c: -1 if c.value == "A" else Card.values.index(c.value))
                else:
                    sortedCards = cards[:]  # As como alto
            else:
                sortedCards = cards[:]

            # Intentar formar secuencias con Jokers insertados
            temp = [] #Lista temporal para almacenar la secuencia actual
            usedJokers = 0 #Por defecto, la cantidad de jokers usados siempre empieza en 0

            for i in range(len(sortedCards)):
                if not temp:
                    temp.append(sortedCards[i])
                else:
                    previousIndex = Card.values.index(temp[-1].value) #Valor numérico de la carta anterior
                    currentIndex = Card.values.index(sortedCards[i].value) #Valor numérico de la carta actual

                    if currentIndex == previousIndex + 1:
                        temp.append(sortedCards[i])
                    elif currentIndex > previousIndex + 1:
                        gap = currentIndex - previousIndex - 1 #Espacio en blanco entre la carta anterior y la actual
                        if gap <= len(jokers) - usedJokers: #Traducción: Si hay suficientes jokers para rellenar el hueco...
                            # Usar Jokers para rellenar huecos
                            for _ in range(gap): # Por cada espacio en blanco...
                                if usedJokers < len(jokers):
                                    # No permitir Jokers consecutivos
                                    if temp and temp[-1].joker:
                                        break
                                    temp.append(jokers[usedJokers])
                                    usedJokers += 1
                            temp.append(sortedCards[i])
                        else:
                            # Reiniciar secuencia
                            if len(temp) >= 4:
                                straights.append(temp)
                            temp = [sortedCards[i]]
                            usedJokers = 0

            if len(temp) >= 4:
                straights.append(temp)

        # Filtrar secuencias que tengan Jokers consecutivos
        straightsFinal = [] 
        for s in straights:
            consecutiveJokers = any(s[i].joker and s[i+1].joker for i in range(len(s)-1))
            if not consecutiveJokers:
                straightsFinal.append(s)

        return straightsFinal

    def insertCard(self, idPlayer): #Aún no tengo en claro si lo mejor sea utilizar el idPlayer como parámetro o colocar otra cosa en su lugar
        if self.downHand == True:
            # Aquí se implementaría la lógica para agregar una carta en la jugada de otro jugador
            pass
        else:
            print("No se puede insertar una carta porque el jugador no se ha bajado.") #Esto se cambiará por una alerta visual más adelante, pero de momento no nos preocupemos por lo visual :3
