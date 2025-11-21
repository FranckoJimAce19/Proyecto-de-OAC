import pygame
import sys
from modules.utils import cfg

def draw_button(screen, number, text, rect, is_hovered=False):
    bg_color = (255, 200, 50) if is_hovered else (200, 200, 200)
    border_color = (100, 100, 100)
    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)
    font = pygame.font.Font(cfg.FONTPATH, 28)
    label = f"{number}. {text}"
    txt_surf = font.render(label, True, (0, 0, 0))
    txt_rect = txt_surf.get_rect(center=rect.center)
    screen.blit(txt_surf, txt_rect)

def showStartInterface(screen, screensize):
    for y in range(screensize[1]):
        ratio = y / screensize[1]
        shade = int(240 - ratio * 20)
        pygame.draw.line(screen, (shade, shade, shade), (0, y), (screensize[0], y))
    title_font = pygame.font.Font(cfg.FONTPATH, 100)
    title_surf = title_font.render("SKIER", True, (255, 255, 100))
    title_rect = title_surf.get_rect(center=(screensize[0] // 2, screensize[1] // 5))
    shadow = title_font.render("SKIER", True, (50, 50, 50))
    screen.blit(shadow, title_rect.move(5, 5))
    screen.blit(title_surf, title_rect)
    btn_w, btn_h = 400, 70
    start_rect = pygame.Rect(0, 0, btn_w, btn_h)
    start_rect.center = (screensize[0] // 2, screensize[1] // 2 - 40)
    scores_rect = pygame.Rect(0, 0, btn_w, btn_h)
    scores_rect.center = (screensize[0] // 2, screensize[1] // 2 + 40)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        start_hover = start_rect.collidepoint(mouse_pos)
        scores_hover = scores_rect.collidepoint(mouse_pos)
        for y in range(screensize[1]):
            ratio = y / screensize[1]
            shade = int(240 - ratio * 20)
            pygame.draw.line(screen, (shade, shade, shade), (0, y), (screensize[0], y))
        screen.blit(shadow, title_rect.move(5, 5))
        screen.blit(title_surf, title_rect)
        draw_button(screen, "1", "INICIAR JUEGO", start_rect, start_hover)
        draw_button(screen, "2", "VER PUNTUACIONES", scores_rect, scores_hover)
        hint_font = pygame.font.Font(cfg.FONTPATH, 20)
        hint = hint_font.render("ESC para salir", True, (0, 0, 0))
        hint_rect = hint.get_rect(center=(screensize[0] // 2, screensize[1] - 40))
        screen.blit(hint, hint_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    return "start"
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    return "scores"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return "start"
                if scores_rect.collidepoint(event.pos):
                    return "scores"