import pygame
import math
import random
from config import *

from colisoes import try_load_image

# Global variables for loaded images
PLAYER_BLUE_IMG = None
PLAYER_RED_IMG = None
PLAYER_BLUE_LEG_LEFT = None
PLAYER_BLUE_LEG_RIGHT = None
PLAYER_RED_LEG_LEFT = None
PLAYER_RED_LEG_RIGHT = None
BALL_IMG = None

def initialize_assets():
    """Initialize all image assets. Call this after pygame display is created."""
    global PLAYER_BLUE_IMG, PLAYER_RED_IMG, PLAYER_BLUE_LEG_LEFT, PLAYER_BLUE_LEG_RIGHT
    global PLAYER_RED_LEG_LEFT, PLAYER_RED_LEG_RIGHT, BALL_IMG
    
    _p_blue = try_load_image("Player Blu.png")
    print(f"Player Blue: {_p_blue is not None}")
    if _p_blue:
        PLAYER_BLUE_IMG = pygame.transform.scale(_p_blue.convert_alpha(), (int(_p_blue.get_width() * (88 / _p_blue.get_height())), 88))
    
    _p_red = try_load_image("Player Red.png")
    print(f"Player Red: {_p_red is not None}")
    if _p_red:
        PLAYER_RED_IMG = pygame.transform.scale(_p_red.convert_alpha(), (int(_p_red.get_width() * (88 / _p_red.get_height())), 88))
    
    _p_b_left = try_load_image("Player blu left leg.png")
    print(f"Player Blue Left Leg: {_p_b_left is not None}")
    PLAYER_BLUE_LEG_LEFT = pygame.transform.scale(_p_b_left.convert_alpha(), (_p_b_left.get_width(), _p_b_left.get_height())) if _p_b_left else None
    _p_b_right = try_load_image("Player blu right leg.png")
    print(f"Player Blue Right Leg: {_p_b_right is not None}")
    PLAYER_BLUE_LEG_RIGHT = pygame.transform.scale(_p_b_right.convert_alpha(), (_p_b_right.get_width(), _p_b_right.get_height())) if _p_b_right else (pygame.transform.flip(PLAYER_BLUE_LEG_LEFT, True, False) if PLAYER_BLUE_LEG_LEFT else None)
    
    _p_r_left = try_load_image("Player red left leg.png")
    print(f"Player Red Left Leg: {_p_r_left is not None}")
    PLAYER_RED_LEG_LEFT = pygame.transform.scale(_p_r_left.convert_alpha(), (_p_r_left.get_width(), _p_r_left.get_height())) if _p_r_left else None
    PLAYER_RED_LEG_RIGHT = pygame.transform.flip(PLAYER_RED_LEG_LEFT, True, False) if PLAYER_RED_LEG_LEFT else None
    
    _ball_img_raw = (try_load_image("football.png") or try_load_image("BALL_IMG.png") or 
                     try_load_image("ball.png") or try_load_image("Ball.png") or 
                     try_load_image("bola.png") or try_load_image("Bola.png") or 
                     try_load_image("BALL.png") or try_load_image("BOLA.png") or 
                     try_load_image("ball.jpg") or try_load_image("Ball.jpg") or 
                     try_load_image("BALL_IMG.jpg"))
    print(f"Ball Image (trying multiple variations): {_ball_img_raw is not None}")
    if _ball_img_raw:
        BALL_IMG = pygame.transform.smoothscale(_ball_img_raw.convert_alpha(), (38, 38))
    else:
        print("AVISO: Nenhuma imagem de bola foi encontrada!")
        print(f"  - Procurou por: football.png, BALL_IMG.png e outras variações")
        print(f"  - Verifique o nome exato do arquivo na pasta 'assets_futebol'")

class Ball:
    def __init__(self, x, y, r=18):
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0.0
        self.vy = 0.0

    def update(self):
        self.vy += GRAVITY * BALL_GRAVITY_MULT
        self.x += self.vx
        self.y += self.vy
        if self.y - self.r < -BALL_TOP_MARGIN:
            self.y = -BALL_TOP_MARGIN + self.r
            if self.vy < 0: self.vy = 0.0
        if self.y + self.r > GROUND_Y:
            self.y = GROUND_Y - self.r
            self.vy = -abs(self.vy) * BALL_BOUNCE
            self.vx *= BALL_FRICTION
        if self.x - self.r < 0:
            self.x = self.r
            self.vx = abs(self.vx) * 0.8
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.vx = -abs(self.vx) * 0.8
        if self.y - self.r < 0:
            self.y = self.r
            self.vy = abs(self.vy) * BALL_BOUNCE

        crossbar_y, goal_zone_width, crossbar_thickness = GROUND_Y - 110, 160, 50
        if self.y - self.r <= crossbar_y and (self.x < goal_zone_width or self.x > WIDTH - goal_zone_width):
            if self.y - self.r > crossbar_y - crossbar_thickness:
                self.y = crossbar_y + self.r
                self.vy = abs(self.vy) * BALL_BOUNCE * 1.2
                self.vx *= 0.75

        self.vx *= BALL_FRICTION
        if abs(self.vx) < 0.01: self.vx = 0.0
        if abs(self.vy) < 0.01 and self.y + self.r >= GROUND_Y - 0.5: self.vy = 0.0
        speed = math.hypot(self.vx, self.vy)
        if speed > MAX_BALL_SPEED:
            scale = MAX_BALL_SPEED / speed
            self.vx *= scale
            self.vy *= scale

    def check_stuck_between_players(self, p1, p2):
        left_player = p1 if p1.x < p2.x else p2
        right_player = p2 if p1.x < p2.x else p1
        if left_player.x < self.x < right_player.x:
            if abs(self.x - left_player.x) < left_player.head_radius + 30 and abs(self.x - right_player.x) < right_player.head_radius + 30:
                self.y = min(left_player.y, right_player.y) - 60
                self.vy, self.vx = -25.0, (8.0 if random.random() > 0.5 else -8.0) + random.uniform(-3, 3)

    def draw(self, surf):
        global BALL_IMG
        if BALL_IMG:
            rect = BALL_IMG.get_rect(center=(int(self.x), int(self.y)))
            surf.blit(BALL_IMG, rect)

