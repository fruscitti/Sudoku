import requests
import time

server = 'https://try.synthetic-minds.com/'
get_api = 'demo/sudoku/v0.1/getpuzzle'
post_api = 'demo/sudoku/v0.1/submit'

p = None
o = None



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


def remove_row(p, j, k, ops):
    r = list(p[j])
    r[k] = '.'
    return ops.difference(set(r))

def remove_col(p, j, k, ops):
    c = [x[k] for x in p]
    c[j] = '.'
    return ops.difference(set(c))

def options_for(p, j, k):
    ops = set([c for c in '123456789'])
    ops = remove_grid(p, j, k, ops)
    ops = remove_row(p, j, k, ops)
    ops = remove_col(p, j, k, ops)
    return ops


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

def next(j,k):
    k = k + 1
    if (k >= 9):
        k = 0
        j = j + 1
    return j, k

def can_add(p, j, k, v):
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


def pprint(p):
    for j in range(9):
        for k in range(9):
            print(p[j][k], end='', flush=True)
            print(' ', end='', flush=True)
        print()

r = requests.get(server + get_api)
d = r.json()
po = d['puzzle']
print(po)

# po = '.39.2......5....2.276..1..47.4.83...............19.2.73..6..752.5....6......7.18.'
p = [list(po)[i:i + 9] for i in range(0, len(po), 9)]
oo = [set() for x in range(9 * 9)]
o = [oo[i:i + 9] for i in range(0, len(oo), 9)]

pprint(p)
setup(p, o)
print(solve(p, o, 0, 0))
pprint(p)

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
