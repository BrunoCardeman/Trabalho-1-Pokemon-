"""
INF1771 - Trabalho 1 - Tarefa 1: escolha dos Pokémon em cada ginásio.
  - Simulated Annealing (busca local) para achar uma boa escolha.
  - A* (com o TreeNode de geral.py) para provar qual é o ótimo global.
Requer geral.py na mesma pasta.
"""
import heapq
import math
import random
import statistics
from itertools import combinations

import geral
from geral import treeNode

# ------------------------- CONFIGURAÇÃO (lida do geral.py) -------------------------
# geral.pokemons = [[energia, poder], ...] na ordem abaixo (não guarda os nomes)
NOMES = ["Pikachu", "Bulbassauro", "Rattata", "Caterpie", "Weedle"]
PODER = {}
for i in range(len(NOMES)):
    nome = NOMES[i]                 # ex.: i = 0  ->  "Pikachu"
    poder = geral.pokemons[i][1]    # ex.: i = 0  ->  [6, 1.5][1]  ->  1.5
    PODER[nome] = poder
ENERGIA = geral.pokemons[0][0]            # todos começam com a mesma energia (6)
DIFICULDADE = dict(geral.ginasios)        # {"2": 35, "3": 40, ...}

GINASIOS = list(DIFICULDADE)
POKEMONS = list(PODER)


# ------------------------- O PROBLEMA -------------------------
# Solução = lista com 24 conjuntos: sol[i] = Pokémon que lutam no ginásio i.

def tempo(ginasio, equipe):
    soma_poder = 0
    for p in equipe:
        soma_poder = soma_poder + PODER[p]
    return DIFICULDADE[ginasio] / soma_poder


def custo(sol):
    total = 0
    for i in range(len(GINASIOS)):
        g = GINASIOS[i]          # ex.: "2"
        equipe = sol[i]          # ex.: {"Weedle"}
        total = total + tempo(g, equipe)
    return total


def energia_final(sol):
    resultado = {}
    for p in POKEMONS:
        batalhas = 0
        for equipe in sol:
            if p in equipe:
                batalhas = batalhas + 1
        resultado[p] = ENERGIA - batalhas
    return resultado


def valida(sol):
    """As restrições são, todo ginásio tem alguém lutando, ninguém fica com energia
    negativa e pelo menos um Pokémon chega com energia maior ou igual a 1."""
    e = energia_final(sol).values()
    return all(sol) and min(e) >= 0 and max(e) >= 1


# ------------------------- SOLUÇÃO INICIAL E VIZINHANÇA -------------------------

def solucao_inicial():
    sol = []
    for i in range(len(GINASIOS)):                # um ginásio de cada vez (24 ao todo)
        posicao = i % len(POKEMONS)               # 0, 1, 2, 3, 4, 0, 1, 2, ...
        pokemon = POKEMONS[posicao]               # Pikachu, Bulbassauro, ..., Weedle, Pikachu, ...
        sol.append([pokemon])                     # a equipe desse ginásio tem só esse Pokémon
    random.shuffle(sol)                           # embaralha a ordem das equipes
    return sol

def vizinho(sol):
    """Gera vizinhos aleatórios até achar um VÁLIDO (os inválidos são descartados)."""
    while True:
        nova = []
        for equipe in sol:
            nova.append(list(equipe))        # copia cada equipe (lista nova)
        a, b = random.sample(range(len(nova)), 2)
        p, q = random.sample(POKEMONS, 2)
        op = random.choice([0, 1, 2])
        if op == 0:                          # coloca ou tira o Pokémon p do ginásio a
            if p in nova[a]:
                nova[a].remove(p)
            else:
                nova[a].append(p)
        elif op == 1:                        # troca as equipes inteiras dos ginásios a e b
            nova[a], nova[b] = nova[b], nova[a]
        elif p in nova[a] and q in nova[b] and q not in nova[a] and p not in nova[b]:
            nova[a].remove(p)                # p sai do ginásio a...
            nova[a].append(q)                # ...e q entra no lugar
            nova[b].remove(q)                # q sai do ginásio b...
            nova[b].append(p)                # ...e p entra no lugar
        if nova != sol and valida(nova):
            return nova


# ------------------------- SIMULATED ANNEALING -------------------------

def simulated_annealing(T=50.0, alpha=0.9999, T_min=0.001):
    atual = solucao_inicial()
    c_atual = custo(atual)
    melhor, c_melhor = atual, c_atual
    while T > T_min:
        cand = vizinho(atual)
        delta = custo(cand) - c_atual
        # melhora: aceita sempre; piora: aceita com probabilidade e^(-delta/T)
        if delta < 0 or random.random() < math.exp(-delta / T):
            atual, c_atual = cand, c_atual + delta
            if c_atual < c_melhor:
                melhor, c_melhor = atual, c_atual
        T *= alpha                       # resfriamento
    return melhor, c_melhor


