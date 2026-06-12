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