import pygame
import os

# Global sound variables
WAKAWAKA_SOUND = None
TORCIDA_SOUND = None

def load_wakawaka():
    """Load wakawaka sound effect for menu."""
    global WAKAWAKA_SOUND
    audio_files = ['wakawaka.mp3', 'wakawaka.wav', 'wakawaka.ogg', 
                   'Wakawaka.mp3', 'Wakawaka.wav', 'Wakawaka.ogg',
                   'wakawaka.flac', 'Wakawaka.flac']
    
    for filename in audio_files:
        caminho = os.path.join('assets_futebol', filename)
        try:
            if os.path.exists(caminho):
                WAKAWAKA_SOUND = pygame.mixer.Sound(caminho)
                print(f"Wakawaka sound loaded: {filename}")
                return True
        except Exception as e:
            print(f"Failed to load {filename} as Sound: {e}")
            if filename.lower().endswith('.mp3'):
                try:
                    pygame.mixer.music.load(caminho)
                    WAKAWAKA_SOUND = 'music'
                    print(f"Wakawaka music loaded: {filename}")
                    return True
                except Exception as e2:
                    print(f"Failed to load {filename} as music: {e2}")
    
    print("AVISO: Som wakawaka não encontrado ou corrompido!")
    return False

def load_torcida():
    """Load crowd/torcida sound effect for gameplay."""
    global TORCIDA_SOUND
    audio_files = ['som torcida.wav', 'som torcida.ogg', 'som_torcida.wav', 'som_torcida.ogg',
                   'torcida.wav', 'torcida.ogg', 'Torcida.wav', 'Torcida.ogg']
    
    for filename in audio_files:
        caminho = os.path.join('assets_futebol', filename)
        try:
            if os.path.exists(caminho):
                TORCIDA_SOUND = pygame.mixer.Sound(caminho)
                print(f"Torcida sound loaded: {filename}")
                return True
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
    
    print("AVISO: Som de torcida não encontrado!")
    return False

def play_wakawaka():
    """Play wakawaka sound on loop."""
    if WAKAWAKA_SOUND:
        if WAKAWAKA_SOUND == 'music':
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
        else:
            WAKAWAKA_SOUND.set_volume(0.7)
            WAKAWAKA_SOUND.play(-1)

def stop_wakawaka():
    """Stop wakawaka sound."""
    if WAKAWAKA_SOUND:
        if WAKAWAKA_SOUND == 'music':
            pygame.mixer.music.stop()
        else:
            WAKAWAKA_SOUND.stop()

def play_torcida():
    """Play crowd sound on loop with reduced volume."""
    if TORCIDA_SOUND:
        TORCIDA_SOUND.set_volume(0.2)
        TORCIDA_SOUND.play(-1)

def stop_torcida():
    """Stop crowd sound."""
    if TORCIDA_SOUND:
        TORCIDA_SOUND.stop()
