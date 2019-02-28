# Python/Sudoku for fun

Vez pasada encontré un site que tiene un Sudoku para resolver, 
https://synthetic-minds.com/pages/try.html
Basicamente muestra un sudoku y luego de resolverlo hay que ingresar la diagonal y da el veredicto.
Debajo hablaba de una api para automatizarlo y resolverlo con una máquina. Resultó interesante.
Estoy aprendiendo python asi que para probar, luego de ver un poco el código, el problema lo obtiene con una interfase REST:
https://try.synthetic-minds.com/demo/sudoku/v0.1/getpuzzle
y el resultado es de la siguiente forma:
```json
{
"puzzle":".1..9.7...4...8.........6.4..2.1..564...7...836..8.2..2.8.........3...9...5.6..4.",
"status":"ok"}
```

Para obtenerlo en python, usando requests es muy sencillo:

```python
import requests
server = 'https://try.synthetic-minds.com/'
get_api = 'demo/sudoku/v0.1/getpuzzle'

r = requests.get(server + get_api)
d = r.json()
po = d['puzzle']
```
So far, so good, ahora po es:

```python
".1..9.7...4...8.........6.4..2.1..564...7...836..8.2..2.8.........3...9...5.6..4."
```

Ok, para resolver el Sudoku hay muchas formas, yo soy principiante en python, pero va la mia:

```python
# transformo en una lista de listas para poder hacer p[0][3], para acceder a la 4 columna de la fila 0 (base 0)
p = [list(po)[i:i + 9] for i in range(0, len(po), 9)]

# idem para guardar luego que opciones o posibilidades tiene cada casilla.
oo = [set() for x in range(9 * 9)]
o = [oo[i:i + 9] for i in range(0, len(oo), 9)]
```
**Aclaración** **j** = fila, **k** = columna (o **r** y **c**)

Luego, para cada celda sin valor, necesito una lista de opciones con las que se puede llenar, que satisfagan las condiciones del juego:

```python
def options_for(p, j, k):
    ops = set([c for c in '123456789'])
    ops = remove_grid(p, j, k, ops)
    ops = remove_row(p, j, k, ops)
    ops = remove_col(p, j, k, ops)
    return ops
```
Esto es sencillo, comienzo con todas las posibilidades y saco las que ya están asignadas a nivel celda o grid (de 3x3), fila y columna.

**Sacar de celda**
```python
def remove_grid(p, j, k, ops):
    gtr = (j // 3) * 3
    gtc = (k // 3) * 3
    ops2 = set(ops)
    for r in range(gtr, gtr + 3):
        for c in range(gtc, gtc + 3):
            if r == j and k == c:
                continue
            if p[r][c] != '.':
                ops2.discard(p[r][c])
    return ops2
```
**Sacar de fila**
```python
def remove_row(p, j, k, ops):
    r = list(p[j])
    r[k] = '.'
    return ops.difference(set(r))
```

**Sacar de columna**
```python
def remove_col(p, j, k, ops):
    c = [x[k] for x in p]
    c[j] = '.'
    return ops.difference(set(c))
```

Ok, luego el proceso en si, en dos etapas
**Setup** calculo para cada celda que no tiene valor los valores posibles y los guardo en la grilla de opciones **o**. Si hay una sola opción, registro dicha opción en la grilla directamente.

```python
def setup(p, o):
    for j in range(9):
        for k in range(9):
            if p[j][k] != '.':
                continue
            options = options_for(p, j, k)
            if len(options) == 1:
                o[j][k] = options.pop()
            else:
                o[j][k].update(options)
```

Luego, la resolución en sí. En este caso usamos lo más sencillo que es backtracking con recursión. Hay muchas otras formas, algunas más eficientes. Por ejemplo es lógico primero tomar las celdas con menos posibilidades para achicar la cantidad de pruebas que se hacen. Pero en este caso hacemos de izquierda a derecha, fila por fila.

```python
# Auxiliar para ir incrementando los índices
def next(j,k):
    k = k + 1
    if (k >= 9):
        k = 0
        j = j + 1
    return j, k

def can_add(p, j, k, v):
    return v in options_for(p, j, k)

def can_add(p, j, k, v):
    # Auxiliar para ver si un valor es posible para na celda 
    return v in options_for(p, j, k)
    
def solve(p, o, j, k):
    if j >= 9:
        return True

    if p[j][k] != '.':
        nj, nk = next(j,k)
        return solve(p, o, nj, nk)

    for op in o[j][k]:
        if can_add(p, j, k, op):
            p[j][k] = op
            nj, nk = next(j, k)
            if solve(p, o, nj, nk):
                return True
    p[j][k] = '.'
    return False
```
Casi estámos.

Para cerrar, llamamos:

```python
setup(p, o)
res = print(solve(p, o, 0, 0))
```

Envio la respuesta, inspeccionando la pagina saqué el formato de json que espera:

```python
    diag = ''
    for j in range(9):
        diag += p[j][j]

    data = {
        'puzzle': po,
        'email': 'fruscitti@xxxxx.com',
        'answer': diag
    }

    r = requests.post(url=server+post_api, json = data)
    print(r.text)
```

Thats it.
