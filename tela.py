# tela.py
import pygame
import sys

def tela_inicial(screen, clock, bg_image_game=None):
    largura, altura = screen.get_size()
    
    # Fontes
    font_title = pygame.font.SysFont("impact", 90)
    font_option = pygame.font.SysFont("verdana", 35, bold=True)
    font_help = pygame.font.SysFont("verdana", 22)

    options = ["JOGAR", "CONFIGURAÇÃO DO JOGO", "SAIR"]
    selecionado = 0
    mostrar_ajuda = False

    # Preparar a imagem de fundo para garantir que ela cubra a tela do menu
    background = None
    if bg_image_game:
        background = pygame.transform.scale(bg_image_game, (largura, altura))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Criar áreas de clique dinâmicas para as opções
        rects = []
        for i in range(len(options)):
            # Retângulo invisível centralizado para detecção de colisão
            r = pygame.Rect(0, 0, 500, 60)
            r.center = (largura // 2, altura // 2 + (i * 80))
            rects.append(r)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if not mostrar_ajuda:
                # Navegação por Teclado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selecionado = (selecionado + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selecionado = (selecionado - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selecionado == 0: return # Inicia o jogo
                        elif selecionado == 1: mostrar_ajuda = True
                        elif selecionado == 2: pygame.quit(); sys.exit()
                
                # Detecção de Clique do Mouse
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, r in enumerate(rects):
                        if r.collidepoint(mouse_pos):
                            if i == 0: return
                            elif i == 1: mostrar_ajuda = True
                            elif i == 2: pygame.quit(); sys.exit()
                
                # Highlight ao passar o mouse
                for i, r in enumerate(rects):
                    if r.collidepoint(mouse_pos):
                        selecionado = i
            else:
                # Sair da tela de Configuração
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    mostrar_ajuda = False

        # --- RENDERIZAÇÃO ---
        
        # 1. Desenhar Fundo (Prioridade total para a imagem do jogo)
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((40, 180, 60)) # Verde caso a imagem falhe

        if not mostrar_ajuda:
            # 2. Título "FUTEBOL" com sombra para melhor leitura
            title_surf = font_title.render("FUTEBOL", True, (255, 255, 255))
            shadow = font_title.render("FUTEBOL", True, (0, 0, 0))
            screen.blit(shadow, (largura//2 - title_surf.get_width()//2 + 5, 105))
            screen.blit(title_surf, (largura//2 - title_surf.get_width()//2, 100))

            # 3. Desenhar Opções centralizadas
            for i, opt in enumerate(options):
                # Cor amarela se selecionado (mesmo estilo do seu código principal)
                cor = (240, 200, 30) if i == selecionado else (255, 255, 255)
                txt_surf = font_option.render(opt, True, cor)
                txt_rect = txt_surf.get_rect(center=rects[i].center)
                screen.blit(txt_surf, txt_rect)
        else:
            # 4. Tela de Configuração (Instruções de como jogar)
            overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 210)) # Fundo escurecido semi-transparente
            screen.blit(overlay, (0,0))
            
            ajuda_texto = [
                "COMO JOGAR",
                "",
                "Jogador Azul: W, A, D (Movimento) | S (Chute) | X (Lob)",
                "Jogador Vermelho: Setas (Movimento) | Seta Baixo (Chute) | M (Lob)",
                "",
                "Pressione qualquer tecla para voltar ao menu"
            ]
            for i, linha in enumerate(ajuda_texto):
                cor_linha = (240, 200, 30) if i == 0 else (255, 255, 255)
                txt = font_help.render(linha, True, cor_linha)
                screen.blit(txt, (largura//2 - txt.get_width()//2, 160 + i * 50))

        pygame.display.flip()
        clock.tick(60)