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
import time
from queue import PriorityQueue
import time

lista_Ginasios = g.ginasios
lista_Pokemons = g.pokemons
lista_custo = g.custo

def busca_a_estrela(mapa, start_position, end_position, coordenadas_ginasios):

    fronteira = []
    visitados = set()

    h_inicial = l.manhattan_distance(start_position, coordenadas_ginasios)
    no_inicial = TreeNode(start_position,h_inicial+1,1)

    if start_position in coordenadas_ginasios:
        no_inicial.add_ginasios_visitados(start_position)
    else:
        no_inicial.set_ginasios_visitados([])

    fronteira.append(no_inicial)
    
    while fronteira:
        no_atual = min(fronteira, key= lambda node: node.get_priority())
        fronteira.remove(no_atual)

        pos_atual = no_atual.get_coord()
        g_atual = no_atual.get_value_gx()
        ginasios_visitados_atual = no_atual.get_ginasios_visitados()

        ultimo_no_expandido = no_atual

        if pos_atual in coordenadas_ginasios and pos_atual not in ginasios_visitados_atual:
            no_atual.add_ginasios_visitados(pos_atual)
            ginasios_visitados_atual = no_atual.get_ginasios_visitados()
            

        if pos_atual == end_position and len(ginasios_visitados_atual) == len(coordenadas_ginasios):
            print("acabou")
            caminho = []
            no_temporario = no_atual
            while no_temporario is not None:
                caminho.append(no_temporario.get_coord())
                no_temporario = no_temporario.get_parent()
            
            # Como o caminho foi pego de trás para frente (do Fim pro Início), invertemos:
            caminho.reverse()
            
            print("\n--- CAMINHO ENCONTRADO! ---")
            print("Passos:", caminho)
            print("Total de ginásios visitados:", len(ginasios_visitados_atual))

            return no_atual

        estado_atual = (pos_atual, tuple(sorted(ginasios_visitados_atual)))
        if estado_atual in visitados:
            continue
        visitados.add(estado_atual)

        visinhos = l.get_neighborhood(mapa, pos_atual)

        #l.printMap(mapa,pos_atual)
        #time.sleep(0.09)

        for visinho in visinhos:
            coord_visinho= visinho[0]
            custo_visinho = visinho[1]

            g_novo = g_atual +custo_visinho

            ginasios_pendentes = [g for g in coordenadas_ginasios if g not in ginasios_visitados_atual]
            if len(ginasios_pendentes) == 0:
                # Se JÁ visitou todos os 24 ginásios, a prioridade agora é chegar no FIM (end_position)
                h_novo = abs(coord_visinho[0] - end_position[0]) + abs(coord_visinho[1] - end_position[1])
            else:
                # Se ainda faltam ginásios, calcula a distância até o ginásio pendente mais próximo
                h_novo = l.manhattan_distance(coord_visinho, ginasios_pendentes)
            copia_ginasios = list(ginasios_visitados_atual)
            novo_no = TreeNode(coord_visinho, h_novo + g_novo, g_novo, ginasios_anteriores=copia_ginasios)

            if coord_visinho in coordenadas_ginasios and coord_visinho not in novo_no.get_ginasios_visitados():
                novo_no.add_ginasios_visitados(coord_visinho)

            novo_no.set_parent(no_atual)
            no_atual.add_child(novo_no)

            fronteira.append(novo_no)

    print("Coordenadas Ginasios",coordenadas_ginasios)
    
    print("--- A* FALHOU ---")
    print(f"Coordenada final que ele tentou: {ultimo_no_expandido.get_coord()}")
    print(f"Ginásios visitados por ele: {ultimo_no_expandido.get_ginasios_visitados()}")
    print(f"Total de ginásios visitados: {len(ultimo_no_expandido.get_ginasios_visitados())}")
    return None


nome_mapa = 'mapa.txt'
mapa, start, end = l.read_file(nome_mapa)
pos_atual = start
l.printMap(mapa,start)
busca_a_estrela(mapa,start,end,l.buscar_ginasios(mapa, lista_Ginasios) )