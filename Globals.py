import pygame

DeltaTime = float
Clock = None

def Updated():
    global DeltaTime
    DeltaTime = Clock.tick(120) / 1000