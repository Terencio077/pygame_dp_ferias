import pygame
import sys
import os
from config import *
import musicas
# Importe a biblioteca de vídeo
from pygame_video import Video

# ... (restante do código anterior)

def tela_vitoria(screen, clock, vencedor):
    largura, altura = screen.get_size()
    fonte_nome = "impact"
    font_titulo = pygame.font.SysFont(fonte_nome, 90)
    font_placar = pygame.font.SysFont(fonte_nome, 110)
    font_menu = pygame.font.SysFont(fonte_nome, 55)
    options = ["REINICIAR", "SAIR"]
    
    # Carrega o vídeo da vitoria
    caminho_video = os.path.join('assets_futebol', 'vitoria.mp4')
    video = Video(caminho_video)
    
    # Redimensiona o vídeo para ocupar a tela (ou parte dela)
    video.set_size((largura, altura))
    
    # IMPORTANTE: Silencia o áudio do vídeo para manter a sua música original
    video.mute()
    
    # Inicia a reprodução
    video.play(loop=True)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        rects = []
        for i in range(len(options)):
            r = pygame.Rect(0, 0, 350, 60)
            r.center = (largura // 2, 400 + (i * 90))
            rects.append(r)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.stop() # Para o vídeo antes de sair
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, r in enumerate(rects):
                    if r.collidepoint(mouse_pos):
                        if i == 0: 
                            video.stop() # Para o vídeo ao reiniciar
                            return "REINICIAR"
                        elif i == 1: 
                            video.stop()
                            pygame.quit(); sys.exit()

        # Desenha o frame atual do vídeo como fundo
        video.draw_to(screen, (0, 0))
        
        # Desenha os textos por cima do vídeo
        cor_v = (60, 140, 220) if vencedor == "Azul" else (220, 60, 60)
        desenhar_texto_contornado(screen, "VENCEDOR:", font_titulo, (255,255,255), (0,0,0), (largura//2, 120))
        desenhar_texto_contornado(screen, vencedor.upper(), font_placar, cor_v, (0,0,0), (largura//2, 230))
        
        for i, opt in enumerate(options):
            cor = (255, 215, 0) if rects[i].collidepoint(mouse_pos) else (255, 255, 255)
            desenhar_texto_contornado(screen, opt, font_menu, cor, (0,0,0), rects[i].center)
            
        pygame.display.flip()
        clock.tick(60)