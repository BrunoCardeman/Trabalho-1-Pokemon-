import pygame
import sys
import os
import random
import main as algoritmo
import lib as l


TILE_SIZE = 10
ARQUIVO_MAPA = "mapa.txt"

mapa = []

SIMBOLOS_GYM = [
    "2", "3", "4", "5", "6", "7", "8", "9",
    "B", "C", "D", "E", "G", "H", "I", "J",
    "K", "L", "N", "O", "P", "Q", "S", "T"
]

COR_CAMINHO = (255, 215, 0, 140)
COR_BORDA_CAMINHO = (255, 235, 80, 220)
COR_INICIO = (0, 200, 0)
COR_FIM = (0, 120, 255)
COR_AGENTE = (255, 0, 0)


def load_mapa(arq):
    global mapa
    mapa = []

    with open(arq, "r", encoding="utf-8") as f:
        for line in f.readlines():
            linha = line.rstrip("\n")
            nova_linha = []
            # Quadrado da floresta aleatorio (floresta - floresta_caterpie)
            for simbolo in linha:
                if simbolo == "F":
                    tipo_floresta = random.choices(
                        ["F", "FC"], weights=[97, 3], k=1
                    )[0]
                    nova_linha.append(tipo_floresta)
                else:
                    nova_linha.append(simbolo)
            mapa.append(nova_linha)

def carregar_sprites():
    pasta = "sprites"
    arquivos = {
        "M": "montanha.png",
        "A": "agua.png",
        "F": "floresta.png",
        "FC": "floresta_caterpie.png",
        "R": "pedra.png",
        ".": "grama.png",
        "GYM": "gym.png",
    }

    sprites = {}
    for simbolo, nome in arquivos.items():
        img = pygame.image.load(os.path.join(pasta, nome)).convert()
        sprites[simbolo] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    return sprites

def calcular_rota():
    mapa_busca, start, end = l.read_file(ARQUIVO_MAPA)
    coordenadas_ginasios = l.buscar_ginasios(mapa_busca, algoritmo.lista_Ginasios)
    resultado = algoritmo.busca_a_estrela(mapa_busca, start, end, coordenadas_ginasios)

    if resultado is None:
        print("Não foi possível encontrar uma rota.")
        return None, start, end
    return resultado, start, end

def criar_camada_terreno(sprites, largura, altura):
    camada = pygame.Surface((largura, altura))
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            simbolo = mapa[i][j]
            if simbolo in SIMBOLOS_GYM or simbolo not in sprites:
                sprite = sprites["."]
            else:
                sprite = sprites[simbolo]
            camada.blit(sprite, (j * TILE_SIZE, i * TILE_SIZE))
    return camada

def criar_camada_ginasios(sprites, largura, altura, start, end):
    camada = pygame.Surface((largura, altura), pygame.SRCALPHA)

    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] in SIMBOLOS_GYM:
                camada.blit(sprites["GYM"], (j * TILE_SIZE, i * TILE_SIZE))

    for (x, y), cor in ((start, COR_INICIO), (end, COR_FIM)):
        pygame.draw.rect(
            camada, cor, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        )
        pygame.draw.rect(
            camada, (255, 255, 255),
            (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1
        )
    return camada

def pintar_celula(camada_caminho, celula):
    x, y = celula
    rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(camada_caminho, COR_CAMINHO, rect)
    pygame.draw.rect(camada_caminho, COR_BORDA_CAMINHO, rect, 1)

def main():
    pygame.init()

    load_mapa(ARQUIVO_MAPA)
    largura = len(mapa[0]) * TILE_SIZE
    altura = len(mapa) * TILE_SIZE

    screen = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Trabalho 1 - IA")
    clock = pygame.time.Clock()

    sprites = carregar_sprites()

    resultado, start, end = calcular_rota()
    caminho = resultado["celulas"] if resultado is not None else []

    camada_terreno = criar_camada_terreno(sprites, largura, altura)
    camada_ginasios = criar_camada_ginasios(sprites, largura, altura, start, end)
    camada_caminho = pygame.Surface((largura, altura), pygame.SRCALPHA)

    passo = 0 
    velocidade = 1

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
        for _ in range(velocidade):
            if passo < len(caminho):
                pintar_celula(camada_caminho, caminho[passo])
                passo += 1
        screen.blit(camada_terreno, (0, 0))
        screen.blit(camada_caminho, (0, 0))
        screen.blit(camada_ginasios, (0, 0))
        
        if caminho and passo > 0:
            ax, ay = caminho[passo - 1]
            centro = (ax * TILE_SIZE + TILE_SIZE // 2, ay * TILE_SIZE + TILE_SIZE // 2)
            pygame.draw.circle(screen, COR_AGENTE, centro, TILE_SIZE // 2 + 1)
            pygame.draw.circle(screen, (255, 255, 255), centro, TILE_SIZE // 2 + 1, 1)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
