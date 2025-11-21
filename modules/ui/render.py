import pygame
from modules.utils import cfg

def draw_gradient_background(screen):
    for y in range(cfg.SCREENSIZE[1]):
        ratio = y / cfg.SCREENSIZE[1]
        shade = int(240 - ratio * 20)
        pygame.draw.line(screen, (shade, shade, shade), (0, y), (cfg.SCREENSIZE[0], y))

def draw_text(screen, text, font, color, pos):
    surf = font.render(text, True, color)
    screen.blit(surf, pos)

def draw_panel(screen, rect, color=(255, 255, 255), border_color=(120, 120, 120), alpha=210):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.set_alpha(alpha)
    panel.fill(color)
    screen.blit(panel, rect.topleft)
    pygame.draw.rect(screen, border_color, rect, 2)

def draw_score_panel(screen, score):
    font = pygame.font.Font(cfg.FONTPATH, 28)
    txt = f"Pts: {score}"
    txt_surf = font.render(txt, True, (255, 180, 0))
    screen.blit(txt_surf, (20, 20))

def draw_speed_indicator(screen, vel, speed_bonus):
    color = (0, 0, 0)       # black
    font = pygame.font.Font(cfg.FONTPATH, 28)
    speed_txt = f"{int(vel)} km/h"
    speed_surf = font.render(speed_txt, True, color)
    speed_x = cfg.SCREENSIZE[0] // 2 - speed_surf.get_width() // 2
    screen.blit(speed_surf, (speed_x, 20))
    if speed_bonus > 0:
        bonus_font = pygame.font.Font(cfg.FONTPATH, 20)
        bonus_txt = f"BOOST +{speed_bonus}"
        bonus_surf = bonus_font.render(bonus_txt, True, (255, 100, 100))
        bonus_x = cfg.SCREENSIZE[0] // 2 - bonus_surf.get_width() // 2
        screen.blit(bonus_surf, (bonus_x, 45))

def draw_health_bar(screen, lives, max_lives=3):
    bar_width = 200
    bar_height = 25
    x = cfg.SCREENSIZE[0] - bar_width - 20
    y = 20
    panel_rect = pygame.Rect(x - 5, y - 5, bar_width + 10, bar_height + 10)
    draw_panel(screen, panel_rect, (220, 220, 220), (120, 120, 120), 180)
    if lives >= 3:
        color = (0, 200, 0)
    elif lives == 2:
        color = (255, 200, 0)
    else:
        color = (255, 50, 50)
    fill_width = int(bar_width * lives / max_lives)
    pygame.draw.rect(screen, color, (x, y, fill_width, bar_height))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, bar_width, bar_height), 2)
    font = pygame.font.Font(cfg.FONTPATH, 18)
    txt = f"{lives}"
    txt_surf = font.render(txt, True, (0, 0, 0))
    screen.blit(txt_surf, (x + bar_width // 2 - txt_surf.get_width() // 2, y + 3))

def draw_top_hud(screen, score, lives, vel, speed_bonus):
    hud_rect = pygame.Rect(0, 0, cfg.SCREENSIZE[0], 70)
    draw_panel(screen, hud_rect, (255, 255, 255), (120, 120, 120), 210)
    draw_score_panel(screen, score)
    draw_speed_indicator(screen, vel, speed_bonus)
    draw_health_bar(screen, lives)

def updateFrame(screen, obstacles, skier, score, lives, speed, speed_bonus=0, vel=0.0):
    draw_gradient_background(screen)
    try:
        obstacles.draw(screen)
    except Exception:
        pass
    screen.blit(skier.image, skier.rect)
    draw_top_hud(screen, score, lives, vel, speed_bonus)
    pygame.display.update()
