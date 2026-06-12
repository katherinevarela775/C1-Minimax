import random, os, time

class Laberinto:
    def __init__(self, tamano):
        self.tamano = tamano
        self.pos_gato = [0, 1]
        self.pos_raton = [tamano - 1, tamano - 1]
        self.salida = [0, 0]
        self.quesos = []
        self.paredes = []
        self.memoria_raton = [] # Historial para evitar bucles
        self.generar_mapa()

    def generar_mapa(self):
        """Arquitecto del laberinto: coloca paredes y quesos asegurando solución."""
        while True:
            self.paredes = [] # Se agrega la lista vacia aqui para que cada vez que corra el bucle la misma se resetee
            seguras = [[0,0], [0,1], [1,0], [1,1], self.pos_gato, self.pos_raton] # Son las posiciones en donde no se pueden generar ningun tipo de objeto
            
            # Densidad de obstáculos
            for _ in range((self.tamano ** 2) // 7): # Determina cada cuanto segun el tamaño del mapa se puede generar paredes
                p = [random.randint(0, self.tamano-1), random.randint(0, self.tamano-1)] # Elige las ubicaciones de forma aleatoria 
                if p not in seguras and p not in self.paredes: # Validacion de que no es una coordenada restringida y de que ya no estan en la lista de ubicaciones ya elegidas
                    self.paredes.append(p) # Si pasa la validacion la agrega a la lista
            
            # Control de calidad: ¿Es posible ganar?
            if self.existe_camino(self.pos_raton, self.salida): # Si el mapa es jugable esta validacion agrega los quesos al mapa y se rompe el bucle de generacion
                self.colocar_quesos(seguras)
                break
    
    def existe_camino(self, inicio, fin):
        """Inspector: Algoritmo BFS para garantizar conectividad."""
        cola = [inicio] # Es donde se almacenan las posiciones que no se revisaron a profundidad (en las cuatro direcciones adyacentes)
        visitados = [inicio] # Es la lista donde se almacenan todas las coordenadas que ya itero o "visito"

        for actual in cola: # Sirve para ir revisando los caminos a lo largo del mapa
            if actual == fin: return True # Si al momento de iterar el mapa llega a la posicion de la salida la iteracion termina
            for vecino in self.movimientos_posibles(actual, [], es_gato=False):
                if vecino not in visitados: # Si la posicion no se encuentra en visitados la agrega y tambien a la lista de cola para revisarla a profundidad
                    visitados.append(vecino)
                    cola.append(vecino)
        return False # Si la lista de cola se vacia y nunca llegamos al fin, el codigo devuelve false, lo que significa que no encontro una salida en este mapa
    
    def colocar_quesos(self, seguras): # Esta funcion recibe la lista de seguras para saber donde tiene prohibido actuar
        self.quesos = [] # Se coloca la lista nuevamente dentro de la funcion para asegurarnos que la misma esta vacia
        while len(self.quesos) < 3: # El bucle se ejecuta hasta que hayan 3 quessos ubicados en el mapa
            q = [random.randint(0, self.tamano-1), random.randint(0, self.tamano-1)] # Aqui elige coordenadas al azar para ubicar los quesos y utiliza randint(0, tamano-1) para que los mismos se ubiquen dentro de los limites del mapa
            if q not in self.paredes and q not in seguras and q not in self.quesos: # Aqui hay una validacion triple de no haya una pared en ese lugar, no sea una zona prohibida y que tampoco haya ya un queso en esa posicion
                self.quesos.append(q) # Si pasa la triple validacion se agrega a la lista

    def movimientos_posibles(self, pos, oponente, es_gato=True): # Esta funcion recibe los datos de la posicion, la posicion del oponente y la de cual personaje pregunta
        """Reglas de física del juego: a dónde se puede mover un agente."""
        opciones = [] # Aqui se guardan los caminos legales a medida que se va explorando los alrededores
        for df, dc in [(-1,0), (1,0), (0,-1), (0,1)]: # Aqui se definen las 4 direcciones en las que se pueden mover y las ira probando una a una
            nueva_pos = [pos[0]+df, pos[1]+dc] # Es un simulacro de que pasaria si me mueve hacia arriba 
            if 0 <= nueva_pos[0] < self.tamano and 0 <= nueva_pos[1] < self.tamano:# Esta validacion camprueba de que la posicion no se salga del tablero
                if nueva_pos not in self.paredes: # Validacion de si existe una pared en esa posicion
                    if not es_gato and nueva_pos == oponente: continue # Aqui lo que hace es que en caso de ser el raton y querer moverse a la posicion del gato, el continue hace que pase a otra posicion 
                    opciones.append(nueva_pos) 

    def dibujar(self, turno, m_gato, m_raton): # Es como el monitor del juego, y necesita tres datos para funcionar, el turno actual y quien esta controlando al gato y al raton
        """Interfaz visual adaptable."""
        os.system('cls' if os.name == 'nt' else 'clear') # Esta linea se encarga de borrar todo lo que hay en la consola despues de cada turno
        info = f" TURNO: {turno:2} | GATO: {m_gato:8} | RATÓN: {m_raton:8} "
        ancho = max(len(info), self.tamano * 3) # En estas lineas se prepara el marcador, el marco del mismo se ajusta segun el tamaño del mapa
        
        print(f"╔{'═' * ancho}╗")
        print(f"║{info.center(ancho)}║") # Estos son los los borde de nuestro marcador
        print(f"╚{'═' * ancho}╝")
        
        for f in range(self.tamano): # Aqui empieza a recorrer el tablero linea por linea y prepara un reglon vacio para empezar a colocar los iconos
            fila = ""
            for c in range(self.tamano):
                p = [f, c]
                if p == self.pos_gato: fila += "🐱 "
                elif p == self.pos_raton: fila += "🐭 "
                elif p == self.salida: fila += "🚪 " # Esta parte mediante validaciones de posicion o de si existe en x lista, coloca los iconos corresp. a cada parte del mapa
                elif p in self.quesos: fila += "🧀 "
                elif p in self.paredes: fila += "⬛ " # Dato: esta parte del codigo usa abstraccion al coordenadas en lo que buscamos
                else: fila += "⬜ "
            print(fila) # Y se imprime el mapa en la pantalla

    def puntuar_estado(self, es_raton): # Es como un juez, el cual como dato necesita saber si a quien juzga
        """Heurística: Sistema de valores de la IA."""
        dist_gr = abs(self.pos_gato[0]-self.pos_raton[0]) + abs(self.pos_gato[1]-self.pos_raton[1]) # Aqui se calcula la dist. Manhattan en donde sumamos la cnat. de pasos en hor. y vert. 
        dist_rs = abs(self.pos_raton[0]-self.salida[0]) + abs(self.pos_raton[1]-self.salida[1]) # dist_gr: Dist. entre el gato y el raton; dist_rs: Dist. entre el raton y la salida
        
        if es_raton: # ("Psicologia del Raton")
            penalizacion = self.memoria_raton.count(self.pos_raton) * 50 # Penalizacion por repetir una casilla en la que estuvo hace poco 
            return (dist_gr * 5) - (dist_rs * 60) - penalizacion + random.randint(0,5) # - penalizacion: Si el raton estuvo hace poco en esa casilla pierde puntos 
        else:
            return -(dist_gr * 200) + random.randint(0,5) # -(dist_gr * 200): Esto aplica al gato, cuan mayor sea la distancia, menor sera su puntaje, lo que hace que prioreice reducir la distancia

    def ia_decidir(self, profundidad, es_max): # Es un simulador de que pasaria si, recibe los datos de profundidad y de si es max, si max = True saca la nota mas alta, y si es false dara la nota mas baja
        """Simulador Minimax."""
        if self.pos_gato == self.pos_raton: return -20000 # Antes de ejecutarse valida los caos finales de si gano el gato(-2000) o el raton (2000)
        if self.pos_raton == self.salida: return 20000
        if profundidad == 0: return self.puntuar_estado(es_max) # Si la profundidad llego a cero y utiliza la funcion de evaluar estado para ver quien esta en la mejor psoicion en ese momento

        mejor_valor = float('-inf') if es_max else float('inf') # Aqui define el punto de partida segun quien sea, si es max empieza con el num mas pequeño (- infinito), y si es min con el mas grande (infinito)
        yo = self.pos_raton if es_max else self.pos_gato
        el_otro = self.pos_gato if es_max else self.pos_raton
        
        for mov in self.movimientos_posibles(yo, el_otro, es_gato=not es_max): # Aqui inicia la ramificacion donde se abre el abanico de posibilidades que tiene en ese turno imaginario
            pos_original = list(yo) # Aqui la IA mueve la pieza en el tablero virtual
            if es_max: self.pos_raton = mov
            else: self.pos_gato = mov
            
            valor = self.ia_decidir(profundidad - 1, not es_max) # Aqui ocurre la recursividad, la funcion se llama a si misma, para imaginar que haria el oponente desde esta nueva posicion que imagino
            mejor_valor = max(mejor_valor, valor) if es_max else min(mejor_valor, valor) 
            
            if es_max: self.pos_raton = pos_original 
            else: self.pos_gato = pos_original
        return mejor_valor 
    
    def ejecutar_turno_ia(self, es_raton): # Es la que toma decision final y mueve la pieza fisicamente en el tablero, recibe el dato de que personaje es para saber que logica ejecutar
        """Toma de decisión oficial."""
        yo = self.pos_raton if es_raton else self.pos_gato # Aqui lo primero que hace es reconocerse a si misma y al rival
        el_otro = self.pos_gato if es_raton else self.pos_raton
        prof = 3 if es_raton else 4 # Define que tan inteligente sera cada uno (cuantos paso en el futuro vera cada personaje)
        
        mejor_m, mejor_p = yo, (float('-inf') if es_raton else float('inf')) # mejor_m guardará el mejor movimiento encontrado y mejor_p la mejor puntuación. Se empieza con el peor o mejor valor posible, para que asi cualquier opcion lo supere de inmediato
        
        for m in self.movimientos_posibles(yo, el_otro, es_gato=not es_raton): # Este bucle mira los movimientos que puede hacer ahora mismo

            original = list(yo) # Aqui guarda la posicion real de la pieza, antes de realizar las simulaciones
            if es_raton: self.pos_raton = m # Para cada mov. posible le pregunta a la funcion de ia_decidir de si es conveniente
            else: self.pos_gato = m  

            puntuacion = self.ia_decidir(prof, not es_raton)

            if (es_raton and puntuacion > mejor_p) or (not es_raton and puntuacion < mejor_p):
                mejor_p, mejor_m = puntuacion, m # Si el el raton o el gato encuentran una mejor puntuacion a la que tenian anotada, actualizan su mejor opcion
            elif es_raton: # Aqui deshace el movimiento de prueba 
                self.pos_raton = original
            else: self.pos_gato = original
            
        if es_raton:
            self.pos_raton = mejor_m
            self.memoria_raton.append(list(mejor_m)) # El raton finalmente cambia su posicion en el mapa y anota la misma en la lista para no repetirla
            if len(self.memoria_raton) > 5: self.memoria_raton.pop(0) # Es el límite de la "memoria a corto plazo" del ratón. Solo recuerda los últimos 5 pasos que dio. Y el pop elimina el recuerdo mas viejo
            elif self.pos_raton in self.quesos: self.quesos.remove(self.pos_raton) # Esto lo que hace es que si la posicion del raton coincide con la del queso, se remueve el queso de esa posicion
        else:
            self.pos_gato = mejor_m