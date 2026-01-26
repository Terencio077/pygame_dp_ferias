import pygame
import os
import math
import random
from config import *

def try_load_image(name):
    # Usa o diretório do script como base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [
        name,
        os.path.join('assets', name),
        os.path.join('assets_futebol', name),
        os.path.join(script_dir, 'assets', name),
        os.path.join(script_dir, 'assets_futebol', name)
    ]
    for p in paths:
        try:
            if os.path.exists(p):
                img = pygame.image.load(p)
                return img
        except Exception as e:
            continue
    return None

def circle_collision(player, ball):
    dx = ball.x - player.x
    dy = ball.y - (player.y - player.head_radius * 0.7)
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
        while math.hypot(ball.x - player.x, ball.y - (player.y - 6)) < min_dist * 1.05 and attempts < 10:
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
    if ball.x - ball.r <= 10 and GROUND_Y - 115 < ball.y < GROUND_Y:
        return 'right'
    if ball.x + ball.r >= WIDTH - 10 and GROUND_Y - 115 < ball.y < GROUND_Y:
        return 'left'
    return None

def reset_positions(ball, p1, p2):
    ball.x = WIDTH // 2
    ball.y = HEIGHT // 2 - 30
    ball.vx = random.choice([-3, 3])
    ball.vy = -4
    p1.x = WIDTH * 0.25
    p1.y = GROUND_Y - p1.head_radius
    p1.vx = p1.vy = 0
    p2.x = WIDTH * 0.75
    p2.y = GROUND_Y - p2.head_radius
    p2.vx = p2.vy = 0