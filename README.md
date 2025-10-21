# Proyecto 2: Implementación del Algoritmo CYK

---

## Integrantes del equipo
22046 - Nelson Escalante

23384 - Eliazar Canastuj

---

## Objetivo del proyecto
Implementar el **algoritmo CYK (Cocke–Younger–Kasami)** para determinar si una **frase en inglés** pertenece a un lenguaje generado por una **gramática libre de contexto (CFG)**.  
Además, generar el **árbol sintáctico (parse tree)** de la oración y medir el **tiempo de ejecución** del análisis.

---

## Gramática utilizada
Ejemplo de gramática (ya integrada en el código):
```
S → NP VP
VP → VP PP | V NP | cooks | drinks | eats | cuts
PP → P NP
NP → Det N | he | she
V → cooks | drinks | eats | cuts
P → in | with
N → cat | dog | beer | cake | juice | meat | soup | fork | knife | oven | spoon
Det → a | the
```

---

## ⚙️ Requisitos
- Python **3.8 o superior**
- Biblioteca necesaria:
```bash
pip install matplotlib
```

---

## 🚀 Ejecución
Guarda el archivo principal como `cyk_parser.py`.

Ejecuta el programa:
```bash
python proy2.py
```

Ingresa una frase en inglés cuando se te solicite:
```
Ingrese una frase en inglés (por ejemplo: 'She eats a cake with a fork'):
```

El programa mostrará:
- Si la frase pertenece al lenguaje (✅ o ❌).
- El tiempo de ejecución.
- Un archivo PNG con el árbol sintáctico (por ejemplo `parse_tree_she_eats_a_cake_with_a_fork.png`).

---

## 🧠 Ejemplos
✅ Frases válidas:
```
She eats a cake
The cat drinks the beer
He cuts a cake with a knife
```
❌ Frases inválidas:
```
He eats with spoon
The beer drinks the cat
```

---

## 🕒 Salida esperada
```
Simplificando gramática...
Gramática simplificada correctamente ✅

✅ 'She eats a cake with a fork' pertenece al lenguaje (tiempo: 0.001523s)
🌳 Árbol sintáctico exportado en: parse_tree_she_eats_a_cake_with_a_fork.png
```
El archivo PNG generado muestra el árbol de derivación correspondiente.
