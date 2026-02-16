import random, os, time # random se encarga de todo lo que tenga que ver con el azar, os permite la comucacion con nuestro sist. operativo, y time sirve para manejar el tiempo y las pausas

# - Logica del Mapa y Caminos - 

def movimientos_posibles(pos, oponente, tamano, tablero, es_gato=True): # pos: posicion actual, oponente: posic. del oponente, es_gato: dato booleano para evitar que el raton pise al gato pero si viceversa
    """Define los movimientos legales en el tablero consultando la matriz (tablero)."""
    opciones = []
    for df, dc in [(-1,0), (1,0), (0,-1), (0,1)]: # Para filas y columnas en las direcciones que puede usar
        nueva_pos = [pos[0]+df, pos[1]+dc] # Calcula la nueva posicion sumando el mov. a la posicion actual
        if 0 <= nueva_pos[0] < tamano and 0 <= nueva_pos[1] < tamano and tablero[nueva_pos[0]][nueva_pos[1]] != "⬛":  # Filtro que revisa que no se salga en x ni en y, y que no choca con un muro en la matriz
            if not es_gato and nueva_pos == oponente: continue # Si el que mueve es el raton y la posicion es la del gato, con continue ignoramos la opcion
            opciones.append(nueva_pos) # Si paso todos los filtros se agrega a la lista de opciones
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
            filas, colum = random.randint(0, tamano-1), random.randint(0, tamano-1) # Genera una coord. al azar en el rango de 0 y el tamaño del mapa
            if [filas, colum] not in seguras: 
                tablero[filas][colum] = "⬛" # Si la coord. esta libre, le ponemos una pared :) (se marca en la matriz)
        
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

def minimax(datos, prof, es_max): # Esta funcion es recursiva se llama a si misma para crear el arbol de posibilidades
    """Simulador de estados futuros."""
    if datos["pos_gato"] == datos["pos_raton"]: return -20000 # Si el gato gana devuelve un valor muy bajo
    elif datos["pos_raton"] == datos["salida"]: return 20000 # Si el raton escapa devuelve uno muy alto
    elif prof == 0: return puntuar(datos, es_max) # Cuando la prof. llega a 0, deja de imagina y utiliza la func. puntuar para evaluar que tan buen es la funcion actual

    mejor = float('-inf') if es_max else float('inf') # En esta variable dependiendo de quen sea se empieza con cierto numero, para max (-inf) y para min (inf)
    yo = datos["pos_raton"] if es_max else datos["pos_gato"] # En esta y la sgte. linea identificamos quien es eljugador que esta "pensando"
    otro = datos["pos_gato"] if es_max else datos["pos_raton"]
    
    for m in movimientos_posibles(yo, otro, datos["tamano"], datos["tablero"], not es_max): # Iteramos cada mov. legal
        orig = list(yo) #Backtracking Punto 1: Guardamos la posición original en orig para poder "regresar en el tiempo" después de simular.
        if es_max: datos["pos_raton"] = m # Cambiamos la pos. en el diccionario para ver que pasaria si nos movemos a la casilla que estamos iterando en ese momento
        else: datos["pos_gato"] = m # ///
        val = minimax(datos, prof - 1, not es_max) # Llamamos nuevamente a la funcion minimax pero le restamos 1 a la profundidad y cambiamos el turno (el -1 es para que no se quede pensando para siempre)
        mejor = max(mejor, val) if es_max else min(mejor, val) # Actualizamos nuestra mejor opcion, si es raton busca el max y si es el gato busca el min, comapara el puntaje que tenia en mejor con el que consiguio en val y se queda con el que mas le convenga
        if es_max: datos["pos_raton"] = orig # Backtracking Punto 2: Devolvemos la pieza a su lugar original (orig) para que la siguiente iteración del for empiece desde el lugar correcto.
        else: datos["pos_gato"] = orig
    return mejor # Devolvemos el mejor puntaje encontrado a cada rama

