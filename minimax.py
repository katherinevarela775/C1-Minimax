import random, os, time 

# - Logica del Mapa y Caminos - 

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
    """BFS (Breadth-First Search): Garantiza que el laberinto tenga solución.""" # BFS: Algoritmo para recorrer elementos en arboles
    cola, visitados = [inicio], [inicio]
    while cola:
        actual = cola.pop(0) 
        if list(actual) == fin: return True 
        for vecina in movimientos_posibles(actual, [-1,-1], tamano, tablero, False): # Revisa primero a los vecinos a un paso de dist., luego pasa alos que estan a 2 y asi sucesivamente
            if vecina not in visitados:
                visitados.append(vecina); cola.append(vecina)
    return False 

def generar_juego(tamano):
    """Configura el estado inicial del mundo, unicamente la parte estatica del nivel""" # al ser la parte dinamica algo aparte, a la hora de que minimax simule el futuro solo debe cambiar unas coordenadas en lugar de copiar y restaurar toda la matriz
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

# - Inteligencia Artificial-

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
    elif prof == 0: return puntuar(datos, es_max)  # Cuando la prof. llega a 0, deja de imaginar y utiliza la func. puntuar para evaluar que tan buena es el estado actual

    mejor_valor = float('-inf') if es_max else float('inf') 
    yo = datos["pos_raton"] if es_max else datos["pos_gato"] 
    otro = datos["pos_gato"] if es_max else datos["pos_raton"]
    
    for movimiento in movimientos_posibles(yo, otro, datos["tamano"], datos["tablero"], not es_max):
        pos_original = tuple(yo) # ------------------> Backtracking: tec. algorit. recursiva que utilizas para probar todas las posibilidades pero quieres descartar rápido las que no funcionan

        if es_max: datos["pos_raton"] = movimiento 
        else: datos["pos_gato"] = movimiento 

        valor_minimax = minimax(datos, prof - 1, not es_max) # Llamamos a la funcion minimax, le restamos 1 a la prof. y pregunatamos por el oponente (Recursividad)
        mejor_valor = max(mejor_valor, valor_minimax) if es_max else min(mejor_valor, valor_minimax) # max y min comparan los dos valores que le entregues, max te devuelve el mayor y min el menor

        if es_max: datos["pos_raton"] = pos_original 
        else: datos["pos_gato"] = pos_original

    return mejor_valor # Resultado de la comparacion de max y min

def mover_ia(datos, es_raton): 
    """Aplica la mejor decisión del Minimax al mundo real y actualiza los estados de los personajes."""
    yo = datos["pos_raton"] if es_raton else datos["pos_gato"] 
    otro = datos["pos_gato"] if es_raton else datos["pos_raton"]
    mejor_mov, mejor_punt = yo, (float('-inf') if es_raton else float('inf')) 

    for movimiento in movimientos_posibles(yo, otro, datos["tamano"], datos["tablero"], not es_raton):
        pos_original = tuple(yo) #Backtracking

        if es_raton: datos["pos_raton"] = movimiento 
        else: datos["pos_gato"] = movimiento

        simulacion = minimax(datos, 3 if es_raton else 4, not es_raton) # Aqui llamamos a la funcion minimax con la prof. de 3 para el raton y de 4 para el gato

        if (es_raton and simulacion > mejor_punt) or (not es_raton and simulacion < mejor_punt): # Aqui comparamos el resultado de la sim. con el mejor puntaje
            mejor_punt, mejor_mov = simulacion, movimiento # Si el valor es mejor, lo guardamos

        if es_raton: datos["pos_raton"] = pos_original 
        else: datos["pos_gato"] = pos_original
            
    if es_raton: 
        datos["pos_raton"] = mejor_mov # Una vez termino el bucle tomamos las decis. final y movemos la pieza a mejor_m
        datos["memoria"].append(tuple(mejor_mov))
        if len(datos["memoria"]) > 5: datos["memoria"].pop(0) 

    else:
        datos["pos_gato"] = mejor_mov 

# --- MOTOR DE JUEGO ---

def dibujar(datos, turn): 
    """ Es el motor de Renderizado, limpia la consola e imprime los diseños. """ 
    os.system('cls' if os.name == 'nt' else 'clear') # Limpia la consola
    print(f" TURNO: {turn} | MODO:  IA vs IA ".center(datos["tamano"]*3, "═")) 

    for f in range(datos["tamano"]): 
        texto_fila = "" 
        for c in range(datos["tamano"]): 
            coord_a_revisar = [f, c] # Representa la coord. actual que esta siendo iterada
            if list(coord_a_revisar) == list(datos["pos_gato"]): texto_fila += "🐱 "
            elif list(coord_a_revisar) == list(datos["pos_raton"]): texto_fila += "🐭 " 
            elif list(coord_a_revisar) == list(datos["salida"]): texto_fila += "🚪 "
            else:
                texto_fila += datos["tablero"][f][c] + " " # Realiza una concatenacion de las cadenas que contienen los pisos y la de esta funcion
        print(texto_fila) 



def jugar(): 
    """ Es el bucle principal del juego, alterna turnos, gestiona la cantidad de los mismos y verificas estados. """
    juego = generar_juego(tamano=10) # Crea el tablero y coloca a los personajes
    historial = {} # Diccionario
    
    for turn in range(1, 61): 
        estado = (tuple(juego["pos_gato"]), tuple(juego["pos_raton"])) # Convierte la lista de coord. de cada personaje y las convierte en tuplas, para poder agg. al diccionario
        historial[estado] = historial.get(estado, 0) + 1 # Aqui busca variable estado, si existe +1, y le pone la cond. de que si no encuentra nada simplemente devuelva 0
        if historial[estado] >= 5: 
            dibujar(juego, turn); print("\n🤝 EMPATE: Bucle detectado."); return

        dibujar(juego, turn) 
        mover_ia(juego, True) # Turno del raton
        if list(juego["pos_raton"]) == juego["salida"]: # Accede a esa info desde juego, ya que la funcion generar_juego te retorna un dicc. cuando se cumple
            dibujar(juego, turn); print("\n🏁 Final: El ratón escapó."); return 
            
        dibujar(juego, turn) 
        time.sleep(0.5) 
        mover_ia(juego, False) # Turno del gato
        if list(juego["pos_gato"]) == juego["pos_raton"]:
            dibujar(juego, turn); print("\n⚔️ Final: El gato atrapó al ratón."); return
    dibujar(juego, turn)
    print("\n⏰ TIEMPO AGOTADO: El ratón se cansó y el gato se durmió.")


jugar()
