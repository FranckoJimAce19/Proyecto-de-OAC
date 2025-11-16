import pygame, sys
from modules.ui.name_input import get_player_name
from modules.utils.files  import save_score
from modules.utils import cfg

def showGameOver(screen, screensize, score):
    name = get_player_name(screen, screensize)
    save_score(name, score)
    font = pygame.font.Font(cfg.FONTPATH, 40)
    screen.fill((255,255,255))
    txt = font.render(f"Fin del juego - Puntuación: {score}", True, (255,0,0))
    trect = txt.get_rect(center=(screensize[0]//2, 200))
    restart = font.render("R - Reiniciar", True, (0,0,255))
    rrect = restart.get_rect(center=(screensize[0]//2, 300))
    exit = font.render("ESC - Salir", True, (0,0,0))
    erect = exit.get_rect(center=(screensize[0]//2, 380))
    screen.blit(txt, trect)
    screen.blit(restart, rrect)
    screen.blit(exit, erect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