def mover_ia(datos, es_raton): # Es la funcion que aplica toda la logica al juego
    """Aplica la mejor decisión del Minimax al mundo real."""
    yo = datos["pos_raton"] if es_raton else datos["pos_gato"] # Identificamos quién está jugando en este turno. Si es_raton es True, entonces yo toma la posición del ratón.
    otro = datos["pos_gato"] if es_raton else datos["pos_raton"]
    mejor_m, mejor_p = yo, (float('-inf') if es_raton else float('inf')) # Inicializamos la variables para recordar la decision; mejor_m: guardara la mejor coord. encontrada o la pos. actual en todo caso; mejor_p: Es el récord de puntaje. Si eres el ratón, empiezas con (-inf) para superar cualquier cosa; si eres el gato, con (inf).
    
    for m in movimientos_posibles(yo, otro, datos["tamano"], datos["tablero"], not es_raton):# Bucle que analiza todas la casillas a las que nos podemos mover
        orig = list(yo) #Backtracking, guardamos la pos. actual en orig
        if es_raton: datos["pos_raton"] = m # Ejecutamos el mov imaginario en el dicc. datos
        else: datos["pos_gato"] = m
        p = minimax(datos, 3 if es_raton else 4, not es_raton) # Aqui llamamos a la funcion minimax con la prof. de 3 para el raton y de 4 para el gato
        if (es_raton and p > mejor_p) or (not es_raton and p < mejor_p): # Aqui comparamos el resultado de la sim. (p) es mejor que el record actual (mejor_p) y guardamos ese mov (m)
            mejor_p, mejor_m = p, m #  //
        if es_raton: datos["pos_raton"] = orig # Aqui devolvemos la pieza a su pos. original antes de la sim.
        else: datos["pos_gato"] = orig
            
    if es_raton: 
        datos["pos_raton"] = mejor_m # Una vez termino el bucle tomamos las decis. final y movemos la pieza a mejor_m
        datos["memoria"].append(list(mejor_m)) # Se guarda el mov. en la lista de memoria 
        if len(datos["memoria"]) > 5: datos["memoria"].pop(0) # Si la memoria tiene mas de 5 elementos, eliminamos el mas antiguo
    else:
        datos["pos_gato"] = mejor_m # Una vez termino el bucle tomamos las decis. final y movemos la pieza a mejor_m

# --- MOTOR DE JUEGO ---

def dibujar(datos, turn): # Se encarga de limpiar la pantalla y redibujar el tablero en cada turno
    os.system('cls' if os.name == 'nt' else 'clear') # Envia un comando al sist. operativo, para borrar el texto anterior
    # f"..." es una f-string para que las llaves {turn} funcionen. .center() centra el texto.
    print(f" TURNO: {turn} | MODO: ESPECTADOR ".center(datos["tamano"]*3, "═")) # .center(...): Es un método de Python que centra el texto y datos["tamano"]*3: Calcula el ancho del tablero para que la línea decorativa ═ mida exactamente lo mismo que el mapa.
    
    for f in range(datos["tamano"]): # Inicia un bucle para recorrer desde 0 hasta el lim. del mapa (fila)
        texto_fila = "" # Variable para ir armando el dibujo de la hilera actual
        for c in range(datos["tamano"]): # Inicia un bucle para recorrer desde 0 hasta el lim. del mapa (colum)
            p = [f, c] # Lista que representa la coordenada actual a revisar
            if p == datos["pos_gato"]: texto_fila += "🐱 "
            elif p == datos["pos_raton"]: texto_fila += "🐭 " # Segun la pos. de la coord. del gato, raton y la salida, se imprime la figura correspondiente
            elif p == datos["salida"]: texto_fila += "🚪 "
            else:
                texto_fila += datos["tablero"][f][c] + " " # Si no hay ninguna de los elementos anteriores, entoces se dibuja lo que det. en generar_juego ya sea piso o una pared
        print(texto_fila) # Imprime la hilera completa

def jugar(): # Esta funcion controla el flujo del tiempo, alterna los turnos y decide cuando termina el juego, implementa el game loop
    juego = generar_juego(tamano=10) # Llama a la funcion generar_juego para crear el diccionario con el tablero inicial, las pos. y las paredes
    historial = {} # Un dicc. vacio para detectar si el gato y el raton se quedan trabados en el mismo lugar mucho rato
    
    for turn in range(1, 61): # El juego tiene un limite de 61 turnos para evitar que corra eternamente
        estado = (tuple(juego["pos_gato"]), tuple(juego["pos_raton"])) # Hcemos un registro con tuplas con las pos. del gato y el raton
        historial[estado] = historial.get(estado, 0) + 1 # Registramos cuantas veces  se repite la pos. que registramos en las tupla
        if historial[estado] >= 5: # Si la misma posicion se repite 5 veces, se declara un empate tecnico
            dibujar(juego, turn); print("\n🤝 EMPATE: Bucle detectado."); return

        dibujar(juego, turn) # Se dibuja el tablero
        mover_ia(juego, True) # Se le pide a la IA que mueva al raton 
        if juego["pos_raton"] == juego["salida"]: # Verificamos si el raton no se encuentra en la salida
            dibujar(juego, turn); print("\n🏁 VICTORIA: El ratón escapó."); return # Si es asi, se imprime el mensaje de victoria, y termina la funcion con un return
            
        dibujar(juego, turn) # Dibujamos el mov. del raton
        time.sleep(0.3) # Hacemos una pausa de 0.3 s
        mover_ia(juego, False) # Se mueve el gato
        if juego["pos_gato"] == juego["pos_raton"]: # Verificamos si ambos estan en la misma pos. o sea que el gato gano
            dibujar(juego, turn); print("\n⚔️ DERROTA: El gato atrapó al ratón."); return

if __name__ == "__main__": # Es una cond. de seguridad, evita que el juego se empice a ejecutar solo, en caso de usar alguna de las func. de este codigo en un proyecto diferente
    jugar()