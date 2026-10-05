import pygame
import sys
import os
import random

# =========================
# CONFIGURAÇÕES
# =========================

TILE_SIZE = 10

LARGURA_TELA = 1505
ALTURA_TELA = 420

mapa = []


# =========================
# CARREGAR MAPA
# =========================

def load_mapa(filename):

    global mapa

    mapa = []

    with open(filename, "r", encoding="utf-8") as file:

        for line in file.readlines():

            linha = line.rstrip("\n")

            nova_linha = []

            for simbolo in linha:

                # =========================
                # FLORESTA
                # =========================

                if simbolo == "F":

                    tipo_floresta = random.choices(
                        ["F", "FC"],
                        weights=[95, 5],
                        k=1
                    )[0]

                    nova_linha.append(tipo_floresta)

                else:

                    nova_linha.append(simbolo)

            mapa.append(nova_linha)


# =========================
# CARREGAR SPRITES
# =========================

def carregar_sprites():

    pasta = "sprites"

    sprites = {}

    sprites["M"] = pygame.image.load(
        os.path.join(pasta, "montanha.png")
    ).convert()

    sprites["A"] = pygame.image.load(
        os.path.join(pasta, "agua.png")
    ).convert()

    sprites["F"] = pygame.image.load(
        os.path.join(pasta, "floresta.jpg")
    ).convert()

    sprites["FC"] = pygame.image.load(
        os.path.join(pasta, "floresta_caterpie.jpg")
    ).convert()

    sprites["R"] = pygame.image.load(
        os.path.join(pasta, "pedra.png")
    ).convert()

    sprites["."] = pygame.image.load(
        os.path.join(pasta, "grama.jpg")
    ).convert()

    sprites["GYM"] = pygame.image.load(
        os.path.join(pasta, "gym.jpg")
    ).convert()

    # Ajusta os sprites para o tamanho dos tiles
    for simbolo in sprites:

        sprites[simbolo] = pygame.transform.scale(
            sprites[simbolo],
            (TILE_SIZE, TILE_SIZE)
        )

    return sprites


# =========================
# DESENHAR MAPA
# =========================

def draw_screen(screen, sprites):

    screen.fill((0, 0, 0))

    # Símbolos que representam ginásios
    simbolos_gym = [
        "2", "3", "4", "5", "6", "7", "8", "9",
        "B", "C", "D", "E", "G", "H", "I", "J",
        "K", "L", "N", "O", "P", "Q", "S", "T"
    ]

    for i in range(len(mapa)):

        for j in range(len(mapa[i])):

            x = j * TILE_SIZE
            y = i * TILE_SIZE

            simbolo = mapa[i][j]

            # =========================
            # GINÁSIOS
            # =========================

            if simbolo in simbolos_gym:

                screen.blit(
                    sprites["GYM"],
                    (x, y)
                )

            # =========================
            # OUTROS SPRITES
            # =========================

            elif simbolo in sprites:

                screen.blit(
                    sprites[simbolo],
                    (x, y)
                )

            # =========================
            # SÍMBOLOS DESCONHECIDOS
            # =========================

            else:

                screen.blit(
                    sprites["."],
                    (x, y)
                )


# =========================
# PROGRAMA PRINCIPAL
# =========================

def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (LARGURA_TELA, ALTURA_TELA)
    )

    pygame.display.set_caption(
        "Mapa - Região de Kanto"
    )

    clock = pygame.time.Clock()

    # Carrega o mapa
    # Aqui os Caterpies são sorteados
    load_mapa("mapa.txt")

    # Carrega os sprites
    sprites = carregar_sprites()

    rodando = True

    while rodando:

        # =========================
        # EVENTOS
        # =========================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

        # =========================
        # DESENHAR MAPA
        # =========================

        draw_screen(
            screen,
            sprites
        )

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    main()
