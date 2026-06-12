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