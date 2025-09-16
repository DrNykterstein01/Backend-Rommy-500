import pygame
from Round import Round
from Card import Card
from itertools import combinations
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
        self.playerCardsToEx = []   # Atrib. exp., para guardar cartas para intercambiar posiciones.
        self.playMade = []
        self.downHand = False #Este atributo nos indica si el jugador ya se bajó o no, mostrando True o False respectivamente
        #self.playerBuy = False
        self.playerPass = False #Atrib. experimental, para saber si pasó de la carta descartada.

    # Mét. para permitir que el jugador seleccione cartas para jugar.
    def chooseCard(self, clickPos):
        
        # Para cada carta en la mano del jugador, verificamos si se hace click en el rectángulo asociado
        # a una carta específica y si dicha carta ha sido previamente seleccionada.
        # Si la carta no está en la lista de seleccionadas, la incluimos; si resulta que está entre las
        # seleccionadas y se vuelve a hacer click en ella, la eliminamos de la lista.
        # NOTA: Con la inclusión de un ID a cada carta este proceso se simplifica, ya que las coincidencias
        #       sólo pueden darse entre cartas con un mismo valor para todos sus atributos.
        for card in self.playerHand:
            if self.playerCardsPos[card].collidepoint(clickPos) and card not in self.playerCardsSelect:
                print(f"Carta marcada: {card}{card.id}")
                self.playerCardsSelect.append(card)
            elif self.playerCardsPos[card].collidepoint(clickPos) and card in self.playerCardsSelect:
                print(f"Carta desmarcada: {card}{card.id}")
                self.playerCardsSelect.remove(card)

    # Mét. para permitir al jugador intercambiar el lugar de sus cartas para que pueda ordenarlas.
    # Trabaja casi igual que chooseCard(), pero almacena dos cartas a lo mucho.
    def exchangeCard(self, clickPos):
        for card in self.playerHand:
            if self.playerCardsPos[card].collidepoint(clickPos) and card not in self.playerCardsToEx:
                print(f"Carta marcada para intercambiar: {card}{card.id}")
                self.playerCardsToEx.append(card)
            elif self.playerCardsPos[card].collidepoint(clickPos) and card in self.playerCardsToEx:
                print(f"Carta desmarcada para intercambiar: {card}{card.id}")
                self.playerCardsToEx.remove(card)

        # Si el jugador marca dos cartas para intercambiar (con el click derecho)...
        if len(self.playerCardsToEx) == 2:
                
                # Tomamos la posición de cada carta en la mano del jugador.
                IndexFirstCard = self.playerHand.index(self.playerCardsToEx[0])
                IndexSecondCard = self.playerHand.index(self.playerCardsToEx[1])

                # Tomamos las cartas asociadas a cada posición.
                firstCard = self.playerHand[IndexFirstCard]
                secondCard = self.playerHand[IndexSecondCard]

                # Intercambiamos posiciones en la mano del jugador.
                self.playerHand[IndexFirstCard] = secondCard
                self.playerHand[IndexSecondCard] = firstCard

                # Limpiamos la lista de intercambio para reiniciar el proceso.
                self.playerCardsToEx.clear()    
                
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
            for i, combination in enumerate(valid_combos, 1): #Simplemente nos imprime en pantalla las combinaciones disponibles en la mano del jugador
                print(f"   Opción {i}:")
                print(f"     Trío -> {[str(c) for c in combination['trio']]}")
                print(f"     Seguidilla -> {[str(c) for c in combination['straight']]}")
            return valid_combos
        else:
            print(f"\n❌ El jugador {self.playerName} NO se puede bajar aún.")
            return None
        #NOTA: Al final, tengo pensado que para que un jugador se pueda bajar, deba organizar su jugada
        #de tal manera que la combinación de cartas que va a bajar coincida con alguna de las combinaciones
        #que retorna este método canGetOff().

    def getOff(self):
        combinations = self.canGetOff()
        availableTrios = [combination["trio"] for combination in combinations] if combinations != None else [] #Esto nos crea una lista con todas las combinaciones de tríos disponibles
        prepareTrio = []
        availableStraights = [combination["straight"] for combination in combinations] if combinations != None else [] #Nos crea una lista con todas las combinaciones de seguidillas válidas disponibles
        prepareStraight = []
        chosenCards = self.playerCardsSelect

        if not chosenCards:
            print("El jugador aún no ha seleccionado cartas")
            return None

        if len(chosenCards) >= 7: #CORREGIR LO QUE ESTÁ EN ESTE BUCLE
            for trio in availableTrios: #Esto nos crea una lista con todas las cartas que se van a descartar
                for straight in availableStraights:
                    for card in chosenCards:
                        if card in trio and card in self.playerHand and card not in prepareTrio:
                            prepareTrio.append(card)
                        elif card in straight and card in self.playerHand and card not in prepareStraight:
                            prepareStraight.append(card)
                        #elif card not in trio and card not in straight and card in self.playerHand:
                            #print("Carta no disponible para el trío o la seguidilla")
                    #print(f"Cartas de la seguidilla: {[str(c) for c in prepareStraight]}")
                    #print(f"Cartas del trío: {[str(c) for c in prepareTrio]}")
            if any(card not in prepareTrio and card not in prepareStraight for card in chosenCards):
                print("Alguna de las cartas seleccionadas no se encuentra en el trío o en la seguidilla")
            if self.downHand:
                print("El jugador ya se bajó en esta ronda. No puede volver a bajarse")
            else:
                if len(prepareTrio) >= 3 and len(prepareStraight) >= 4 and len(chosenCards) >= 7 and any(prepareStraight == straight for straight in availableStraights):
                    self.playMade.append({"trio": prepareTrio, "straight": prepareStraight})
                    for card in prepareTrio:
                        self.playerHand.remove(card)
                    for card in prepareStraight:
                        self.playerHand.remove(card)
                    self.downHand = True
                    print(f"El jugador {self.playerName} se bajó con: \n     Trío -> {[str(c) for c in prepareTrio]}\n     Seguidilla -> {[str(c) for c in prepareStraight]}")
                    return prepareTrio, prepareStraight


        elif len(chosenCards) < 7:
            print(f"Se han seleccionado {len(chosenCards)} cartas, no son suficientes aún.")

    def findTrios(self):
        trios = []  #Esta lista va a almacenar todos los tríos posibles en la mano del jugador
        cardsPerValue = {}  #Diccionario para almacenar las cartas por valor
        jokers = []  #Jokers que hay en la mano del jugador

        #Clasificamos las cartas en normales y jokers
        for card in self.playerHand:
            if card.joker:
                jokers.append(card)
            else:
                if card.value not in cardsPerValue:
                    cardsPerValue[card.value] = []
                cardsPerValue[card.value].append(card)

        #Incluimos los jokers como valor especial para más adelante hacer combinaciones
        if jokers:
            cardsPerValue["Joker"] = jokers

        #A partir de aquí comenzamos a generar posibles tríos, partiendo de los grupos de cartas en el diccionario
        for value, cards in cardsPerValue.items():
            if value == "Joker":
                continue  #No se pueden formar tríos solo con jokers

            totalCards = cards.copy()  #Creamos una copia de las cartas (con su valor) para no modificar la original
            if jokers:
                totalCards += jokers  #Añadimos los jokers a la lista temporal

            #Creamos todas las combinaciones de tamaño 3 o más (independientemente de la cantidad de cartas
            #del mismo valor que tenga el jugador en su mano)
            for size in range(3, len(totalCards) + 1):
                for combination in combinations(totalCards, size):
                    jokerCount = sum(1 for c in combination if c.joker)

                    # Restricción: máximo 1 Joker por trío
                    if jokerCount <= 1:
                        # Evitar duplicados
                        sortedCombo = sorted(combination, key=lambda c: (c.joker, c.value, c.type))
                        if sortedCombo not in trios:
                            trios.append(sortedCombo)

        return trios

    
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

        def isConsecutiveWithJokers(c1, c2, highAs):
            return rank(c2, highAs) - rank(c1, highAs) == 2

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
                    usedJokers = sum(1 for card in currentSequence if getattr(card, "joker", False))

                    #Caso A->2, que es manejado por rank() cuando highMode = False
                    if isConsecutive(prev, curr, highMode):
                        currentSequence.append(curr)
                    elif isConsecutiveWithJokers(prev, curr, highMode) and usedJokers < len(jokers):
                        currentSequence.append(jokers[usedJokers])
                        jokers.remove(jokers[usedJokers])
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


    def insertCard(self, targetPlayer, targetPlayIndex, cardToInsert, position=None):
        """
        Inserta una carta en targetPlayer.playMade[targetPlayIndex].
        position: 'start', 'end' o None para sustitución de Joker.
        Requisitos: self.downHand == True y cardToInsert in self.playerHand
        """

        # 1) Validaciones básicas
        if not self.downHand:
            print(f"❌ {self.playerName} no puede insertar cartas: aún no se ha bajado.")
            return False

        if cardToInsert not in self.playerHand:
            print(f"❌ {self.playerName} no tiene la carta {cardToInsert} en su mano.")
            return False

        if targetPlayIndex < 0 or targetPlayIndex >= len(targetPlayer.playMade):
            print("❌ El índice dado para la jugada objetivo es inválido.")
            return False

        targetPlay = targetPlayer.playMade[targetPlayIndex]
        temporalPlay = targetPlay.copy()

        # Mapa para ranks (A tratado luego según modo)
        valueToRank = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
            "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13
        }

        def isJoker(c):
            return getattr(c, "joker", False)

        # ---------- Validación TRÍO ----------
        def isValidTrio(play):
            # Un trío debe tener exactamente 3 cartas (o 3 con 1 Joker)
            if len(play) < 3:
                return False
            jokers = [c for c in play if isJoker(c)]
            nonJokers = [c for c in play if not isJoker(c)]
            # Regla: no más de 1 joker en trío
            if len(jokers) > 1:
                return False
            if len(nonJokers) == 0:
                return False
            values = [c.value for c in nonJokers]
            return len(set(values)) == 1

        # ---------- Validación SEGUIDILLA ----------
        def isValidStraight(play):
            # Debe tener al menos 4 cartas totales
            if len(play) < 4:
                return False

            # No permitir jokers adyacentes
            for i in range(len(play) - 1):
                if isJoker(play[i]) and isJoker(play[i + 1]):
                    return False

            # Validar palos (los no-jokers deben pertenecer al mismo palo)
            suits = [c.type for c in play if not isJoker(c)]
            if len(suits) == 0:
                return False
            if len(set(suits)) > 1:
                return False

            # Intentaremos ambos modos: As como bajo (A=1) y As como alto (A=14)
            for highAs in (False, True):
                # Construir lista de ranks (None para jokers)
                ranks = []
                okMode = True #
                for c in play:
                    if isJoker(c):
                        ranks.append(None)
                    else:
                        if c.value == "A":
                            r = 14 if highAs else 1
                        else:
                            if c.value not in valueToRank:
                                okMode = False
                                break
                            r = valueToRank[c.value]
                        ranks.append(r)
                if not okMode:
                    continue

                # Debe haber al menos un non-joker para fijar la base
                nonIndex = [i for i, r in enumerate(ranks) if r is not None]
                if not nonIndex:
                    continue

                # Calcular el "base" candidato: r - pos para cada non-joker
                baseSet = set(ranks[i] - i for i in nonIndex)
                if len(baseSet) != 1:
                    continue
                base = baseSet.pop()

                # Comprobar que los expected ranks estén en 1..14 y coincidan con non-jokers
                expectedOk = True
                for pos, r in enumerate(ranks):
                    expected = base + pos
                    if expected < 1 or expected > 14:
                        expectedOk = False
                        break
                    if r is not None and r != expected:
                        expectedOk = False
                        break
                if not expectedOk:
                    continue

                # Reglas específicas con As:
                # Si hay un As en play:
                for i, c in enumerate(play):
                    if not isJoker(c) and c.value == "A":
                        # As como bajo: no debe haber ningún Joker antes de esa A
                        if not highAs:
                            if any(isJoker(play[j]) for j in range(0, i)):
                                expectedOk = False
                                break
                        # As como alto: no debe haber ningún Joker después de esa A
                        else:
                            if any(isJoker(play[j]) for j in range(i + 1, len(play))):
                                expectedOk = False
                                break
                if not expectedOk:
                    continue

                # Si llegamos hasta aquí, el modo es válido => la secuencia es válida
                return True

            # Ningún modo válido
            return False

        # ---------- Detectar si la jugada objetivo "parece" trío ----------
        def isTrioLike(play):
            # heurística: si la mayoría de cartas no-joker comparten valor y longitud <= 4
            nonJokers = [c for c in play if not isJoker(c)]
            if not nonJokers:
                return False
            values = [c.value for c in nonJokers]
            return len(play) <= 4 and len(set(values)) == 1

        isTrioTarget = isTrioLike(targetPlay)

        # ---------- Simular la operación ----------
        if position is None:
            # sustitución: buscar primer Joker
            jokerIndex = next((i for i, c in enumerate(temporalPlay) if isJoker(c)), None)
            if jokerIndex is None:
                print("❌ No hay Joker para sustituir en esta jugada.")
                return False
            temporalPlay[jokerIndex] = cardToInsert
        elif position == "start":
            temporalPlay.insert(0, cardToInsert)
        elif position == "end":
            temporalPlay.append(cardToInsert)
        else:
            print("❌ Posición inválida. Usa 'start', 'end' o None.")
            return False

        # ---------- Validar la jugada simulada (sin depender de findStraight/findTrios) ----------
        if isTrioTarget:
            valid = isValidTrio(temporalPlay)
        else:
            valid = isValidStraight(temporalPlay)

        if not valid:
            if isTrioTarget:
                print("❌ La sustitución/inserción rompe el trío: operación rechazada.")
            else:
                print("❌ La carta no puede insertarse: la seguidilla resultante no es válida.")
            return False

        # ---------- Aplicar cambios reales ----------
        if position is None:
            # Reemplazar el Joker real y devolver esa instancia de Joker a la mano del que inserta
            jokerIndexReal = next((i for i, c in enumerate(targetPlay) if isJoker(c)), None)
            if jokerIndexReal is None:
                print("❌ (race) No hay Joker real para sustituir.")
                return False
            replacedJoker = targetPlay[jokerIndexReal]
            targetPlay[jokerIndexReal] = cardToInsert
            # quitar carta del que inserta y devolver el Joker real a su mano
            self.playerHand.remove(cardToInsert)
            self.playerHand.append(replacedJoker)
            print(f"🔄 {self.playerName} sustituyó un Joker con {cardToInsert} (Joker -> mano).")
            return True
        else:
            # Insert real al inicio o final
            if position == "start":
                targetPlay.insert(0, cardToInsert)
                print(f"⬅️ {self.playerName} agregó {cardToInsert} al inicio de la jugada.")
            else:
                targetPlay.append(cardToInsert)
                print(f"➡️ {self.playerName} agregó {cardToInsert} al final de la jugada.")
            self.playerHand.remove(cardToInsert)
            return True

    # Mét. para cambiar el valor de "playerPass" para saber si, en un turno dado, pasó de la carta del
    # descarte y agarró del mazo de disponibles. Servirá para la compra de cartas de los siguientes
    # jugadores.
    def passCard(self):
        self.playerPass = not self.playerPass
