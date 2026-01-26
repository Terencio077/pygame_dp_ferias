import pygame
import sys
from config import *
from utils import circle_collision, check_goal, reset_positions
from sprites import Ball, Player, PLAYER_BLUE_IMG, PLAYER_RED_IMG
from game_logic import draw_field, tela_inicial

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Heads - Pygame Prototype")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# Inicialização
ball = Ball(WIDTH // 2, HEIGHT // 2 - 50)
p1 = Player(WIDTH * 0.25, BLUE, {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'kick': pygame.K_s, 'lob': pygame.K_x}, image=PLAYER_BLUE_IMG)
p2 = Player(WIDTH * 0.75, RED, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'kick': pygame.K_DOWN, 'lob': pygame.K_m}, image=PLAYER_RED_IMG)

reset_positions(ball, p1, p2)
tela_inicial(screen, clock, font)

running, paused, goal_cooldown = True, False, 0

while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if event.key == pygame.K_SPACE: paused = not paused

    if not paused:
        p1.update(keys)
        p2.update(keys)
        ball.update()
        ball.check_stuck_between_players(p1, p2)
        circle_collision(p1, ball)
        circle_collision(p2, ball)

        for p in [p1, p2]:
            p.try_kick(ball, keys, 'kick')
            p.try_kick(ball, keys, 'lob')
            p.try_headbutt(ball, keys, 'kick')
            p.try_headbutt(ball, keys, 'lob')

        if goal_cooldown == 0:
            scorer = check_goal(ball, (p1, p2))
            if scorer:
                if scorer == 'right': p2.score += 1
                else: p1.score += 1
                goal_cooldown = FPS * 3
                reset_positions(ball, p1, p2)
        else: goal_cooldown -= 1

    draw_field(screen)
    p1.draw(screen)
    p2.draw(screen)
    ball.draw(screen)

    score_text = font.render(f"{p1.score}  -  {p2.score}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 18))

    if paused:
        pause_txt = font.render("PAUSADO", True, BLACK)
        screen.blit(pause_txt, (WIDTH // 2 - pause_txt.get_width() // 2, HEIGHT // 2 - 20))

    if p1.score >= SCORE_TO_WIN or p2.score >= SCORE_TO_WIN:
        winner = "Azul" if p1.score > p2.score else "Vermelho"
        end_txt = font.render(f"{winner} venceu! Aperte ESC para sair.", True, BLACK)
        screen.blit(end_txt, (WIDTH // 2 - end_txt.get_width() // 2, HEIGHT // 2 + 40))
        running = False # Simplesmente para o loop e espera o flip final
    
    pygame.display.flip()

# Espera o usuário fechar após vitória
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit(); sys.exit()