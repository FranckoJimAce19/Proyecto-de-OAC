import pygame
from modules.utils import cfg
from modules.utils.files import load_scores

def wait_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                return

def show_scores(screen, screensize):
    screen.fill((255,255,255))
    title_font = pygame.font.Font(cfg.FONTPATH, 60)
    score_font = pygame.font.Font(cfg.FONTPATH, 32)
    title = title_font.render("Puntuaciones", True, (0,0,255))
    trect = title.get_rect(center=(screensize[0]//2, 80))
    screen.blit(title, trect)
    scores = load_scores()
    y = 150
    if not scores:
        text = score_font.render("No hay puntuaciones aún", True, (0,0,0))
        rect = text.get_rect(center=(screensize[0]//2, y))
        screen.blit(text, rect)
    else:
        for i, (name, s) in enumerate(scores):
            txt = score_font.render(f"{i+1}. {name} - {s}", True, (0,0,0))
            rect = txt.get_rect(center=(screensize[0]//2, y))
            screen.blit(txt, rect)
            y += 45
    exit_text = score_font.render("Presiona una tecla para regresar", True, (255,0,0))
    ex_rect = exit_text.get_rect(center=(screensize[0]//2, screensize[1]-60))
    screen.blit(exit_text, ex_rect)
    pygame.display.update()
    wait_key()