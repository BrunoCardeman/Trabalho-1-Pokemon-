import pygame
import sys
import os
import random


TILE_SIZE = 10
LARGURA_TELA = 1505
ALTURA_TELA = 420

mapa = []

def load_mapa(arq):
    global mapa
    mapa = []
    with open(arq, "r", encoding="utf-8") as f:
        for line in f.readlines():
            linha = line.rstrip("\n")
            nova_linha = []
            for simbolo in linha:   #mato c/ sprite aleatorio
                if simbolo == "F":
                    tipo_floresta = random.choices(["F", "FC"], weights=[97,3], k=1)[0]
                    nova_linha.append(tipo_floresta)
                else:
                    nova_linha.append(simbolo)
            mapa.append(nova_linha)

def carregar_sprites():
    pasta = "sprites"
    sprites = {}
    sprites["M"] = pygame.image.load(os.path.join(pasta, "montanha.png")).convert()
    sprites["A"] = pygame.image.load(os.path.join(pasta, "agua.png")).convert()
    sprites["F"] = pygame.image.load(os.path.join(pasta, "floresta.jpg")).convert()
    sprites["FC"] = pygame.image.load(os.path.join(pasta, "floresta_caterpie.jpg")).convert()
    sprites["R"] = pygame.image.load(os.path.join(pasta, "pedra.png")).convert()
    sprites["."] = pygame.image.load(os.path.join(pasta, "grama.jpg")).convert()
    sprites["GYM"] = pygame.image.load(os.path.join(pasta, "gym.jpg")).convert()
    for simbolo in sprites: # Ajusta o tamanho dos sprites
        sprites[simbolo] = pygame.transform.scale(sprites[simbolo],(TILE_SIZE, TILE_SIZE))
    return sprites

def draw_screen(screen, sprites):
    screen.fill((0, 0, 0))
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
            if simbolo in simbolos_gym:
                screen.blit(sprites["GYM"],(x, y))
            elif simbolo in sprites:
                screen.blit(sprites[simbolo],(x, y))
            else:
                screen.blit(sprites["."],(x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Trabalho 1 - IA")
    clock = pygame.time.Clock()
    load_mapa("mapa.txt")
    sprites = carregar_sprites()
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
        draw_screen(screen,sprites) #desenha o mapa 
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

main()
