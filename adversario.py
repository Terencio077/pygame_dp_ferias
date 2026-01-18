import math
import random

def calcular_movimento_ia(player_ia, ball):
    # Dicionário que simula as teclas pressionadas para o Player 2
    fake_keys = {
        player_ia.controls['left']: False,
        player_ia.controls['right']: False,
        player_ia.controls['jump']: False,
        player_ia.controls['kick']: False,
        player_ia.controls['lob']: False
    }

    # 1. Movimentação Horizontal: O oponente segue a bola
    # Ele tenta manter uma pequena distância para não ficar exatamente "em cima" do centro da bola
    if ball.x < player_ia.x - 25:
        fake_keys[player_ia.controls['left']] = True
    elif ball.x > player_ia.x + 25:
        fake_keys[player_ia.controls['right']] = True

    # 2. Lógica de Pulo: Pula se a bola estiver alta e vindo em sua direção
    if ball.y < player_ia.y - 70 and abs(ball.x - player_ia.x) < 120:
        fake_keys[player_ia.controls['jump']] = True

    # [cite_start]3. Lógica de Chute e Cabeceio: Se a bola estiver no alcance (distância euclidiana) [cite: 44, 53]
    dist = math.hypot(ball.x - player_ia.x, ball.y - player_ia.y)
    if dist < player_ia.head_radius + ball.r + 25:
        # Alterna entre chute normal (80%) e lob (20%) para variar o jogo
        if random.random() > 0.2:
            fake_keys[player_ia.controls['kick']] = True
        else:
            fake_keys[player_ia.controls['lob']] = True

    return fake_keys