class Player:
    def __init__(self, x, color, controls, image=None):
        self.x, self.y = x, GROUND_Y - 40
        self.vx, self.vy = 0.0, 0.0
        self.radius, self.head_radius = 18, 23
        self.color, self.speed = color, 5.0
        self.on_ground, self.facing = True, 1
        self.controls, self.score = controls, 0
        self.kick_cooldown, self.image = 0, image
        self.kick_timer, self.kick_duration, self.kick_side = 0, 12, None
        self.front_leg_scale, self.leg_phase = 4.8, 0.0

    def update(self, keys):
        moving_left, moving_right = keys[self.controls['left']], keys[self.controls['right']]
        if moving_left and not moving_right: self.vx, self.facing = -self.speed, -1
        elif moving_right and not moving_left: self.vx, self.facing = self.speed, 1
        else:
            self.vx *= 0.85
            if abs(self.vx) < 0.1: self.vx = 0.0
        if keys[self.controls['jump']] and self.on_ground:
            self.vy, self.on_ground = -14.5, False
        self.vy += GRAVITY * 0.9
        self.x += self.vx
        self.y += self.vy
        if self.y + self.head_radius > GROUND_Y:
            self.y, self.vy, self.on_ground = GROUND_Y - self.head_radius, 0.0, True
        self.x = max(10, min(WIDTH - 10, self.x))
        if self.kick_cooldown > 0: self.kick_cooldown -= 1
        if self.kick_timer > 0:
            self.kick_timer -= 1
            self.leg_phase += 0.3
        else: self.kick_side = None

    def draw(self, surf):
        global PLAYER_BLUE_LEG_LEFT, PLAYER_BLUE_LEG_RIGHT, PLAYER_RED_LEG_LEFT, PLAYER_RED_LEG_RIGHT
        if self.image:
            img = pygame.transform.flip(self.image, True, False) if self.facing == -1 else self.image
            rect = img.get_rect(midbottom=(int(self.x), int(self.y + self.head_radius)))
            surf.blit(img, rect)
            hip_x, hip_y = rect.centerx, rect.bottom - int(self.head_radius * 0.2)
            
            if self.color == BLUE:
                front_img = PLAYER_BLUE_LEG_RIGHT if (self.facing == 1) else PLAYER_BLUE_LEG_LEFT
            else:
                front_img = PLAYER_RED_LEG_RIGHT if (self.facing == 1) else PLAYER_RED_LEG_LEFT
            
            kick_ang = -math.sin(((self.kick_duration - self.kick_timer) / max(1, self.kick_duration)) * math.pi) * 90 if self.kick_timer > 0 else 0
            if front_img:
                img_blit = pygame.transform.flip(front_img, True, False) if self.facing == -1 else front_img
                rot = pygame.transform.rotozoom(img_blit, -kick_ang * self.facing, self.front_leg_scale)
                surf.blit(rot, rot.get_rect(center=(hip_x + int(self.head_radius * 0.95) * self.facing, hip_y + int(self.head_radius * 0.05))))
            return

    def try_kick(self, ball, keys, kick_type='kick'):
        if kick_type not in self.controls or not keys[self.controls[kick_type]]: return
        if self.kick_cooldown == 0:
            self.kick_timer, self.kick_side, self.kick_cooldown = self.kick_duration, ('right' if self.facing == 1 else 'left'), 18
            dx, dy = ball.x - self.x, ball.y - self.y
            dist = math.hypot(dx, dy)
            if dist < self.head_radius + ball.r + 15:
                force = 16.0 if kick_type == 'lob' else 18.0
                nx, ny = dx/(dist+1e-6), dy/(dist+1e-6)
                ball.vx += nx * force + self.facing * (2.0 if kick_type == 'lob' else 4.0)
                ball.vy += ny * force - (16.0 if kick_type == 'lob' else 3.0)

    def try_headbutt(self, ball, keys, kick_type='kick'):
        if kick_type not in self.controls or not keys[self.controls[kick_type]]: return
        dx, dy = ball.x - self.x, ball.y - (self.y - self.head_radius * 0.5)
        dist = math.hypot(dx, dy)
        if dy < -5 and dist < self.head_radius + ball.r + 12 and self.kick_cooldown == 0:
            self.kick_timer, self.kick_side, self.kick_cooldown = self.kick_duration, ('right' if self.facing == 1 else 'left'), 18
            nx, ny = dx/(dist+1e-6), dy/(dist+1e-6)
            ball.vx += nx * 17.0 + self.facing * 3.0
            ball.vy += ny * 17.0 - (10.0 if kick_type == 'lob' else 5.0)