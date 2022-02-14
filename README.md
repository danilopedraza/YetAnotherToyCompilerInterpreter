# YetAnotherToyCompilerInterpreter

Un parser básico para gramáticas LL(1).

## Uso

Para correr el programa de ejemplo:

* Descargar el repositorio
* En el directorio del repositorio, descargar el requerimiento con ```pip install -r requirements.txt```
* Ejecutar con ```python3 main.py```

Para procesar una cadena, basta construir  un objeto ```Parser(Lexer(tokens), grammar)``` (disponible en ```myparser.py```), con dos entradas:

* Un objeto ```Lexer``` con un parámetro ```tokens```, que es una lista de parejas de la forma ```(nombre, regex)```. El buffer de tokens para el parser se obtendrá en función de este parámetro,
etiquetando tokens de acuerdo a las expresiones regulares con las que haya compatibilidad.
Siempre se aceptará el prefijo más largo posible, y si hay dos expresiones que aceptan una cadena, se tomará la primera en la lista.
No se pueden ignorar tokens, solo lidiar con ellos en la gramática.

* ```grammar```, una lista de parejas de la forma ```(noTerminal, regla)```. Cada pareja representa una regla de producción para una gramática LL(1).
Se asume que en la primera regla de la lista, a la izquierda, está el simbolo inicial. La parte de la derecha es una lista de simbolos de la gramática,
que deben ser etiquetas definidas en la lista de tokens, o simbolos a la izquierda de alguna regla de la gramática, o la cadena vacía: ```""```.

Ya con el parser construido, solo hay que usar el método ```parse(string)``` para obtener la raíz del árbol de sintaxis: un objeto ```ASTNode``` con
atributos ```type```, ```children``` y ```literal```. Todos los nodos tienen el atributo ```type```, los no terminales tienen
nodos hijos en ```children```, que es una lista, y los terminales tienen una cadena en el atributo ```literal```. Los nodos correspondientes a la cadena vacía tienen el tipo ```"EPSILON"```.


## Sobre la implementación

* Para el análisis léxico se simula un autómata no determinista obtenido de las expresiones regulares. El procesamiento de las expresiones  está en ```re_to_nfa.py```.

* Las expresiones regulares solo usan el operador de unión ```|```, estrella de Kleene ```*``` y los paréntesis ```()```. Para detectar estos símbolos con una expresión regular, hay que poner ```\``` al principio de cada carácter especial.

* Para el análisis sintáctico se emplea una estrategia top-down, usando una tabla de parsing. No hay manejo de errores como tal: Si se llega a un estado sin reglas aplicables el procedimiento de parsing es abortado.

* Cuando la cadena de entrada se consuma por completo, el lexer retornará tokens de tipo ```"EOF"```. Si una cadena o símbolo no es aceptado por ninguna expresión, será pasado con un token de tipo ```"ILLEGAL"```.

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

![](https://i.imgur.com/dg9HMgi.png)

También se puede utilizar la función ```displayTree``` para ver el árbol. ```displayTree``` usa la biblioteca ```graphViz```, el único requerimiento en ```requirements.txt```. Muestra un árbol así:

![](https://i.imgur.com/3309rVD.png)

