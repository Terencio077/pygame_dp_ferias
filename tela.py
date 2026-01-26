import pygame
import sys
import os
from config import *
import musicas

# variaveis
BG_FIELD = None

def load_background():
    """Load the background image for the field."""
    global BG_FIELD
    largura, altura = WIDTH, HEIGHT
    
    filenames = ['plano de fundo.png', 'plano_de_fundo.png', 'fundo.png', 
                 'Plano de fundo.png', 'background.png', 'Background.png',
                 'fundo.tela.png']
    
    for filename in filenames:
        caminho = os.path.join('assets_futebol', filename)
        try:
            if os.path.exists(caminho):
                BG_FIELD = pygame.image.load(caminho).convert()
                BG_FIELD = pygame.transform.scale(BG_FIELD, (largura, altura))
                print(f"Background loaded: {filename}")
                return
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
    
    print("AVISO: Imagem de fundo não encontrada! Usando cor sólida.")
    BG_FIELD = pygame.Surface((largura, altura))
    BG_FIELD.fill((30, 144, 255))

def desenhar_texto_contornado(screen, texto, fonte, cor_interna, cor_contorno, pos_centro):
    x, y = pos_centro
    offsets = [(-2,-2), (0,-2), (2,-2), (-2,0), (2,0), (-2,2), (0,2), (2,2)]
    for dx, dy in offsets:
        surf_c = fonte.render(texto, True, cor_contorno)
        screen.blit(surf_c, surf_c.get_rect(center=(x + dx, y + dy)))
    surf_p = fonte.render(texto, True, cor_interna)
    screen.blit(surf_p, surf_p.get_rect(center=(x, y)))

def tela_inicial(screen, clock):
    # le arquivo de som
    musicas.load_wakawaka()
    
    largura, altura = screen.get_size()
    caminho = os.path.join('assets_futebol', 'fundo.tela.png')
    try:
        bg_menu = pygame.image.load(caminho).convert()
        bg_menu = pygame.transform.scale(bg_menu, (largura, altura))
    except:
        bg_menu = pygame.Surface((largura, altura))
        bg_menu.fill((30, 144, 255))

    fonte_nome = "impact" 
    font_titulo = pygame.font.SysFont(fonte_nome, 100)
    font_menu = pygame.font.SysFont(fonte_nome, 55)
    font_ajuda = pygame.font.SysFont("arial", 25, bold=True)
    options = ["PLAY", "CONFIGURAÇÕES", "SAIR"]
    mostrar_ajuda = False
    
    # Play wakawaka sound
    musicas.play_wakawaka()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        rects = []
        for i in range(len(options)):
            r = pygame.Rect(0, 0, 450, 60)
            r.center = (largura // 2, 350 + (i * 90))
            rects.append(r)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if not mostrar_ajuda:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, r in enumerate(rects):
                        if r.collidepoint(mouse_pos):
                            if i == 0: 
                                # Stop wakawaka before returning
                                musicas.stop_wakawaka()
                                return 
                            elif i == 1: mostrar_ajuda = True
                            elif i == 2: pygame.quit(); sys.exit()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    mostrar_ajuda = False

        screen.blit(bg_menu, (0, 0))
        if not mostrar_ajuda:
            desenhar_texto_contornado(screen, "FUTEBOL GAME", font_titulo, (255,255,255), (0,0,0), (largura//2, 150))
            for i, opt in enumerate(options):
                cor = (255, 215, 0) if rects[i].collidepoint(mouse_pos) else (255, 255, 255)
                desenhar_texto_contornado(screen, opt, font_menu, cor, (0,0,0), rects[i].center)
        else:
            overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0,0))
            instrucoes = ["COMO JOGAR", "", "P1: WASD | S: Chute", "P2: Setas | Baixo: Chute", "", "CLIQUE PARA VOLTAR"]
            for i, l in enumerate(instrucoes):
                cor = (255, 215, 0) if i == 0 else (255, 255, 255)
                desenhar_texto_contornado(screen, l, font_ajuda, cor, (0,0,0), (largura//2, 150 + i*50))
        pygame.display.flip()
        clock.tick(60)

def tela_vitoria(screen, clock, vencedor):
    largura, altura = screen.get_size()
    fonte_nome = "impact"
    font_titulo = pygame.font.SysFont(fonte_nome, 90)
    font_placar = pygame.font.SysFont(fonte_nome, 110)
    font_menu = pygame.font.SysFont(fonte_nome, 55)
    options = ["REINICIAR", "SAIR"]
    
    caminho = os.path.join('assets_futebol', 'fundo.tela.png')
    try:
        bg_menu = pygame.image.load(caminho).convert()
        bg_menu = pygame.transform.scale(bg_menu, (largura, altura))
    except:
        bg_menu = pygame.Surface((largura, altura))
        bg_menu.fill((30, 144, 255))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        rects = []
        for i in range(len(options)):
            r = pygame.Rect(0, 0, 350, 60)
            r.center = (largura // 2, 400 + (i * 90))
            rects.append(r)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, r in enumerate(rects):
                    if r.collidepoint(mouse_pos):
                        if i == 0: return "REINICIAR"
                        elif i == 1: pygame.quit(); sys.exit()

        screen.blit(bg_menu, (0, 0))
        cor_v = (60, 140, 220) if vencedor == "Azul" else (220, 60, 60)
        desenhar_texto_contornado(screen, "VENCEDOR:", font_titulo, (255,255,255), (0,0,0), (largura//2, 120))
        desenhar_texto_contornado(screen, vencedor.upper(), font_placar, cor_v, (0,0,0), (largura//2, 230))
        for i, opt in enumerate(options):
            cor = (255, 215, 0) if rects[i].collidepoint(mouse_pos) else (255, 255, 255)
            desenhar_texto_contornado(screen, opt, font_menu, cor, (0,0,0), rects[i].center)
        pygame.display.flip()
        clock.tick(60)

def draw_field(screen):
    """Draw the football field background."""
    global BG_FIELD
    if BG_FIELD:
        screen.blit(BG_FIELD, (0, 0))
    else:
        screen.fill((34, 139, 34))