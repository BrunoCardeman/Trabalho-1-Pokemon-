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
from treeNode import TreeNode

NOMES = ["Pikachu", "Bulbassauro", "Rattata", "Caterpie", "Weedle"]
PODER = {}
for i in range(len(NOMES)):
    nome = NOMES[i]
    poder = geral.pokemons[i][1]
    PODER[nome] = poder
ENERGIA = geral.pokemons[0][0] 
DIFICULDADE = dict(geral.ginasios)  

GINASIOS = list(DIFICULDADE)
POKEMONS = list(PODER)

def tempo(ginasio, equipe):
    soma_poder = 0
    for p in equipe:
        soma_poder = soma_poder + PODER[p]
    return DIFICULDADE[ginasio] / soma_poder

def custo(sol):
    total = 0
    for i in range(len(GINASIOS)):
        g = GINASIOS[i]          
        equipe = sol[i]        
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

def solucao_inicial():
    sol = []
    for i in range(len(GINASIOS)):         
        posicao = i % len(POKEMONS)             
        pokemon = POKEMONS[posicao]              
        sol.append([pokemon])                   
    random.shuffle(sol)                         
    return sol

def vizinho(sol):
    """Gera vizinhos aleatórios até achar um VÁLIDO (os inválidos são descartados)."""
    while True:
        nova = []
        for equipe in sol:
            nova.append(list(equipe))        #copia cada equipe para uma lista nova
        a, b = random.sample(range(len(nova)), 2)
        p, q = random.sample(POKEMONS, 2)
        op = random.choice([0, 1, 2])
        if op == 0:                          #coloca ou tira o Pokémon p do ginásio a
            if p in nova[a]:
                nova[a].remove(p)
            else:
                nova[a].append(p)
        elif op == 1:                      
            nova[a], nova[b] = nova[b], nova[a]
        elif p in nova[a] and q in nova[b] and q not in nova[a] and p not in nova[b]:
            nova[a].remove(p)         
            nova[a].append(q)              
            nova[b].remove(q)           
            nova[b].append(p)             
        if nova != sol and valida(nova):
            return nova

def simulated_annealing(T=50.0, alpha=0.9999, T_min=0.001):
    atual = solucao_inicial()
    c_atual = custo(atual)
    melhor, c_melhor = atual, c_atual
    while T > T_min:
        cand = vizinho(atual)
        delta = custo(cand) - c_atual
        if delta < 0 or random.random() < math.exp(-delta / T):
            atual, c_atual = cand, c_atual + delta
            if c_atual < c_melhor:
                melhor, c_melhor = atual, c_atual
        T *= alpha
    return melhor, c_melhor
energia_atual = {}
historico = []          #lista de ginasio, equipe e custo_da_batalha na ordem que foram visitados

def reiniciar_percurso():
    energia_atual.clear()   #zera a energia de todos os Pokémon e o historico^
    for p in POKEMONS:
        energia_atual[p] = ENERGIA
    historico.clear()


reiniciar_percurso()

def _valida_plano(equipes, energia):
    uso = {p: 0 for p in POKEMONS}
    for eq in equipes:
        if not eq:
            return False
        for p in eq:
            uso[p] += 1
    sobra = 0
    for p in POKEMONS:
        resto = energia[p] - uso[p]
        if resto < 0:
            return False
        sobra += resto
    return sobra >= 1

def _vizinho_plano(equipes, energia):
    for _ in range(200):
        nova = [list(e) for e in equipes]
        a = random.randrange(len(nova))
        afetados = [a]
        p, q = random.sample(POKEMONS, 2)
        op = random.choice([0, 1, 2])
        if op == 0:                               
            if p in nova[a]:
                nova[a].remove(p)
            else:
                nova[a].append(p)
        elif op == 1 and len(nova) > 1:               
            b = random.choice([i for i in range(len(nova)) if i != a])
            if p in nova[a] and p not in nova[b]:
                nova[a].remove(p)
                nova[b].append(p)
                afetados = [a, b]
        elif p in nova[a] and q not in nova[a]:      
            nova[a].remove(p)
            nova[a].append(q)
        if nova != equipes and _valida_plano(nova, energia):
            return nova, afetados
    return None

def _annealing_plano(ginasios, energia, T, alpha, T_min):
    m = len(ginasios)
    resto = dict(energia)
    atual = []
    for _ in range(m):                                #inicial: um Pokémon por ginásio,
        p = max(POKEMONS, key=lambda x: resto[x])     #sempre o que tem mais energia
        resto[p] -= 1
        atual.append([p])
    if not _valida_plano(atual, energia):
        raise ValueError("Energia insuficiente para cobrir os ginásios restantes.")

    c_atual = sum(tempo(ginasios[i], atual[i]) for i in range(m))
    melhor, c_melhor = atual, c_atual
    while T > T_min:
        viz = _vizinho_plano(atual, energia)
        if viz is not None:
            cand, afetados = viz
            delta = 0
            for i in afetados:
                delta += tempo(ginasios[i], cand[i]) - tempo(ginasios[i], atual[i])
            if delta < 0 or random.random() < math.exp(-delta / T):
                atual, c_atual = cand, c_atual + delta
                if c_atual < c_melhor:
                    melhor, c_melhor = atual, c_atual
        T *= alpha
    return melhor, c_melhor


