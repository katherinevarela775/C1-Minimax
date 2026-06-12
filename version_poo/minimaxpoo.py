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
            for vecino in self.movimientos_posibles(actual, [], es_gato=False): # Desde el punto en el que se encuentra, mira a las 4 direcciones posibles y la funcion de movimientos posibles filtara las paredes y bordes
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
                    opciones.append(nueva_pos) # Si el movimiento paso todas las validaciones se guarda en opciones
        return opciones # Aqui te entrega la lista con los movs. validos

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