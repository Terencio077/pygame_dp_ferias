import pygame
import os
import math
import random
from config import *

def try_load_image(name):
    paths = [name, os.path.join('assets', name), os.path.join('assets_futebol', name)]
    for p in paths:
        try:
            return pygame.image.load(p)
        except Exception:
            continue
    return None

def circle_collision(player, ball):
    # Ajuste do centro de colisão da cabeça: 
    # Como player.y agora é o pé, a cabeça está cerca de 60-70 pixels acima.
    head_center_y = player.y - 65 
    
    dx = ball.x - player.x
    dy = ball.y - head_center_y
    dist = math.hypot(dx, dy)
    min_dist = player.head_radius + ball.r

    if dist < min_dist and dist > 0.1:
        overlap = min_dist - dist
        nx = dx / dist
        ny = dy / dist

        push_distance = max(overlap * 2.0 + 5, player.head_radius * 0.3)
        ball.x += nx * push_distance
        ball.y += ny * push_distance

        attempts = 0
        while math.hypot(ball.x - player.x, ball.y - head_center_y) < min_dist * 1.05 and attempts < 10:
            ball.x += nx * 2
            ball.y += ny * 2
            attempts += 1

        rel_vel_norm = (ball.vx - player.vx) * nx + (ball.vy - player.vy) * ny
        if rel_vel_norm < 0:
            e = PLAYER_BOUNCE * 1.2
            impulse = -(1 + e) * rel_vel_norm * 0.6
            ball.vx += impulse * nx
            ball.vy += impulse * ny

        ball.vx += player.vx * 0.08
        ball.vy += player.vy * 0.08

def check_goal(ball, players):
    # Ajuste da área do gol para o novo GROUND_Y
    if ball.x - ball.r <= 10 and GROUND_Y - 115 < ball.y < GROUND_Y:
        return 'right'
    if ball.x + ball.r >= WIDTH - 10 and GROUND_Y - 115 < ball.y < GROUND_Y:
        return 'left'
    return None

def reset_positions(ball, p1, p2):
    # A bola começa no centro
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2 - 30
    ball.vx, ball.vy = random.choice([-3, 3]), -4
    
    # AJUSTE PRINCIPAL:
    # Os jogadores agora usam o GROUND_Y diretamente, pois o desenho (blit) 
    # utiliza o midbottom como referência (o pé toca o chão).
    p1.x, p1.y = WIDTH * 0.25, GROUND_Y
    p2.x, p2.y = WIDTH * 0.75, GROUND_Y
    
    p1.vx = p1.vy = p2.vx = p2.vy = 0