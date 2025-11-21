import pygame
import sys
from modules.utils import cfg
from modules.utils.files import save_score
from modules.ui.name_input import get_player_name

def draw_panel(screen, rect, color=(255, 255, 255), border_color=(120, 120, 120), alpha=220):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.set_alpha(alpha)
    panel.fill(color)
    screen.blit(panel, rect.topleft)
    pygame.draw.rect(screen, border_color, rect, 2)

def showGameOver(screen, screensize, score):
    name = get_player_name(screen, screensize)
    save_score(name, score)
    for y in range(screensize[1]):
        ratio = y / screensize[1]
        shade = int(240 - ratio * 20)
        pygame.draw.line(screen, (shade, shade, shade), (0, y), (screensize[0], y))
    panel_width, panel_height = 500, 300
    panel_rect = pygame.Rect(
        (screensize[0] - panel_width) // 2,
        (screensize[1] - panel_height) // 2,
        panel_width,
        panel_height,
    )
    draw_panel(screen, panel_rect)
    title_font = pygame.font.Font(cfg.FONTPATH, 80)
    score_font = pygame.font.Font(cfg.FONTPATH, 36)
    small_font = pygame.font.Font(cfg.FONTPATH, 28)
    title_surf = title_font.render("GAME OVER", True, (200, 50, 50))
    title_rect = title_surf.get_rect(center=(screensize[0] // 2, panel_rect.top + 70))
    screen.blit(title_surf, title_rect)
    score_surf = score_font.render(f"Puntuación: {score}", True, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(screensize[0] // 2, panel_rect.top + 130))
    screen.blit(score_surf, score_rect)
    pygame.display.update()
    restart_surf = small_font.render("Presiona ENTER para reiniciar", True, (200, 200, 200))
    restart_rect = restart_surf.get_rect(center=(screensize[0] // 2, panel_rect.bottom - 60))
    screen.blit(restart_surf, restart_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
