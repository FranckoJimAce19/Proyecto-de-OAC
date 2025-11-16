import pygame
from modules.utils import cfg

def showScore(screen, score, lives, speed, speed_bonus=0.0, vel=0.0, pos=(10, 10)):
    font = pygame.font.Font(cfg.FONTPATH, 28)
    base_text = f"Score: {score}  Vidas: {lives}  Velocidad: {vel:.2f}"
    if 0 < speed_bonus < 1:
        percent = int(speed_bonus * 100)
        base_text += f" (+{percent}% bonus)"
    score_surface = font.render(base_text, True, (0, 0, 0))
    screen.blit(score_surface, pos)


def updateFrame(screen, obstacles, skier, score, lives, speed, speed_bonus=0, vel=0.0):
    screen.fill((255, 255, 255))
    try:
        obstacles.draw(screen)
    except Exception:
        pass
    screen.blit(skier.image, skier.rect)
    showScore(screen, score, lives, speed, speed_bonus, vel)
    pygame.display.update()