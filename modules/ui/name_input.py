import pygame
import sys
from modules.utils import cfg

def draw_gradient_background(screen, screensize):
    for y in range(screensize[1]):
        ratio = y / screensize[1]
        shade = int(240 - ratio * 20)  # 240 → 220
        pygame.draw.line(screen, (shade, shade, shade), (0, y), (screensize[0], y))

def get_player_name(screen, screensize):
    font = pygame.font.Font(cfg.FONTPATH, 36)
    input_box = pygame.Rect(screensize[0] // 2 - 150, screensize[1] // 2, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    name = ""
    draw_gradient_background(screen, screensize)
    msg = font.render("Escribe tu nombre y presiona ENTER", True, (0, 0, 0))
    msg_rect = msg.get_rect(center=(screensize[0] // 2, screensize[1] // 2 - 100))
    screen.blit(msg, msg_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN and name.strip():
                    return name[:12]
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    if len(name) < 12 and event.unicode.isprintable():
                        name += event.unicode
        draw_gradient_background(screen, screensize)
        screen.blit(msg, msg_rect)
        txt_surface = font.render(name, True, color)
        input_box.w = max(300, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
