import random
from array import array

import numpy as np


def _construir_pdb(Dn, grupo, destino):
    m, N = len(grupo), Dn.shape[0]
    F = np.full((1 << m, N), 1 << 30, dtype=np.int64)
    F[0, :] = Dn[:, destino]                       # nada a visitar: só ir até U

    todas = np.arange(1, 1 << m)
    bits = np.array([bin(x).count("1") for x in range(1 << m)])

    for camada in range(1, m + 1):
        masks = todas[bits[todas] == camada]
        for k in range(m):
            sel = masks[((masks >> k) & 1) == 1]   # máscaras da camada que contêm o ginásio k
            if sel.size == 0:
                continue
            cand = Dn[:, grupo[k]][None, :] + F[sel ^ (1 << k), grupo[k]][:, None]
            F[sel] = np.minimum(F[sel], cand)
    return F


def criar_heuristica(D, n, tam=16, qtd=4, candidatos=60, semente=1):
    destino, origem, N = n + 1, n, n + 2
    Dn = np.array(D, dtype=np.int64)

    # Com poucos ginásios, um único grupo com todos já é exato.
    if n <= tam:
        grupos = [list(range(n))]
    else:
        rnd = random.Random(semente)
        cands = []
        for _ in range(candidatos):
            g = sorted(rnd.sample(range(n), tam))
            F = _construir_pdb(Dn, g, destino)
            cands.append((int(F[(1 << tam) - 1, origem]), g, F))   # limite inferior na origem
        cands.sort(key=lambda t: -t[0])
        grupos = [g for _, g, _ in cands[:qtd]]
        pdbs_prontos = [F for _, _, F in cands[:qtd]]

    if n <= tam:
        pdbs_prontos = [_construir_pdb(Dn, grupos[0], destino)]

    # Para cada grupo guardamos a tabela F (em vetor plano) e a lista de (ginásio, valor do seu "bit"
    # na tabela). A tabela é indexada por subconjunto, por isso cada ginásio do grupo vale 1, 2, 4, 8...
    tabelas = []
    for grupo, F in zip(grupos, pdbs_prontos):
        membros = [(k, 1 << pos) for pos, k in enumerate(grupo)]
        tabelas.append((array("H", F.ravel().tolist()), membros))

    def h(atual, visitados):
        melhor = 0
        for F, membros in tabelas:
            # sub = identificador do subconjunto de ginásios DO GRUPO que ainda faltam
            sub = 0
            for k, valor in membros:
                if k not in visitados:
                    sub += valor
            v = F[sub * N + atual]          # F[sub][atual], com a tabela achatada
            if v > melhor:
                melhor = v                  # máximo entre os grupos
        return melhor

    return h