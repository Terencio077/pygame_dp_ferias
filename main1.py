import pygame
import sys
import traceback
import importlib
from config import *
from colisoes import circle_collision, check_goal, reset_positions
from tela import tela_inicial, tela_vitoria, draw_field 

def main_loop():
    # 1. INICIALIZAÇÃO (Obrigatório antes de qualquer conversão de imagem)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Football Heads - Pygame Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 45)
    
    # inicializa assets e importa classes
    import assets
    assets.initialize_assets()
    
    # importa classes
    from assets import Ball, Player
    
    # background
    from tela import load_background
    load_background()

    from tela import BG_FIELD
    if BG_FIELD:
        import config
        config.GROUND_Y = HEIGHT - 20

    P_BLUE = assets.PLAYER_BLUE_IMG
    P_RED = assets.PLAYER_RED_IMG
    BALL_IMG = assets.BALL_IMG

    # valida imagens carregadas
    if P_BLUE is None:
        print("ERRO: Imagem do jogador azul não carregou!")
        pygame.quit()
        sys.exit()
    if P_RED is None:
        print("ERRO: Imagem do jogador vermelho não carregou!")
        pygame.quit()
        sys.exit()
    if BALL_IMG is None:
        print("ERRO: Imagem da bola não carregou!")
        pygame.quit()
        sys.exit()

    # 2. MENU INICIAL
    tela_inicial(screen, clock)
    import musicas
    musicas.load_torcida()

    TORCIDA_SOUND = musicas.TORCIDA_SOUND

    # 3. INSTANCIAÇÃO DOS OBJETOS
    ball = Ball(WIDTH // 2, HEIGHT // 2 - 50)
    p1 = Player(WIDTH * 0.25, BLUE, {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'kick': pygame.K_s, 'lob': pygame.K_x}, image=P_BLUE)
    p2 = Player(WIDTH * 0.75, RED, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'kick': pygame.K_DOWN, 'lob': pygame.K_m}, image=P_RED)

    reset_positions(ball, p1, p2)
    
    musicas.play_torcida()

    running = True
    paused = False
    goal_cooldown = 0

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Ao apertar ESC durante o jogo, volta para o menu
                    tela_inicial(screen, clock)
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            # FÍSICA E ATUALIZAÇÕES
            p1.update(keys)
            p2.update(keys)
            ball.update()

            #Detecção de ponto instantâneo ao bater na parede
            try:
                ball_radius = ball.radius
            except Exception:
                ball_radius = BALL_IMG.get_width() // 2

            # verifica colisão com as paredes laterais e pontua imediatamente
            if goal_cooldown == 0:
                if ball.x - ball.r <= 10 and 485 < ball.y < GROUND_Y:
                    p2.score += 1
                    goal_cooldown = FPS * 3
                    reset_positions(ball, p1, p2)
                elif ball.x + ball.r >= WIDTH - 10 and 485 < ball.y < GROUND_Y:
                    p1.score += 1
                    goal_cooldown = FPS * 3
                    reset_positions(ball, p1, p2)
            else:
                goal_cooldown -= 1


            ball.check_stuck_between_players(p1, p2)
            circle_collision(p1, ball)
            circle_collision(p2, ball)

            for p in [p1, p2]:
                p.try_kick(ball, keys, 'kick')
                p.try_kick(ball, keys, 'lob')
                p.try_headbutt(ball, keys, 'kick')
                p.try_headbutt(ball, keys, 'lob')

        # RENDERIZAÇÃO
        draw_field(screen)
        p1.draw(screen)
        p2.draw(screen)
        ball.draw(screen)

        # Placar com tamanho aumentado e cor branca
        score_text = font.render(f"{p1.score}  -  {p2.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 18))

        if paused:
            pause_txt = font.render("PAUSADO", True, WHITE)
            screen.blit(pause_txt, (WIDTH // 2 - pause_txt.get_width() // 2, HEIGHT // 2 - pause_txt.get_height() // 2))

        # VERIFICAÇÃO DE VITÓRIA
        if p1.score >= SCORE_TO_WIN or p2.score >= SCORE_TO_WIN:
            musicas.stop_torcida()
            
            vencedor = "Azul" if p1.score > p2.score else "Vermelho"
            
            # Chama a sua TELA DE VITÓRIA
            resultado = tela_vitoria(screen, clock, vencedor)
            
            if resultado == "REINICIAR":
                p1.score = 0
                p2.score = 0
                reset_positions(ball, p1, p2)

                musicas.play_torcida()
            else:
                running = False
        
        pygame.display.flip()

# EXECUÇÃO COM TRATAMENTO DE ERRO
if __name__ == "__main__":
    try:
        main_loop()
    except Exception:
        print("\n--- ERRO ENCONTRADO ---")
        traceback.print_exc()
        input("\nPressione Enter para fechar...")
    finally:
        pygame.quit()
        sys.exit()
