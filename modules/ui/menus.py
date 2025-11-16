import pygame, sys
from modules.utils import cfg

def showStartInterface(screen, screensize):
    screen.fill((255, 255, 255))
    tfont = pygame.font.Font(cfg.FONTPATH, 90)
    cfont = pygame.font.Font(cfg.FONTPATH, 36)
    title = tfont.render("SKIER", True, (255, 0, 0))
    start_text = cfont.render("1. Iniciar juego", True, (0, 0, 255))
    score_text = cfont.render("2. Ver puntuaciones", True, (0, 0, 255))
    exit_text = cfont.render("ESC para salir", True, (0, 0, 0))
    trect = title.get_rect(center=(screensize[0]//2, screensize[1]//5))
    srect = start_text.get_rect(center=(screensize[0]//2, screensize[1]//2 - 40))
    screct = score_text.get_rect(center=(screensize[0]//2, screensize[1]//2 + 10))
    exrect = exit_text.get_rect(center=(screensize[0]//2, screensize[1] - 60))
    screen.blit(title, trect)
    screen.blit(start_text, srect)
    screen.blit(score_text, screct)
    screen.blit(exit_text, exrect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start"
                elif event.key == pygame.K_2:
                    return "scores"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
