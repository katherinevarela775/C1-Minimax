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