
# Proyecto: El Laberinto del Gato y el Ratón (Minimax) 🐭🐱

1. Introducción y Reto

Este proyecto nació como un desafío para aplicar el algoritmo **Minimax** en un entorno de persecución. 
La idea era crear un simulador donde un gato y un ratón no solo se movieran, sino que "pensaran" sus jugadas para ganar.

2. Arquitectura

- El sistema funciona sobre un tablero bidimensional  en Python.
 
- El Mapa: Implementé un generador aleatorio de paredes, pero para no dejar al ratón encerrado, usé un algoritmo de búsqueda BFS que verifica si siempre hay salida antes de empezar.


- El Cerebro (Minimax): Es el corazón del código. El ratón intenta maximizar su seguridad y el gato minimizar la distancia para atraparlo. Cada movimiento es una rama en un árbol de decisiones que el programa explora hacia el futuro.


- La Heurística: Para que el gato sea agresivo, usé la Distancia Manhattan. Le di pesos más altos a la cercanía del gato para que no se quede dando vueltas y realmente persiga al objetivo.

3. Extras y Bonus

Me tomé la libertad de añadir una cosa que pedía el desafío como bonus:

- Gráficos en Consola: Usé emojis para que el tablero sea fácil de leer sin necesidad de una interfaz compleja.



4. Bitácora de errores y anécdotas

Lo que funcionó: La lógica de turnos quedó muy sólida. Separar la "inteligencia" del movimiento físico ayudó mucho a organizar el código.


El desastre: Al principio, el ratón se quedaba en bucles infinitos yendo y viniendo entre dos casillas. Tuve que programarle una memoria a corto plazo para que penalice los lugares donde ya estuvo.
Mi momento "¡Jaja!": Fue ver al gato "campeando" la salida. Me di cuenta de que, matemáticamente, el gato descubrió que si se quedaba en la puerta, la distancia al ratón eventualmente se reduciría a cero cuando el ratón intentara escapar. Tuve que ajustar los pesos de la IA para que fuera un cazador activo y no un portero.

5. Reglas de uso

Para correr el código solo necesitas Python básico:

1. Ejecutas `python nombre_del_archivo.py`.
y ya
