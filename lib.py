

import heapq
import geral as g
num_lins = 0
num_cols = 0

def read_file(filename):

    global num_cols, num_lins
    lines = None    
    start = (0,0)
    end = (0,0)

    with open(filename) as file:
        lines = file.readlines()

        j = 0
        for line in lines:
            lines[j] = line.strip('\n')
            
            if line.find('U') > -1:
                end = (line.find('U'), j)
            if line.find('1') > -1:
                start = (line.find('1'), j)
            j += 1

    num_cols = len(lines[0])
    num_lins = len(lines)

    return lines, start, end

def printMap(lines, actual):

    print()
    print()
    print()
            
    print("\033[%d;%dH" % (1, 1)) # y, x

    for j in range(num_lins):
        for i in range(num_cols):
            if actual[0] == i and actual[1] == j:
                print('█', end='')
            else:
                print(lines[j][i], end='')

        print()

def get_char_from_map(mapa, coord):
    return mapa[coord[1]][coord[0]]

def get_value(c):
    return 1

def add_valid_pos(nb, mapa, coord):        
    nb.append([coord, custo(mapa, coord)])
def get_neighborhood(mapa, coord):
    
    nb = []
    if coord[0] == 0: # coord[0] = x (cols)
        add_valid_pos(nb, mapa, (coord[0] + 1, coord[1]))
    
    elif coord[0] == num_cols - 1:
        add_valid_pos(nb, mapa, (coord[0] - 1, coord[1]))
    
    else:    
        add_valid_pos(nb, mapa, (coord[0] + 1, coord[1]))
        add_valid_pos(nb, mapa, (coord[0] - 1, coord[1]))
    

    if coord[1] == 0:  # coord[1] = y (linhas)
        add_valid_pos(nb, mapa, (coord[0], coord[1] + 1))
    
    elif coord[1] == num_lins - 1:
        add_valid_pos(nb, mapa, (coord[0], coord[1] - 1))
    
    else:    
        add_valid_pos(nb, mapa, (coord[0], coord[1] + 1))
        add_valid_pos(nb, mapa, (coord[0], coord[1] - 1))
    
    return nb


def buscar_ginasios(mapa, ginasios):
    coordenadas_ginasios = []
    
    # Cria uma lista apenas com os símbolos dos ginásios (ex: ['2', '3', '4', ..., 'B', ...])
    simbolos_ginasios = [g[0] for g in ginasios]
    
    for y, linha in enumerate(mapa):
        for x, celula in enumerate(linha):
            if celula in simbolos_ginasios: # Agora compara string com string perfeitamente!
                coordenadas_ginasios.append((x, y))

    return coordenadas_ginasios

def custo(mapa, cord):

    tipo_terreno = mapa[cord[1]][cord[0]]
    
    # Se o terreno estiver no dicionário de custos, retorna o valor numérico
    if tipo_terreno in g.custo:
        return g.custo[tipo_terreno]
    # Se for um ginásio, o início ('1') ou o fim ('U'), custa 1 por padrão para caminhar por cima
    else:
        return 1


def dijkstra(mapa, origem):
    """Menor custo da origem até todas as células (custo = soma do custo() das células em que se ENTRA)."""
    dist = {origem: 0}
    prev = {}
    fila = [(0, origem)]
    while fila:
        d, atual = heapq.heappop(fila)
        if d > dist[atual]:
            continue
        for vizinho, custo_vizinho in get_neighborhood(mapa, atual):
            nd = d + custo_vizinho
            if nd < dist.get(vizinho, float("inf")):
                dist[vizinho] = nd
                prev[vizinho] = atual
                heapq.heappush(fila, (nd, vizinho))
    return dist, prev


def matriz_distancias(mapa, pontos):
    """D[a][b] = menor custo de pontos[a] até pontos[b]; prevs[a] serve para reconstruir o caminho."""
    D, prevs = [], []
    for origem in pontos:
        dist, prev = dijkstra(mapa, origem)
        D.append([dist[destino] for destino in pontos])
        prevs.append(prev)
    return D, prevs


def caminho_dijkstra(prev, a, b):
    caminho = [b]
    while caminho[-1] != a:
        caminho.append(prev[caminho[-1]])
    caminho.reverse()
    return caminho