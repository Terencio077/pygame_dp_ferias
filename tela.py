import pygame
import sys
import os

def desenhar_texto_contornado(screen, texto, fonte, cor_interna, cor_contorno, pos_centro):
    """Cria o efeito de contorno grosso igual ao da imagem"""
    x, y = pos_centro
    # Desenha o contorno em 8 direções para dar espessura
    offsets = [(-2,-2), (0,-2), (2,-2), (-2,0), (2,0), (-2,2), (0,2), (2,2)]
    for dx, dy in offsets:
        surf_c = fonte.render(texto, True, cor_contorno)
        screen.blit(surf_c, surf_c.get_rect(center=(x + dx, y + dy)))
    
    # Desenha o texto principal por cima
    surf_p = fonte.render(texto, True, cor_interna)
    screen.blit(surf_p, surf_p.get_rect(center=(x, y)))

def tela_inicial(screen, clock):
    largura, altura = screen.get_size()
    
    # Carrega a imagem da pasta assets_futebol conforme seu projeto
    caminho = os.path.join('assets_futebol', 'fundo.tela.png')
    try:
        bg_menu = pygame.image.load(caminho).convert()
        bg_menu = pygame.transform.scale(bg_menu, (largura, altura))
    except:
        bg_menu = pygame.Surface((largura, altura))
        bg_menu.fill((30, 144, 255))

    # Configuração de Fontes
    fonte_nome = "impact" 
    font_titulo = pygame.font.SysFont(fonte_nome, 100)
    font_menu = pygame.font.SysFont(fonte_nome, 55)
    font_ajuda = pygame.font.SysFont("arial", 25, bold=True)

    options = ["PLAY", "CONFIGURAÇÕES", "SAIR"]
    mostrar_ajuda = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        # Criamos os retângulos de colisão para cada opção
        rects = []
        for i in range(len(options)):
            # Retângulo invisível para detectar o mouse
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
                            if i == 0: return # Botão PLAY
                            elif i == 1: mostrar_ajuda = True # Botão CONFIGURAÇÕES
                            elif i == 2: pygame.quit(); sys.exit() # Botão SAIR
            else:
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    mostrar_ajuda = False

        # --- DESENHO ---
        screen.blit(bg_menu, (0, 0))

        if not mostrar_ajuda:
            # Título principal
            desenhar_texto_contornado(screen, "FUTEBOL GAME", font_titulo, (255,255,255), (0,0,0), (largura//2, 150))

            # Desenha as opções com mudança de cor no mouse
            for i, opt in enumerate(options):
                # Se o mouse estiver sobre o retângulo, muda para Amarelo, senão fica Branco
                if rects[i].collidepoint(mouse_pos):
                    cor_texto = (255, 215, 0) # Amarelo (Hover)
                else:
                    cor_texto = (255, 255, 255) # Branco (Padrão)
                
                desenhar_texto_contornado(screen, opt, font_menu, cor_texto, (0,0,0), rects[i].center)
        else:
            # Tela de Instruções (Overlay)
            overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0,0))
            instrucoes = ["COMO JOGAR", "", "P1: WASD | S: Chute", "P2: Setas | Baixo: Chute", "", "CLIQUE PARA VOLTAR"]
            for i, l in enumerate(instrucoes):
                cor = (255, 215, 0) if i == 0 else (255, 255, 255)
                desenhar_texto_contornado(screen, l, font_ajuda, cor, (0,0,0), (largura//2, 150 + i*50))

        pygame.display.flip()
        clock.tick(60)