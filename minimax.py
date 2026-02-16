import random, os, time

# - Logica del Mapa y Caminos - 

def movimientos_posibles(pos, oponente, tamano, tablero, es_gato=True): # pos: posicion actual, oponente: posic. del oponente, es_gato: dato booleano para evitar que el raton pise al gato pero si viceversa
    """Define los movimientos legales en el tablero consultando la matriz."""
    opciones = []
    for df, dc in [(-1,0), (1,0), (0,-1), (0,1)]: # Para filas y columnas en las direcciones que puede usar
        n = [pos[0]+df, pos[1]+dc] # Calcula la nueva posicion sumando el mov. a la posicion actual
        # Filtro que revisa que no se salga en x ni en y, y que no choca con un muro en la matriz
        if 0 <= n[0] < tamano and 0 <= n[1] < tamano and tablero[n[0]][n[1]] != "⬛": 
            if not es_gato and n == oponente: continue # Si el que mueve es el raton y la posicion es la del gato, con continue ignoramos la opcion
            opciones.append(n) # Si paso todos los filtros se agrega a la lista de opciones
    return opciones

def existe_camino(inicio, fin, tamano, tablero): 
    """BFS (Breadth-First Search): Garantiza que el laberinto tenga solución."""
    cola, visitados = [inicio], [inicio] # cola: casillas por explorar, visitados: casillas visitadas
    for actual in cola: # Itera mientras haya casillas en cola
        if actual == fin: return True # Si la casilla que estamos iterando es igual a la casilla, se termina
        # Pedimos las casillas vecinas legales, el [-1, -1] aqui actua como un oponente fantasma para poder usar la funcion, y el False es por que el raton es el unico que necesita llegar a la salida
        for vecina in movimientos_posibles(actual, [-1,-1], tamano, tablero, False): 
            if vecina not in visitados:
                visitados.append(vecina); cola.append(vecina) # Si no visitamos aun esa casilla se agrega a visitados, y a cola para revisar desde ahi las demas casillas vecinas 
    return False # Si nada se cumple, esta funcion se vuelve a ejecutar en el proximo mapa que se genere

