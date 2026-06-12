import random, os, time 

def movimientos_posibles(pos, oponente, tamano, tablero, es_gato=True): # es_gato = True es para la val. de restriccion
    """ Calcula los movimientos legales en el tablero consultando la matriz (tablero) y los filtra segun 3 criterios: limites, paredes y rest. de ocupacion """
    opciones = []
    for num_fila, num_columna in [(-1,0), (1,0), (0,-1), (0,1)]:
        nueva_pos = [pos[0]+num_fila, pos[1]+num_columna] 
        if 0 <= nueva_pos[0] < tamano and 0 <= nueva_pos[1] < tamano and tablero[nueva_pos[0]][nueva_pos[1]] != "⬛":  
            if not es_gato and nueva_pos == oponente: continue # Si es el raton y la nueva pos. es la del gato, la ignora
            opciones.append(tuple(nueva_pos))
    return opciones

def existe_camino(inicio, fin, tamano, tablero): 
    """BFS (Breadth-First Search): Garantiza que el laberinto tenga solución.""" # Conceptualizar mejor BFS
    cola, visitados = [inicio], [inicio]
    for actual in cola: 
        if actual == fin: return True 
        for vecina in movimientos_posibles(actual, [-1,-1], tamano, tablero, False): # Dentro de la iteracion de cola, explora los mov. posibles 
            if vecina not in visitados:
                visitados.append(vecina); cola.append(vecina) 
    return False 

def generar_juego(tamano):
    """Configura el estado inicial del mundo, unicamente la parte estatica del nivel""" # Explicacion del renderizado aparte
    gato, raton, salida = [0, 1], [tamano-1, tamano-1], [0, 0] 
    while True:
        tablero = [["⬜" for _ in range(tamano)] for _ in range(tamano)] 
        restringidas = [[0,0], [0,1], [1,0], [1,1], gato, raton] 
        
        for paredes in range((tamano ** 2) // 5): # En un rango proporcional a la sup. total de mi tablero
            filas, colum = random.randint(0, tamano-1), random.randint(0, tamano-1)
            if [filas, colum] not in restringidas: 
                tablero[filas][colum] = "⬛" 
        
        if existe_camino(raton, salida, tamano, tablero): 
            return {"tamano": tamano, "pos_gato": gato, "pos_raton": raton, "salida": salida, "tablero": tablero, "memoria": []} # Diccionario con la estructura del juego

def puntuar(datos, es_raton): 
    """Heurística: El motor de decisiones de la IA.""" # Heuristica: Dist. Manhattan para penalizacion
    gato, raton, salida = datos["pos_gato"], datos["pos_raton"], datos["salida"] 
    dist_gato_raton = abs(gato[0]-raton[0]) + abs(gato[1]-raton[1]) 
    dist_raton_salida = abs(raton[0]-salida[0]) + abs(raton[1]-salida[1]) #Las dist. Manhattan las utilizo para la penalizacion

    if es_raton:
        penalizacion = datos["memoria"].count(raton) * 60 
        return (dist_gato_raton * 5) - (dist_raton_salida * 60) - penalizacion + random.randint(0,5) 
    return -(dist_gato_raton * 200) + random.randint(0,5) 

def minimax(datos, prof, es_max): 
    """Simulador de estados futuros."""
    if datos["pos_gato"] == datos["pos_raton"]: return -20000 
    elif datos["pos_raton"] == datos["salida"]: return 20000 
    elif prof == 0: return puntuar(datos, es_max)  # Cuando la prof. llega a 0, deja de imaginar y utiliza la func. puntuar para evaluar que tan buena es la funcion actual

    mejor_valor = float('-inf') if es_max else float('inf') 
    yo = datos["pos_raton"] if es_max else datos["pos_gato"] 
    otro = datos["pos_gato"] if es_max else datos["pos_raton"]
    
    for movimiento in movimientos_posibles(yo, otro, datos["tamano"], datos["tablero"], not es_max):
        pos_original = tuple(yo) # ------------------> Conceptualizar mejor Backtracking

        if es_max: datos["pos_raton"] = movimiento 
        else: datos["pos_gato"] = movimiento 

        valor_minimax = minimax(datos, prof - 1, not es_max) # Llamamos a la funcion minimax, le restamos 1 a la prof. y pregunatamos por el oponente (Recursividad)
        mejor_valor = max(mejor_valor, valor_minimax) if es_max else min(mejor_valor, valor_minimax) # max y min comparan los dos valores que le entregues, max te devuelve el mayor y min el menor

        if es_max: datos["pos_raton"] = pos_original 
        else: datos["pos_gato"] = pos_original

    return mejor_valor # Resultado de la comparacion de max y min