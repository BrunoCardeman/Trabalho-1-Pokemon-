"""

Busca Local: Utilizada para determinar quais Pokémon participarão de cada batalha, respeitando as restrições de energia
Busca Heuristica A: Utilizada para calcular automaticamente a melhor rota para percorrer todos os 24 ginásios

TODO:

-Criar o mapa (Vanzin)
-Escolher um algoritmo: Implementar Hill Climbing, Simulated Annealing ou Algoritmo Genético para escolher quais Pokémon lutam em cada ginásio. (henrique)
-Experimento: Executar o algoritmo várias vezes e anotar o melhor resultado, a média, o desvio-padrão e o número de testes. (Henrique)
-Algoritmo A*: Usar a busca A* para calcular a melhor rota que parte de 1, passa obrigatoriamente pelos 24 ginásios (em qualquer ordem) e termina em U (Bruno)
-Definições: Definir claramente o estado (quais ginásios já foram visitados), as ações, a função de custo e a heurística (Bruno)
-Mostrar os movimentos do agente no terminal, distinguindo o caminho, a fronteira e os estados visitados (Vanzin)
-Bônus opcional: Criar uma boa interface gráfica 2D/3D (não vale ASCII) para ganhar até 1 ponto extra. (Vanzin)
-programa tem de mostrar a ordem dos ginásios visitados, os Pokémon usados, a energia final de cada um, e os custos individuais e totais ($C_{total} = C_{rota} + C_{batalhas}$)
"""


# (HENRIQUE):
# Faça 3 funções implementando os 3 metodos, Hill Climbing, Simulated Annealing ou Algoritmo Genético. 
# A função ira receber o a dificuldade do ginasio 
# E deverar retornar quanto tempo/pontos foram gastos
# E ela deve retirar la lista de pokemons a vida dos pokemons ultilizados.

import geral as g
from treeNode import TreeNode
import lib as l
import heuristica
import heapq
import simulated_anneling as sa

lista_Ginasios = g.ginasios
lista_Pokemons = g.pokemons
lista_custo = g.custo


def busca_a_estrela(mapa, start_position, end_position, coordenadas_ginasios):
    n = len(coordenadas_ginasios)
    ORIG, DEST = n, n + 1
    pontos = list(coordenadas_ginasios) + [start_position, end_position]

    # menor custo entre todos os pares de pontos (+ predecessores para reconstruir o caminho)
    D, prevs = l.matriz_distancias(mapa, pontos)
    h = heuristica.criar_heuristica(D, n)

    g_inicial = l.custo(mapa, start_position)
    visitados_inicial = frozenset()

    no_inicial = TreeNode(start_position, g_inicial + h(ORIG, visitados_inicial), g_inicial,
                          ginasios_anteriores=visitados_inicial, indice=ORIG)

    fronteira = [no_inicial]
    melhor_g = {(ORIG, visitados_inicial): g_inicial}
    fechados = set() 
    expandidos = 0

    while fronteira:
        no_atual = heapq.heappop(fronteira)
        visitados = no_atual.get_ginasios_visitados()

        estado = (no_atual.indice, visitados)
        if estado in fechados:
            continue                            
        fechados.add(estado)
        expandidos += 1

        if no_atual.indice == DEST:
            indices = []
            no = no_atual
            while no is not None:
                indices.append(no.indice)
                no = no.get_parent()
            indices.reverse()
            celulas = [start_position]
            for a, b in zip(indices, indices[1:]):
                celulas += l.caminho_dijkstra(prevs[a], pontos[a], pontos[b])[1:]

            ordem = [mapa[pontos[i][1]][pontos[i][0]] for i in indices[1:-1]]
            return {
                "no": no_atual,
                "custo": no_atual.get_value_gx(),
                "ordem": ordem,                    #símbolos dos ginásios, na ordem de visita
                "celulas": celulas,                #lista de (x, y) do caminho completo
                "expandidos": expandidos,
            }

        if len(visitados) == n:
            proximos = [DEST]
        else:
            proximos = [k for k in range(n) if k not in visitados]

        for k in proximos:
            if k < n:
                novos_visitados = visitados | {k}  #adiciona o ginasio k no conjunto
            else:
                novos_visitados = visitados        #ir para U não muda os visitados
            vizinho = (k, novos_visitados)

            g_novo = no_atual.get_value_gx() + D[no_atual.indice][k]
            if g_novo >= melhor_g.get(vizinho, float("inf")):
                continue
            melhor_g[vizinho] = g_novo

            f_novo = g_novo + h(k, novos_visitados)
            novo_no = TreeNode(pontos[k], f_novo, g_novo,
                               ginasios_anteriores=novos_visitados, indice=k)
            novo_no.set_parent(no_atual)
            heapq.heappush(fronteira, novo_no)

    print("Erro ao calcular a rota A*\n")
    return None

def percorrer_ginasios(ordem):
    sa.reiniciar_percurso()
    c_batalhas = 0.0
    for k, ginasio in enumerate(ordem):
        custo_batalha = sa.simulated_annealing_ginasio(ginasio)
        c_batalhas += custo_batalha
        retorno = sa.historico[-1]
        equipe = retorno[1]
        print(f"{ginasio:>2}:{', '.join(equipe)}. Custo = {custo_batalha:7f}")
    return c_batalhas


if __name__ == "__main__":
    nome_mapa = 'mapa.txt'
    mapa, start, end = l.read_file(nome_mapa)
    coordenadas_ginasios = l.buscar_ginasios(mapa, lista_Ginasios)

    resultado = busca_a_estrela(mapa, start, end, coordenadas_ginasios)

    if resultado is None:
        raise SystemExit("Não foi possível encontrar uma rota.")

    l.print_solution_map(mapa, resultado["celulas"], end)

    ordem = resultado["ordem"]
    c_rota = resultado["custo"]

    print("Ordem dos ginásios:", " -> ".join(["1"] + ordem + ["U"]))
    c_batalhas = percorrer_ginasios(ordem)

    print("\nEnergia dos Pokémon:")
    for nome, e in sa.energia_atual.items():
        print(f"{nome:<12} {e}")

    c_total = c_rota + c_batalhas
    print(f"\nCusto das batalhas = {c_batalhas:.4f}")
    print(f"\nCusto da rota = {c_rota:.4f}")
    print(f"\nCusto total = {c_total:.4f}")