def generar_juego(tamano):
    """Configura el estado inicial del mundo."""
    gato, raton, salida = [0, 1], [tamano-1, tamano-1], [0, 0] # Pos. fijas iniciales
    while True:
        tablero = [["⬜" for _ in range(tamano)] for _ in range(tamano)] # Creamos el tablero como una matriz de listas (llena de suelo ⬜)
        seguras = [[0,0], [0,1], [1,0], [1,1], gato, raton] # Coord. en donde no pueden aparecer paredes
        
        for _ in range((tamano ** 2) // 7): # Crea una cant. de paredes proporcional al tamaño del tablero
            fila, colum = random.randint(0, tamano-1), random.randint(0, tamano-1) # Genera una coord. al azar en el rango de 0 y el tamaño del mapa
            if [fila, colum] not in seguras: 
                tablero[fila][colum] = "⬛" # Si la coord. esta libre, le ponemos una pared :) (se marca en la matriz)
        
        if existe_camino(raton, salida, tamano, tablero): # Aca llamamos a la funcion anterior y si esta se cumplio (hay camino)
            return {"tamano": tamano, "pos_gato": gato, "pos_raton": raton, "salida": salida, "tablero": tablero, "memoria": []} # Devolvemos un diccionario con todo el estado del juego

# - Inteligencia Artificial-

def puntuar(datos, es_raton): # Esta funcion le da una puntuacion a una pos. especifica
    """Heurística: El motor de decisiones de la IA."""
    gato, raton, salida = datos["pos_gato"], datos["pos_raton"], datos["salida"] # Extrae la info de las posiciones de diccionario datos
    d_gr = abs(gato[0]-raton[0]) + abs(gato[1]-raton[1]) # Distancia Manhattan Gato-Ratón, abs: valor absoluto
    d_rs = abs(raton[0]-salida[0]) + abs(raton[1]-salida[1]) # Distancia Manhattan Ratón-Salida

    if es_raton:
        penal = datos["memoria"].count(raton) * 60 # Aca guardamos en la memoria los ult. 5 movs. y penalizamos si se repiten
        return (d_gr * 5) - (d_rs * 60) - penal + random.randint(0,5) # Estar lejos del gato le da unos puntos, pero quedarse lejos de la salida le resta muchos mas, y el random.int es un poco de caos para que elija un camino al azar en caso de haber dos iguales
    return -(d_gr * 200) + random.randint(0,5) # En caso de evaluar al gato, cuan mayor sea la dist. entre el y el raton mas puntos pierde

def minimax(datos, prof, es_max):
    """Simulador de estados futuros."""
    if datos["pos_gato"] == datos["pos_raton"]: return -20000
    if datos["pos_raton"] == datos["salida"]: return 20000
    if prof == 0: return puntuar(datos, es_max)

    mejor = float('-inf') if es_max else float('inf')
    yo = datos["pos_raton"] if es_max else datos["pos_gato"]
    otro = datos["pos_gato"] if es_max else datos["pos_raton"]
    
    for m in movimientos_posibles(yo, otro, datos["tamano"], datos["tablero"], not es_max):
        orig = list(yo)
        if es_max: datos["pos_raton"] = m
        else: datos["pos_gato"] = m
        val = minimax(datos, prof - 1, not es_max)
        mejor = max(mejor, val) if es_max else min(mejor, val)
        if es_max: datos["pos_raton"] = orig
        else: datos["pos_gato"] = orig
    return mejor

def mover_ia(datos, es_raton):
    """Aplica la mejor decisión del Minimax al mundo real."""
    yo = datos["pos_raton"] if es_raton else datos["pos_gato"]
    otro = datos["pos_gato"] if es_raton else datos["pos_raton"]
    mejor_m, mejor_p = yo, (float('-inf') if es_raton else float('inf'))
    
    for m in movimientos_posibles(yo, otro, datos["tamano"], datos["tablero"], not es_raton):
        orig = list(yo)
        if es_raton: datos["pos_raton"] = m
        else: datos["pos_gato"] = m
        p = minimax(datos, 3 if es_raton else 4, not es_raton)
        if (es_raton and p > mejor_p) or (not es_raton and p < mejor_p):
            mejor_p, mejor_m = p, m
        if es_raton: datos["pos_raton"] = orig # Limpieza
        else: datos["pos_gato"] = orig
            
    if es_raton:
        datos["pos_raton"] = mejor_m
        datos["memoria"].append(list(mejor_m))
        if len(datos["memoria"]) > 5: datos["memoria"].pop(0)
    else:
        datos["pos_gato"] = mejor_m

# --- MOTOR DE JUEGO ---

def dibujar(datos, t):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f" TURNO: {t} | MODO: ESPECTADOR ".center(datos["tamano"]*3, "═"))
    for fila in range(datos["tamano"]):
        fila = ""
        for colum in range(datos["tamano"]):
            p = [fila, colum]
            if p == datos["pos_gato"]: fila += "🐱 "
            elif p == datos["pos_raton"]: fila += "🐭 "
            elif p == datos["salida"]: fila += "🚪 "
            else:
                # Accedemos directamente al valor de la matriz para dibujar suelo o pared
                fila += datos["tablero"][fila][colum] + " " 
        print(fila)

def jugar():
    juego = generar_juego(tamano=10) # Tamaño fijo para evitar inputs
    historial = {}
    
    for t in range(1, 81):
        estado = (tuple(juego["pos_gato"]), tuple(juego["pos_raton"]))
        historial[estado] = historial.get(estado, 0) + 1
        if historial[estado] >= 5:
            dibujar(juego, t); print("\n🤝 EMPATE: Bucle detectado."); return

        dibujar(juego, t)
        mover_ia(juego, True) # Ratón
        if juego["pos_raton"] == juego["salida"]:
            dibujar(juego, t); print("\n🏁 VICTORIA: El ratón escapó."); return
            
        dibujar(juego, t)
        time.sleep(0.3)
        mover_ia(juego, False) # Gato
        if juego["pos_gato"] == juego["pos_raton"]:
            dibujar(juego, t); print("\n⚔️ DERROTA: El gato atrapó al ratón."); return

if __name__ == "__main__":
    jugar()