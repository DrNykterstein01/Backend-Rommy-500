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
        self.playerHand = [] #Lista que contendrá las cartas del jugador.
        self.playerCardsPos = {} #Atributo experimental, para conocer la posición de cada carta lógica.
        self.playerCardsSelect = [] #Atributo experimental, para guardar las cartas selecc. para un movimiento.
        self.downHand = False
        #self.playerBuy = False
        self.playerPass = False #Atrib. experimental, para saber si pasó de la carta descartada.

    def chooseCard(self, clickPos):
        
        #Creamos un bucle para recorrer los índices de las cartas en la mano del jugador. 
        for c in range(len(self.playerHand)):

            #Verificamos si hay un click sobre una carta que no ha sido seleccionada previamente.
            #NOTA: La posición de cada carta física está asociada con el índice de la carta lógica
            #      en la mano del jugador. De esta forma, se evitan problemas si hay cartas repetidas.
            
            #"Si el jugador hizo click en un rectángulo, y la carta lógica asociada al índice del rectán.
            #no está entre las seleccionadas..."
            if self.playerCardsPos[c].collidepoint(clickPos) and self.playerHand[c] not in self.playerCardsSelect:
                card = self.playerHand[c]
                print(f"Carta marcada: {card}")
                self.playerCardsSelect.append(card)
            #Verificamos si hay un click sobre una carta que ya ha sido seleccionada previamente.
            #NOTA: En este condicional verificamos qué carta seleccionó el jugador, en caso de que
            #      tenga dos o más cartas iguales en su mano.
            elif self.playerCardsPos[c].collidepoint(clickPos) and self.playerHand[c] in self.playerCardsSelect:
                card = self.playerHand[c] #Guardamos la carta asociada a la posición en que clickeó.

                countsOcurSelec = self.playerCardsSelect.count(card)          #Contamos las ocurrencias de dicha carta en las seleccionadas.
                countsOcurHand = self.playerHand.count(card)                  #Contamos las ocurrencias de dicha carta en la mano del jugador.
                if countsOcurSelec != countsOcurHand:                         #Si los conteos son distintos, entonces el jugador tiene repetida la carta.
                    indexOcur = 0                                             #Var. de control para buscar el índice de la carta en la mano del jugador.
                    sameIndex = False                                         #Var. de control para saber si el jugador clickeó el mismo índice.
                    for i in range(countsOcurSelec):                          #Bucle para cada una de las ocurrencias de la carta entre las seleccionadas.
                        indexOcur = self.playerHand.index(card, indexOcur,-1) #Identificamos el índice de la primera ocurrencia en la mano del jugador (desde el índice de indexOcur hasta el último).
                        if c == indexOcur:                                    #Verificamos si el índice clickeado corresponde al de la primera ocurrencia.
                            sameIndex = True                                  #Si los índices coinciden, el jugador clickeó en una misma posición dos veces (una misma carta).
                        else:
                            indexOcur += 1

                            #Si los índices son distintos y aún quedan ocurrencias en las seleccionadas, reanudamos la búsqueda del índice
                            #de la siguiente ocurrencia de la carta partiendo del índice siguiente al de la ocurrencia previa (por eso indexOcur += 1).

                    if sameIndex:                                             #Si resulta que el jugador clickeó dos veces en el mismo índice (posición)...
                        print(f"Carta desmarcada: {card}")
                        self.playerCardsSelect.remove(card)                   #Eliminamos las cartas de las seleccionadas.
                    else:
                        print(f"Carta marcada: {card}")                       #Si el jugador no hizo click en la misma posición, está marcando otra carta con el mismo valor.
                        self.playerCardsSelect.append(card)                   #Añadimos la carta a las seleccionadas.
                else:
                    print(f"Carta desmarcada: {card}")
                    self.playerCardsSelect.remove(card)                       #Si el conteo inicial de ocurrencias es el mismo en ambas listas, no hay repeticiones de la carta; por tanto, la eliminamos.

    def takeCard(self, card): #Esto solo agregará la carta a la playerHand del jugador, independientemente de si la toma del mazo o del descarte (eso se manejará en otro archivo)
        self.playerHand.append(card)
        
    #Mét. para descartar una carta de la playerHand del jugador. Sólo se ejecuta si el jugador tiene una única
    #carta seleccionada previamente.
    def discardCard(self):

        #Verificamos la cantidad de cartas seleccionadas.
        if len(self.playerCardsSelect) == 2:

            #Si seleccionó dos y la primera es un Joker, se retorna una lista con ambas cartas.
            if self.playerCardsSelect[0].joker:

                cardDiscarted = self.playerCardsSelect.pop()
                jokerDiscarted = self.playerCardsSelect.pop()
                self.playerHand.remove(cardDiscarted)
                self.playerHand.remove(jokerDiscarted)

                return [jokerDiscarted, cardDiscarted]
            #Si seleccionó dos y la segunda es un Joker, volvemos a retornar ambas cartas.
            elif self.playerCardsSelect[1].joker:

                jokerDiscarted = self.playerCardsSelect.pop()
                cardDiscarted = self.playerCardsSelect.pop()
                self.playerHand.remove(jokerDiscarted)
                self.playerHand.remove(cardDiscarted)

                return [cardDiscarted, jokerDiscarted]
        #Si el jugador sólo seleccionó una carta para descartar, retornamos dicha carta.
        elif len(self.playerCardsSelect) == 1:

            cardDiscarted = self.playerCardsSelect.pop()
            self.playerHand.remove(cardDiscarted)

            return [cardDiscarted]
        #Si el jugador no seleccionó ninguna carta, retornamos None.
        else:
            return None
    
    def canGetOff(self):
        trios = self.findTrios()
        straights = self.findStraight()
        jokers = [c for c in self.playerHand if c.joker]

        valid_combos = []

        # Probar cada combinación de trío + seguidilla
        for trio in trios:
            for straight in straights:
                jokersInTrio = sum(1 for c in trio if c.joker)
                jokersInStraight = sum(1 for c in straight if c.joker)
                usedJokers = jokersInTrio + jokersInStraight
                # Verificamos que no compartan cartas (verificando si tienen la misma instancia)
                conflict = any(c1.id == c2.id for c1 in trio for c2 in straight if not c1.joker and not c2.joker)
                conflict2 = usedJokers > len(jokers) #El segundo conflicto es para evitar que se dupliquen jokers en las jugadas
                if not conflict and not conflict2 and len(trio) >= 3 and len(straight) >= 4: #Esto nos filtra las combinaciones en las que hay conflictos y en las que haya seguidillas de 3 o menos cartas
                    valid_combos.append({
                        "trio": trio,
                        "straight": straight
                    })

        if valid_combos:
            print(f"\n✅ El jugador {self.playerName} SI SE PUEDE BAJAR con {len(valid_combos)} combinación(es):")
            for i, combo in enumerate(valid_combos, 1): #Simplemente nos imprime en pantalla las combinaciones disponibles en la mano del jugador
                print(f"   Opción {i}:")
                print(f"     Trío -> {[str(c) for c in combo['trio']]}")
                print(f"     Seguidilla -> {[str(c) for c in combo['straight']]}")
            return True, valid_combos
        else:
            print(f"\n❌ El jugador {self.playerName} NO se puede bajar aún.")
            return False, []
        #NOTA: Al final, tengo pensado que para que un jugador se pueda bajar, deba organizar su jugada
        #de tal manera que la combinación de cartas que va a bajar coincida con alguna de las combinaciones
        #que retorna este método canGetOff().

                
    
    def findTrios(self):
        #Se utilizará para identificar tríos en la mano del jugador.
        trios = [] #Lista para almacenar los tríos encontrados en la mano del jugador
        cardsPerValue = {} #Diccionario para almacenar las cartas por valor
        jokers = [] #Cartas jokers
        for card in self.playerHand:
            if card.joker: #Si la carta es un joker, la añadimos a la lista de jokers
                jokers.append(card)
            else:
                if card.value not in cardsPerValue: #Si el valor de la carta no se encuentra en el diccionario, lo creamos
                    cardsPerValue[card.value] = []
                cardsPerValue[card.value].append(card) #Añadimos la carta a la lista correspondiente en el diccionario
        for card in jokers:
            if "Joker" not in cardsPerValue:
                cardsPerValue["Joker"] = []
            cardsPerValue["Joker"].append(card)
        for value, cards in cardsPerValue.items():
            if len(cards) >= 3: 
                trios.append(cards) #Si hay al menos 3 cartas del mismo valor (sin jokers), las añadimos a la lista de tríos
            elif len(cards) >= 3 and len(jokers) >= 1:
                trios.append(cards + [jokers[0]]) 
            elif len(cards) == 2 and len(jokers) >= 1 :
                trios.append(cards + [jokers[0]]) #Si hay 2 cartas del mismo valor y 1 joker, las añadimos a la lista de tríos
        validTrios = []
        for trio in trios: #Regla para que no haya más de un joker por trío
            jokerQuantity = sum(1 for card in trio if card.joker)
            if jokerQuantity <= 1:
                validTrios.append(trio)
            elif jokerQuantity == 1:
                validTrios.append(trio)
        return validTrios
    
    def findStraight(self, highAsMode=False):
        straights = []
        jokers = [c for c in self.playerHand if c.joker]
        nonJokers = [c for c in self.playerHand if not c.joker]

        #Diccionario de valores a número (A=1, J=11, Q=12, K=13)
        valueToRank = {
            "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
            "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13
        }

        #Rank local: devuelve 14 para A cuando highAsMode = True
        def rank(card, highAs = False):
            if getattr(card, "joker", False):
                return -1
            if card.value == "A" and highAs:
                return 14
            return valueToRank[card.value]

        #Ordenamos las cartas por palo y por valor (colocando el As como bajo para el orden inicial)
        nonJokers.sort(key=lambda c: (c.type, rank(c, False)))

        #Agrupamos las cartas por palo
        palos = {}
        for c in nonJokers:
            palos.setdefault(c.type, []).append(c)

        #Función para evitar Jokers consecutivos
        def noConsecJokers(seq):
            return all(not (getattr(a, "joker", False) and getattr(b, "joker", False))
                    for a, b in zip(seq, seq[1:]))

        # Reglas para insertar Jokers al inicio/fin
        def canInsertAtStart(seq, highAsMode):
            """Función que controla si podemos colocar un Joker al inicio de la secuencia"""
            if not seq:
                return False

            # Si es As bajo y la primera carta es A, NO permitir Joker antes
            if seq[0].value == "A" and not highAsMode:
                return False

            # Caso As alto o cualquier otra carta, sí se permite Joker antes
            return True


        def canInsertAtEnd(seq, highAsMode):
            """Esta función controla si podemos colocar un Joker al final de la secuencia"""
            if not seq:
                return False

            #Si es una seguidilla con As alto y la última carta es A, NO permitir un Joker después
            if seq[-1].value == "A" and highAsMode:
                return False

            #Caso As bajo o cualquier otra carta, sí se permite Joker después
            return True


        #Función para insertar jokers en las seguidillas existentes
        def expandWithJokers(seq, jokersList, highAs):
            variants = []

            if not jokersList:
                return variants

            def helper(currSequence, remainingJokers, startAllowed, endAllowed):
                """Esta función inserta Jokers en todas las posiciones posibles (respetando las reglas)"""
                #Si ya no hay Jokers que insertar, validamos la secuencia final
                if not remainingJokers:
                    if len(currSequence) >= 4 and noConsecJokers(currSequence):
                        variants.append(currSequence[:])
                    return

                #Tomamos el siguiente Joker
                nextJoker = remainingJokers[0]
                restJokers = remainingJokers[1:]

                # 1)Probamos la inserción de cartas al inicio de la secuencia
                if startAllowed and canInsertAtStart(currSequence, highAs):
                    helper([nextJoker] + currSequence, restJokers, startAllowed, endAllowed)

                # 2)Ahora intentamos insertar en el medio como reemplazo de alguna otra carta
                for i in range(len(currSequence)):
                    newSequence = currSequence[:i] + [nextJoker] + currSequence[i+1:]
                    if noConsecJokers(newSequence):
                        helper(newSequence, restJokers, startAllowed, endAllowed)

                # 3)Por último, intentamos insertar un joker al final de la seguidilla
                if endAllowed and canInsertAtEnd(currSequence, highAs):
                    helper(currSequence + [nextJoker], restJokers, startAllowed, endAllowed)

            #Llamada inicial
            helper(seq, jokersList, True, True)

            #Eliminamos secuencias duplicadas
            unique = []
            seen = set()
            for v in variants:
                key = tuple(id(c) for c in v)
                if key not in seen:
                    seen.add(key)
                    unique.append(v)

            return unique


        #Función que comprueba si dos cartas (c1 y c2) son consecutivas en el modo actual
        def isConsecutive(c1, c2, highAs):
            return rank(c2, highAs) - rank(c1, highAs) == 1

        #Con el siguiente ciclo, recorremos todos los palos y las secuencias que puedan formarse con ellos
        for palo, cartas in palos.items():
            if not cartas:
                continue
            

            #Evaluamos las secuencias en ambos modos: As bajo y As alto
            for highMode in (False, True):
                #Ordenamos las cartas para este modo (As como 1 o 14 según highMode)
                sortedCards = sorted(cartas, key=lambda c: rank(c, highMode))

                if not sortedCards:
                    continue

                currentSequence = [sortedCards[0]] #currentSequence nos permite ir construyendo secuencias de carta en carta

                for i in range(1, len(sortedCards)):
                    prev = sortedCards[i - 1]
                    curr = sortedCards[i]

                    #Caso A->2, que es manejado por rank() cuando highMode = False
                    if isConsecutive(prev, curr, highMode):
                        currentSequence.append(curr)
                        
                    else:
                        #Guardamos la secuencia si alcanza mínimo 3 (para luego añadirle jokers)
                        if len(currentSequence) >= 3:
                            straights.append(currentSequence)
                            remainingJokers = jokers[:]  # jokers disponibles para esta secuencia
                            for v in expandWithJokers(currentSequence, remainingJokers, highMode):
                                straights.append(v)
                        #Reiniciamos la secuencia
                        currentSequence = [curr]

                #Al terminar el palo, procesamos la última secuencia
                if len(currentSequence) >= 3:
                    straights.append(currentSequence)
                    remainingJokers = jokers[:]
                    for v in expandWithJokers(currentSequence, remainingJokers, highMode):
                        straights.append(v)
                for s in straights: #Con esto, construimos secuencias alternas
                    #Se utilizará para construir seguidillas heredadas de algunas seguidillas mayores
                    #Ejemplo: Si nuestra seguidilla tiene 5 cartas, de allí podremos construir seguidillas de 4 cartas
                    #Otro ejemplo: Si nuestra seguidilla tiene 6 cartas, se podrán construir seguidillas de 5 cartas o 4 cartas,
                    #Según lo desee el jugador
                    if len(s) >= 5:
                        for i in range(len(s)):
                            altSeq1 = s[i+1:]
                            altSeq2 = s[:-i-1]
                            if len(altSeq1) >= 4 and altSeq1 not in straights:
                                straights.append(altSeq1)
                            if len(altSeq2) >= 4 and altSeq2 not in straights:
                                straights.append(altSeq2)
    
        return straights



    def insertCard(self, idPlayer): #Aún no tengo en claro si lo mejor sea utilizar el idPlayer como parámetro o colocar otra cosa en su lugar
        if self.downHand == True:
            #Aquí se implementaría la lógica para agregar una carta en la jugada de otro jugador
            pass
        else:
            print("No se puede insertar una carta porque el jugador no se ha bajado.") #Esto se cambiará por una alerta visual más adelante, pero de momento no nos preocupemos por lo visual :3
