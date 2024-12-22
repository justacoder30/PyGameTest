import pygame
from Control.Mixer import *

def Init():
    global sounds
    sounds = {
        "coin": Sound("resource/SoundFX/coin_sound.mp3", 1),
        "attack": Sound("resource/SoundFX/attack_sound.wav", 1),
        "button": Sound("resource/SoundFX/ButtonChose_sound.wav", 1),
        "button_click": Sound("resource/SoundFX/ButtonClick_sound.wav", 1),
        "Hurt": Sound("resource/SoundFX/Hit_sound.mp3", 1),
        "landing": Sound("resource/SoundFX/landing_sound.mp3", 1),
        "WinGame": Sound("resource/SoundFX/WinGame_sound.mp3", 1),
        "LoseGame": Sound("resource/SoundFX/GameLose_sound.wav", 1),

    }
    
def PlaySound(name, volume=1):
    sounds[name].play()

def PlayMusic():
    pass
