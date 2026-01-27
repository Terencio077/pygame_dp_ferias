import pygame
import os
import math
import random
from config import *

def try_load_image(name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [name, os.path.join('assets_futebol', name), os.path.join(script_dir, 'assets_futebol', name)]
    for p in paths:
        try:
            if os.path.exists(p): return pygame.image.load(p)
        except: continue
    return None

def circle_collision(player, ball):
    dx, dy = ball.x - player.x, ball.y - (player.y - player.head_radius * 0.7)
    dist = math.hypot(dx, dy)
    min_dist = player.head_radius + ball.r
    if dist < min_dist and dist > 0.1:
        nx, ny = dx / dist, dy / dist
        ball.x += nx * (min_dist - dist + 5)
        ball.y += ny * (min_dist - dist + 5)
        rel_vel = (ball.vx - player.vx) * nx + (ball.vy - player.vy) * ny
        if rel_vel < 0:
            impulse = -(1 + PLAYER_BOUNCE * 1.2) * rel_vel * 0.6
            ball.vx += impulse * nx
            ball.vy += impulse * ny

def check_goal(ball, players):
    if ball.x - ball.r <= 10 and 485 < ball.y < GROUND_Y: return 'right'
    if ball.x + ball.r >= WIDTH - 10 and 485 < ball.y < GROUND_Y: return 'left'
    return None

def reset_positions(ball, p1, p2):
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2 - 30
    ball.vx, ball.vy = random.choice([-3, 3]), -4
    p1.x, p1.vx, p1.vy = WIDTH * 0.25, 0, 0
    p2.x, p2.vx, p2.vy = WIDTH * 0.75, 0, 0
    # GARANTE QUE AO RESETAR ELES ESTEJAM NO CHÃO
    p1.y = GROUND_Y - p1.head_radius
    p2.y = GROUND_Y - p2.head_radius