# ------------------------- A* (ótimo global) -------------------------
# Estado: (próximo ginásio, energia de cada Pokémon)
# Ação:   escolher uma equipe entre os Pokémon acordados
# g(x):   tempo de batalha acumulado
# h(x):   soma das dificuldades restantes / poder de TODOS os acordados.
#         Nenhuma equipe é mais forte que "todos juntos", então h nunca
#         superestima => h é admissível => o A* acha o ótimo.
       # o "set(c)" do começo da linha

equipes = [[]]                        # começa só com a equipe vazia
for p in POKEMONS:
    novas = []
    for eq in equipes:
        novas.append(eq)              # versão SEM o Pokémon p
        novas.append(eq + [p])        # versão COM o Pokémon p
    equipes = novas

EQUIPES = []
for eq in equipes:
    if len(eq) > 0:                   # descarta a equipe vazia
        EQUIPES.append(eq)

def h(i, energia):
    poder = 0
    for k in range(len(POKEMONS)):
        if energia[k] > 0:
            poder = poder + PODER[POKEMONS[k]]
    if poder == 0:
        return math.inf
      
    total_dificuldade = 0
    for g in GINASIOS[i:]:
        total_dificuldade = total_dificuldade + DIFICULDADE[g]


def a_estrela():
    inicio = (0, (ENERGIA,) * len(POKEMONS))
    fronteira = [TreeNode(inicio, h(*inicio), gx=0.0)]
    melhor_g = {inicio: 0.0}
    expandidos = 0

    while fronteira:
        no = fronteira.pop()                          # o último é o de menor f(x)
        i, energia = no.get_coord()
        if no.get_value_gx() > melhor_g[no.get_coord()]:
            continue                                  # já achamos caminho melhor
        if i == len(GINASIOS):                        # objetivo: todos decididos
            sol = []
            while no.get_parent():                    # volta pelos pais
                sol.append(no.indice)
                no = no.get_parent()
            return sol[::-1], custo(sol[::-1]), expandidos
        expandidos += 1

        for equipe in EQUIPES:
            # energia de cada Pokémon depois desta batalha
            nova = []
            for k in range(len(POKEMONS)):
                p = POKEMONS[k]                       # nome do Pokémon na posição k
                e = energia[k]                        # energia dele agora
                if p in equipe:
                    nova.append(e - 1)                # luta nesse ginásio: gasta 1
                else:
                    nova.append(e)                    # não luta: energia igual
            nova = tuple(nova)

            if min(nova) < 0 or (i == len(GINASIOS) - 1 and max(nova) == 0):
                continue                              # equipe inválida
            coord = (i + 1, nova)
            gx = no.get_value_gx() + tempo(GINASIOS[i], equipe)
            if gx < melhor_g.get(coord, math.inf):
                melhor_g[coord] = gx
                filho = TreeNode(coord, gx + h(*coord), gx=gx, indice=equipe)
                filho.set_parent(no)

                # coloca o filho na fronteira mantendo a ordem
                # (do MAIOR f(x) para o MENOR, para o menor ficar no fim)
                ini, fim = 0, len(fronteira)
                while ini < fim:
                    meio = (ini + fim) // 2
                    if fronteira[meio] < filho:
                        fim = meio
                    else:
                        ini = meio + 1
                fronteira.insert(ini, filho)


# ------------------------- EXECUÇÃO -------------------------

def mostra(sol):
    for i in range(len(GINASIOS)):
        g = GINASIOS[i]
        equipe = sol[i]
        dificuldade = DIFICULDADE[g]
        t = tempo(g, equipe)
        print(f"  Ginásio {g:>2} ({dificuldade:>3}): {str(equipe):<26} {t:7.3f}")

    print("  Energia final:", energia_final(sol))
    print(f"  C_batalhas = {custo(sol):.4f}")


if __name__ == "__main__":
    N = 30
    resultados = []
    melhor_sol = None
    for semente in range(N):
        random.seed(semente)
        sol, c = simulated_annealing()
        resultados.append(c)
        if c == min(resultados):
            melhor_sol = sol

    # média
    media = sum(resultados) / len(resultados)

    # desvio-padrão (amostral: divide por N - 1)
    soma = 0
    for c in resultados:
        soma = soma + (c - media) ** 2      # distância de cada resultado até a média, ao quadrado
    desvio = (soma / (len(resultados) - 1)) ** 0.5   # raiz quadrada

    print(f"SIMULATED ANNEALING ({N} execuções)")
    print(f"  melhor = {min(resultados):.4f}   média = {media:.4f}"
          f"   desvio-padrão = {desvio:.4f}")
    mostra(melhor_sol)

    print("\nA* (ótimo global)")
    sol_ot, c_ot, expandidos = a_estrela()
    print(f"  ótimo = {c_ot:.4f}   estados expandidos = {expandidos}")
    print(f"  SA achou o ótimo em {sum(abs(c - c_ot) < 1e-6 for c in resultados)}/{N} execuções")