def simulated_annealing_ginasio(ginasio, T=30.0, alpha=0.9995, T_min=0.01):
    visitados = [h[0] for h in historico]
    if ginasio not in DIFICULDADE:
        raise ValueError(f"Ginásio desconhecido: {ginasio}")
    if ginasio in visitados:
        raise ValueError(f"Ginásio {ginasio} já foi visitado.")

    futuros = [g for g in GINASIOS if g != ginasio and g not in visitados]
    plano, _ = _annealing_plano([ginasio] + futuros, dict(energia_atual), T, alpha, T_min)
    equipe = plano[0]                    

    for p in equipe:
        energia_atual[p] -= 1             
    custo_batalha = tempo(ginasio, equipe)
    historico.append((ginasio, list(equipe), custo_batalha))
    return custo_batalha

equipes = [[]]                        #começa com a equipe vazia
for p in POKEMONS:
    novas = []
    for eq in equipes:
        novas.append(eq)            
        novas.append(eq + [p])     
    equipes = novas

EQUIPES = []
for eq in equipes:
    if len(eq) > 0:                   #descarta a equipe vazia
        EQUIPES.append(eq)

def h(i, energia):
    if i == len(GINASIOS):
        return 0                  
    poder = 0
    for k in range(len(POKEMONS)):
        if energia[k] > 0:
            poder = poder + PODER[POKEMONS[k]]
    if poder == 0:
        return math.inf
      
    total_dificuldade = 0
    for g in GINASIOS[i:]:
        total_dificuldade = total_dificuldade + DIFICULDADE[g]
    return total_dificuldade / poder


def a_estrela():
    energia_inicial = []
    for k in range(len(POKEMONS)):
      energia_inicial.append(ENERGIA)           #um 6 para cada Pokémon
    inicio = (0, tuple(energia_inicial))        #(0, (6, 6, 6, 6, 6))
    fronteira = [TreeNode(inicio, h(*inicio), gx=0.0)]
    melhor_g = {inicio: 0.0}
    expandidos = 0

    while fronteira:
        no = fronteira.pop()                        
        i, energia = no.get_coord()
        if no.get_value_gx() > melhor_g[no.get_coord()]:
            continue                                  #Continua se ja encontrou um caminho melhor
        if i == len(GINASIOS):                       
            sol = []
            while no.get_parent():                    #volta pelos pais
                sol.append(no.indice)
                no = no.get_parent()
            return sol[::-1], custo(sol[::-1]), expandidos
        expandidos += 1

        for equipe in EQUIPES:
            nova = []
            for k in range(len(POKEMONS)):
                p = POKEMONS[k]                       #nome do Pokémon na posição k
                e = energia[k]                        #energia atual
                if p in equipe:
                    nova.append(e - 1)                #-1 de energia pelo ginasio
                else:
                    nova.append(e)                    #nao luta
            nova = tuple(nova)

            if min(nova) < 0 or (i == len(GINASIOS) - 1 and max(nova) == 0):
                continue                              #equipe inválida
            coord = (i + 1, nova)
            gx = no.get_value_gx() + tempo(GINASIOS[i], equipe)
            if gx < melhor_g.get(coord, math.inf):
                melhor_g[coord] = gx
                filho = TreeNode(coord, gx + h(*coord), gx=gx, indice=equipe)
                filho.set_parent(no)                  # coloca o filho na fronteira mantendo a ordem
                ini, fim = 0, len(fronteira)
                while ini < fim:
                    meio = (ini + fim) // 2
                    if fronteira[meio] < filho:
                        fim = meio
                    else:
                        ini = meio + 1
                fronteira.insert(ini, filho)

def mostra(sol):
    for i in range(len(GINASIOS)):
        g = GINASIOS[i]
        equipe = sol[i]
        dificuldade = DIFICULDADE[g]
        t = tempo(g, equipe)
        print(f"  Ginásio {g:>2} ({dificuldade:>3}): {str(equipe):<26} {t:7.3f}")
    print("  Energia final:", energia_final(sol))
    print(f"  C_batalhas = {custo(sol):.4f}")



N = 30
resultados = []
melhor_sol = None
for semente in range(N):
    random.seed(semente)
    sol, c = simulated_annealing()
    resultados.append(c)
    if c == min(resultados):
        melhor_sol = sol

    
media = sum(resultados) / len(resultados)

# desvio-padrão (amostral: divide por N - 1)
soma = 0
for c in resultados:
    soma = soma + (c - media) ** 2      # distância de cada resultado até a média, ao quadrado
desvio = (soma / (len(resultados) - 1)) ** 0.5   # raiz quadrada

print(f"SIMULATED ANNEALING ({N} execuções)")
print(f"  melhor = {min(resultados):.4f}   média = {media:.4f}"f"   desvio-padrão = {desvio:.4f}")mostra(melhor_sol)
print("\nA* (ótimo global)")
sol_ot, c_ot, expandidos = a_estrela()
print(f"  ótimo = {c_ot:.4f}   estados expandidos = {expandidos}")
print(f"  SA achou o ótimo em {sum(abs(c - c_ot) < 1e-6 for c in resultados)}/{N} execuções")
