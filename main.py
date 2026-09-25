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


