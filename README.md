# YetAnotherToyCompilerInterpreter

Un parser básico para gramáticas LL(1).

## Uso

Para procesar una cadena, basta construir  un objeto ```Parser(tokens, grammar)``` (disponible en ```myparser.py```), con dos entradas:

* ```tokens```, una lista de parejas de la forma ```(nombre, regex)```. El buffer de tokens para el parser se obtendrá en función de este parámetro,
etiquetando tokens de acuerdo a las expresiones regulares con las que haya compatibilidad.
Siempre se aceptará el prefijo más largo posible, y si hay dos expresiones que aceptan una cadena, se tomará la primera en la lista.
No se pueden ignorar tokens, solo lidiar con ellos en la gramática.
Cuando la cadena de entrada se consuma por completo, se retornarán objetos ```Token``` de tipo ```"EOF"```.

* ```grammar```, una lista de parejas de la forma ```(noTerminal, regla)```. Cada pareja representa una regla de producción para una gramática LL(1).
Se asume que en la primera regla de la lista, a la izquierda, está el simbolo inicial. La parte de la derecha es una lista de simbolos de la gramática,
que deben ser etiquetas definidas en la lista de tokens, o simbolos a la izquierda de alguna regla de la gramática, o la cadena vacía: ```""```.

Ya con el parser construido, solo hay que usar el método ```parse(string)``` para obtener la raíz del árbol de sintaxis: un objeto ```ASTNode``` con
atributos ```type```, ```children``` y ```literal```. Todos los nodos tienen el atributo ```type```, los no terminales tienen
nodos hijos en ```children```, que es una lista, y los terminales tienen una cadena en el atributo ```literal```.


## Sobre la implementación

* Para el análisis léxico se simula un autómata no determinista obtenido de las expresiones regulares.

* Las expresiones regulares solo usan el operador de unión ```|```, estrella de Kleene ```*``` y los paréntesis ```()```. Así, estos símbolos no se pueden usar como parte del lenguaje a diseñar.

* Para el análisis sintáctico se emplea una estrategia top-down, usando una tabla de parsing. No hay manejo de errores como tal: Si se llega a un estado sin reglas aplicables el procedimiento de parsing es abortado.

## Ejemplo
En ```main.py``` se crea un objeto ```Parser``` con los siguientes parámetros:

```py
tokens = [
    ("INT", "(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*"),
    ("PLUS","+"),
    ("MINUS", "-"),
    ("LPAREN", "["),
    ("RPAREN", "]")
]

grammar = [
    ("E", ["T","E2"]),
    ("E2", ["PLUS", "T","E2"]),
    ("E2", [""]),
    ("T", ["F", "T2"]),
    ("T2", ["MINUS", "F", "T2"]),
    ("T2", [""]),
    ("F", ["LPAREN", "E", "RPAREN"]),
    ("F", ["INT"])
]
```

Al procesar la cadena ```"5-2+7"``` se obtiene un árbol de sintaxis que es transformado por la función ```treeToTeX``` en una cadena procesable en LaTeX con el paquete qtree.
Al renderizar la cadena correspondiente al árbol de ejemplo, luce así:

![](https://i.imgur.com/wy0pd6R.png)
