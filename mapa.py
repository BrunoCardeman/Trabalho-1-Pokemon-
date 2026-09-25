import pygame
import sys


# =========================
# CONFIGURAÇÕES
# =========================

TILE_SIZE = 32

LARGURA_TELA = 1200
ALTURA_TELA = 700

mapa = []


# =========================
# CARREGAR MAPA
# =========================

def load_mapa(filename):
    global mapa

    mapa = []

    file = open(filename, "r")

    for line in file.readlines():
        # Remove somente o \n do final da linha
        linha = line.rstrip("\n")

        # Transforma a linha em uma lista de caracteres
        mapa.append(list(linha))

    file.close()


# =========================
# CRIAÇÃO DOS TILES
# =========================

def criar_tiles():

    tile_montanha = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_montanha.fill((139, 69, 19))

    tile_agua = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_agua.fill((0, 120, 255))

    tile_floresta = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_floresta.fill((0, 180, 0))

    tile_rochoso = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_rochoso.fill((130, 130, 130))

    tile_livre = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_livre.fill((255, 255, 255))

    return (
        tile_montanha,
        tile_agua,
        tile_floresta,
        tile_rochoso,
        tile_livre
    )


# =========================
# DESENHAR MAPA
# =========================

def draw_screen(screen, tiles, camera_x, camera_y):

    tile_montanha = tiles[0]
    tile_agua = tiles[1]
    tile_floresta = tiles[2]
    tile_rochoso = tiles[3]
    tile_livre = tiles[4]

    screen.fill((0, 0, 0))

    for i in range(len(mapa)):
        for j in range(len(mapa[i])):

            x = j * TILE_SIZE - camera_x
            y = i * TILE_SIZE - camera_y

            # Não desenha tiles que estão completamente fora da tela
            if x + TILE_SIZE < 0:
                continue

            if x > LARGURA_TELA:
                continue

            if y + TILE_SIZE < 0:
                continue

            if y > ALTURA_TELA:
                continue

            if mapa[i][j] == "M":
                screen.blit(tile_montanha, (x, y))

            elif mapa[i][j] == "A":
                screen.blit(tile_agua, (x, y))

            elif mapa[i][j] == "F":
                screen.blit(tile_floresta, (x, y))

            elif mapa[i][j] == "R":
                screen.blit(tile_rochoso, (x, y))

            elif mapa[i][j] == ".":
                screen.blit(tile_livre, (x, y))

            else:
                # Por enquanto, ginásios e outros símbolos
                # aparecem como terreno livre
                screen.blit(tile_livre, (x, y))


# =========================
# PROGRAMA PRINCIPAL
# =========================

def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (LARGURA_TELA, ALTURA_TELA)
    )

    pygame.display.set_caption("Mapa - Região de Kanto")

    clock = pygame.time.Clock()

    # Carrega o mapa
    load_mapa("Mapa.txt")

    # Cria os tiles
    tiles = criar_tiles()

    # Posição da câmera
    camera_x = 0
    camera_y = 0

    rodando = True

    while rodando:

        # =========================
        # EVENTOS
        # =========================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

        # =========================
        # MOVIMENTO DA CÂMERA
        # =========================

        keys = pygame.key.get_pressed()

        velocidade_camera = 10

        if keys[pygame.K_LEFT]:
            camera_x -= velocidade_camera

        if keys[pygame.K_RIGHT]:
            camera_x += velocidade_camera

        if keys[pygame.K_UP]:
            camera_y -= velocidade_camera

        if keys[pygame.K_DOWN]:
            camera_y += velocidade_camera

        # =========================
        # LIMITES DA CÂMERA
        # =========================

        largura_mapa = len(mapa[0]) * TILE_SIZE
        altura_mapa = len(mapa) * TILE_SIZE

        camera_x = max(0, camera_x)