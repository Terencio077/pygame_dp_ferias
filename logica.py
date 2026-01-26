import pygame
import sys
from config import *
from colisoes import try_load_image

_bg = try_load_image("plano de fundo.png")
BG_IMAGE = pygame.transform.scale(_bg, (WIDTH, HEIGHT)).convert() if _bg else None
if BG_IMAGE: GROUND_Y = HEIGHT - 20

def draw_field(surf):
    if BG_IMAGE: surf.blit(BG_IMAGE, (0, 0))
    else: surf.fill(GREEN)

def tela_inicial(screen, clock, font):
    esperando = True
    while esperando:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if event.key in (pygame.K_RETURN, pygame.K_SPACE): esperando = False
        
        draw_field(screen)
        texts = [
            ("FOOTBALL HEADS", WHITE, -120),
            ("Pressione ESPAÇO ou ENTER para jogar", YELLOW, -70),
            ("Azul: A/D move, W pula, S chuta, X lob", WHITE, 10),
            ("Vermelho: ←/→ move, ↑ pula, ↓ chuta, M lob", WHITE, 45),
            ("ESC para sair", WHITE, 90)
        ]
        for t, c, y_off in texts:
            img = font.render(t, True, c)
            screen.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 + y_off))
        pygame.display.flip()