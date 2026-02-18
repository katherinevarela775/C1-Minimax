 Challenge 1 - Minimax

Proyecto: El Laberinto del Gato y el Ratón (Minimax) 🐭🐱

Introducción y Reto:

 El desafío consistió en implementar un sistema de toma de decisiones autónomo utilizando el algoritmo Minimax, enfrentando a dos agentes con objetivos opuestos en un entorno dinámico y con obstáculos.

 Arquitectura del Sistema:
 El simulador está construido íntegramente en Python, priorizando la eficiencia algorítmica y la claridad estructural.

 El Mapa (Estructura de Matriz): 
 A diferencia de una lista de coordenadas, el mundo se representa como una matriz bidimensional (lista de listas). Esto permite una detección de colisiones optimizada en tiempo constante.

 Garantía de Solución (BFS): Antes de iniciar, el sistema utiliza un algoritmo Breadth-First Search (BFS) para asegurar que el laberinto generado aleatoriamente tenga un camino válido entre el ratón y la salida.

 El Cerebro (Minimax): Es el motor de IA. El ratón actúa como el Maximizador, buscando estados que aumenten su puntuación, mientras que el gato es el Minimizador, intentando reducir las opciones del ratón a cero.

 La Heurística (Manhattan): Para evaluar posiciones futuras sin recorrer el árbol hasta el infinito, implementé la Distancia Manhattan. Esta mide la proximidad entre agentes y objetivos ignorando diagonales, simulando un movimiento por celdas reales.


 Detalles Técnicos y "Bonus"

 Modo Espectador: El sistema permite observar en tiempo real cómo las dos IAs compiten, con un retraso programado (time.sleep) para apreciar el análisis de cada turno.

 Gráficos en Consola: Renderizado mediante emojis y limpieza de pantalla (os.system) para una experiencia visual limpia y minimalista directamente en la terminal.

 Detección de Bucles: Implementé un historial de estados que registra las posiciones de los agentes. Si el sistema detecta que se repite una configuración 5 veces, declara un empate técnico para evitar ciclos infinitos.

 Bitácora de Desarrollo y Aprendizajes
 Lo que funcionó: La transición de una lista de coordenadas a una matriz de datos fue un punto de inflexión. El código se volvió más legible y la lógica de dibujo mucho más intuitiva.

 El reto de la memoria: Un problema recurrente era el "titubeo" del ratón (moverse de A a B y volver a A). Se solucionó implementando una memoria a corto plazo que penaliza en la heurística las casillas visitadas recientemente.

 El Gato campero: En las primeras pruebas, el gato aprendió que la mejor estrategia era quedarse quieto frente a la salida (campear). Tuve que ajustar los pesos de la distancia gato-ratón en la función de puntuación para obligar al gato a ser un cazador activo.


Reglas de Uso

Asegúrate de tener instalado Python 3.x.
Descarga el archivo minimax.py.
Ejecuta el comando: Bash python minimax.py
Observa cómo la IA resuelve el laberinto en un mapa de 10x10.

 Este proyecto solo utiliza la Librería Estándar de Python.
 No se requieren dependencias externas.
