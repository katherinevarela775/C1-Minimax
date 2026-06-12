# Proyecto: El Laberinto del Gato y el Ratón (Minimax IA) 🐭🐱

1. Introducción y Reto

Este proyecto nació como un desafío para aplicar el algoritmo **Minimax** en un entorno de persecución y simulación interactiva. 
La idea principal era crear un ecosistema en el que un gato y un ratón no solo se movieran por un laberinto, sino que "pensaran" estratégicamente sus jugadas futuras para ganar la partida, permitiendo además la intervención directa del jugador.

2. Estructura del Repositorio (Dos Versiones)

Para demostrar la evolución del desarrollo y el dominio de diferentes paradigmas de programación, el proyecto se divide en dos arquitecturas independientes:

*   **📂 `version_def/` (Programación Estructurada):** La base del proyecto. Todo el control se realiza mediante funciones interconectadas que comparten un diccionario de estado global. Es ideal para entender la lógica pura del algoritmo de forma directa en la modalidad IA vs IA.
*   **📂 `version_poo/` (Programación Orientada a Objetos + Videojuego Multimodo):** Una reestructuración modular completa. Toda la lógica se encapsula de forma elegante dentro de la clase `Laberinto`. Esta versión introduce mecánicas avanzadas, mayor robustez y jugabilidad interactiva para el usuario.

3. Componentes de la IA y el Mapa

Ambas versiones comparten el mismo núcleo algorítmico de toma de decisiones:

- **El Mapa y BFS:** Implementa un generador aleatorio de paredes. Para garantizar que el ratón nunca quede encerrado, un algoritmo de búsqueda **BFS** verifica que siempre exista al menos un camino libre hacia la salida antes de iniciar el juego.
- **El Cerebro (Minimax):** Es el corazón estratégico. Mediante simulación por *Backtracking*, explora las ramas de un árbol de decisiones hacia el futuro (con profundidad 3 para el ratón y 4 para el gato). El ratón intenta maximizar su seguridad, mientras que el gato intenta minimizar la distancia para atraparlo.
- **La Heurística (Manhattan):** Utiliza la distancia de Manhattan para calcular los pesos de penalización y recompensa en las casillas, guiando a la IA cuando la profundidad del árbol llega a su fin.

4. Nuevas Mecánicas en Versión POO

En la versión orientada a objetos se introdujeron dinámicas avanzadas para enriquecer la jugabilidad:
- **Incentivo de exploración para el ratón (Sistema de Quesos 🧀):** Se esparcen 3 quesos aleatorios en el tablero. La distancia Manhattan del ratón añade un vector de atracción hacia el queso más cercano. Esto lo obliga a moverse y trazar rutas dinámicas en lugar de correr directo a la puerta, evitando que el gato intercepte su camino fácilmente. El gato ignora los quesos y se enfoca puramente en cazar de forma activa.
- **Tres Modos de Juego Seleccionables:** El usuario cuenta con un menú interactivo al iniciar para elegir si desea **Jugar como Ratón**, **Jugar como Gato** o actuar simplemente como **Espectador** (IA vs IA).
- **Sistema de Control Manual (`W/A/S/D`):** Implementa un capturador de teclado que valida en tiempo real si el movimiento ingresado por el usuario es legal dentro del mapa físico (evitando colisiones con paredes o salidas del tablero).

5. Extras y Control de Errores

- **Gráficos Adaptables en Consola:** Uso de emojis interactivos con limpieza automática de pantalla (`cls`/`clear`). El marco y las dimensiones del marcador superior se ajustan de manera automática dependiendo del tamaño de tablero seleccionado por el usuario.
- **Memoria de Pisadas:** Para evitar que el ratón se quede atascado en bucles infinitos de vaivén, se implementó una memoria a corto plazo que registra sus últimos 5 pasos y penaliza fuertemente el regreso a zonas ya visitadas.
- **Prevención de Cuelgues:** El menú de configuración inicial valida mediante seguridad tipográfica (`isdigit()`) el tamaño del tablero introducido. Si el usuario ingresa un dato inválido o texto, el motor aplica un tamaño estándar de 10x10 por seguridad.
- **Finales Técnicos:** El juego concluye por victoria de cualquiera de las partes, por un límite estricto de **80 turnos**, o de forma prematura declarando un **Empate Técnico** si se registra un bucle repetitivo de posiciones en el historial global del tablero.

6. Reglas de uso

Para ejecutar cualquiera de las versiones solo necesitas Python 3 instalado:

1. Entra a la carpeta de la versión que quieras probar:
   ```bash
   cd version_def
   # o bien:
   cd version_poo
   ```
2. Ejecuta el script principal:
   ```bash
   python minimax.py          # (en version_def)
   python minimaxpoo.py     # (en version_poo)
   ```
