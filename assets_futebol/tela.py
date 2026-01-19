import pygame
import sys

def tela_inicial(screen, clock):
    font_titulo = pygame.font.SysFont("arial", 48, bold=True)
    font_texto = pygame.font.SysFont("arial", 24)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER começa
                    return
                if event.key == pygame.K_ESCAPE:  # ESC sai
                    pygame.quit()
                    sys.exit()

        screen.fill((30, 30, 30))

        # Título
        titulo = font_titulo.render("JOGO DE FUTEBOL", True, (255, 255, 255))
        screen.blit(
            titulo,
            (screen.get_width() // 2 - titulo.get_width() // 2, 100)
        )

        # Textos do menu
        textos = [
            "Vermelho: Jogador",
            "Azul: IA (Adversário)",
            "",
            "Setas: mover e pular",
            "Espaço: chutar",
            "",
            "ENTER para começar",
            "ESC para sair"
        ]

        y = 220
        for linha in textos:
            txt = font_texto.render(linha, True, (200, 200, 200))
            screen.blit(
                txt,
                (screen.get_width() // 2 - txt.get_width() // 2, y)
            )
            y += 30

        pygame.display.flip()
