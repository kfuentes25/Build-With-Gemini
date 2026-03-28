import pygame, math

class Animator:
    @staticmethod
    def get_bob(speed=0.005, amp=10):
        return math.sin(pygame.time.get_ticks() * speed) * amp

    @staticmethod
    def pulse_surface(surf):
        alpha = int((math.sin(pygame.time.get_ticks() * 0.01) + 1) * 50) + 150
        temp = surf.copy()
        temp.set_alpha(alpha)
        return temp