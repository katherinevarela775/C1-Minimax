# Proyecto: El Laberinto del Gato y el Ratón (Minimax IA) 🐭🐱

1. Introducción y Reto

Este proyecto nació como un desafío para aplicar el algoritmo **Minimax** en un entorno de persecución y simulación interactiva. 
La idea principal era crear un ecosistema en el que un gato y un ratón no solo se movieran por un laberinto, sino que "pensaran" estratégicamente sus jugadas futuras para ganar la partida.

2. Estructura del Repositorio (Dos Versiones)

Para demostrar la evolución del desarrollo y el dominio de diferentes paradigmas de programación, el proyecto se divide en dos arquitecturas independientes:

*   **📂 `version_def/` (Programación Estructurada):** La base del proyecto. Todo el control se realiza mediante funciones interconectadas que comparten un diccionario de estado global. Es ideal para entender la lógica pura del algoritmo de forma directa.
*   **📂 `version_poo/` (Programación Orientada a Objetos + Mejoras):** Una reestructuración modular completa. Toda la lógica se encapsula en una clase independiente (`Laberinto`). Esta versión incluye mecánicas avanzadas y una IA más pulida.

3. Componentes de la IA y el Mapa

Ambas versiones comparten el mismo núcleo algorítmico de toma de decisiones:

- **El Mapa y BFS:** Implementa un generador aleatorio de paredes. Para garantizar que el ratón nunca quede encerrado, un algoritmo de búsqueda **BFS** verifica que siempre exista al menos un camino libre hacia la salida antes de iniciar el juego.
- **El Cerebro (Minimax):** Es el corazón estratégico. Mediante simulación por *Backtracking*, explora las ramas de un árbol de decisiones hacia el futuro. El ratón intenta maximizar su seguridad, mientras que el gato intenta minimizar la distancia para atraparlo.
- **La Heurística (Manhattan):** Utiliza la distancia de Manhattan para calcular los pesos de penalización y recompensa en las casillas, guiando a la IA cuando la profundidad del árbol llega a su fin.

4. Nueva Mecánica en Versión POO: El Sistema de Quesos 🧀

En la versión orientada a objetos se introdujo una dinámica para enriquecer la jugabilidad:
- **Incentivo de exploración para el ratón:** Se esparcen quesos de forma aleatoria en el tablero.
- **Modificación Heurística del Ratón:** La distancia Manhattan del ratón ahora no solo mide la cercanía del enemigo y la salida, sino que añade un vector de atracción hacia el queso más cercano. Esto lo obliga a moverse y trazar rutas dinámicas por el laberinto en lugar de correr en línea recta a la puerta, evitando que el gato intercepte su camino fácilmente. El gato, por su parte, ignora los quesos y se enfoca puramente en cazar de forma activa.

5. Extras y Control de Errores

- **Gráficos en Consola:** Uso de emojis interactivos con limpieza automática de pantalla (`cls`/`clear`) para ofrecer una simulación fluida en tiempo real de la modalidad **IA vs IA**.
- **Memoria de Pisadas:** Para evitar que el ratón se quede atascado yendo y viniendo entre dos casillas idénticas, se implementó una memoria a corto plazo que registra sus últimos 5 pasos y penaliza fuertemente los regresos a zonas ya visitadas.
- **El Gato Portero (Solucionado):** En las primeras pruebas, el gato descubrió matemáticamente que si se "campeaba" en la puerta de salida, ganaba siempre. Al activar al **ratón mediante el estímulo de los quesos**, el ratón busca rutas alternativas, forzando al gato a abandonar la puerta y convertirse en un cazador móvil.

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
