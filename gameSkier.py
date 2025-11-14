import sys, cfg, pygame, random, os 

class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 0
        self.imagpaths = cfg.SKIER_IMAGE_PATH[:-1]
        self.image = pygame.image.load(self.imagpaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.speed = [self.direction, 6 - abs(self.direction) * 2]
        self.lives = 3  # vidas iniciales

    def turn(self, num):
        self.direction += num
        self.direction = max(-2, self.direction)
        self.direction = min(2, self.direction)
        center = self.rect.center
        self.image = pygame.image.load(self.imagpaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = [self.direction, 6 - abs(self.direction) * 2]
        return self.speed

    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centerx = max(20, self.rect.centerx)
        self.rect.centerx = min(620, self.rect.centerx)

    def setFall(self):
        self.image = pygame.image.load(cfg.SKIER_IMAGE_PATH[-1])

    def setForward(self):
        self.direction = 0
        self.image = pygame.image.load(self.imagpaths[self.direction])
        self.speed = [self.direction, 6 - abs(self.direction) * 2]


class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, img_path, location, attribute):
        pygame.sprite.Sprite.__init__(self)
        self.img_path = img_path
        self.image = pygame.image.load(self.img_path)
        self.location = location[:] 
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.attribute = attribute
        self.passed = False

    def move(self, num):
        self.rect.centery = self.location[1] - num


#=========================================================
def createObstacles(s, e, num=10):
    obstacles = pygame.sprite.Group()
    locations = []
    for i in range(num):
        row = random.randint(s, e)
        col = random.randint(0, 9)
        location = [col * 64 + 20, row * 64 + 20]
        if location not in locations:
            locations.append(location)
            attribute = random.choice(list(cfg.OBSTICE_PATH.keys()))
            img_path = cfg.OBSTICE_PATH[attribute]
            obstacle = ObstacleClass(img_path, location, attribute)
            obstacles.add(obstacle)
    return obstacles


def addObstacles(obstacles0, obstacles1):
    obstacles = pygame.sprite.Group()
    for obstacle in obstacles0:
        obstacles.add(obstacle)
    for obstacle in obstacles1:
        obstacles.add(obstacle)
    return obstacles

def showStartInterface(screen, screensize):
    screen.fill([255, 255, 255])
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
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start"
                elif event.key == pygame.K_2:
                    return "scores"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def load_scores():
    if not os.path.exists(cfg.HIGHEST_SCORE_RECORD_FILEPATH):
        return []
    with open(cfg.HIGHEST_SCORE_RECORD_FILEPATH, "r") as f:
        lines = f.readlines()
    scores = []
    for line in lines:
        parts = line.strip().split(":", 1)
        if len(parts) == 2:
            name, sc = parts
            try:
                scores.append((name, int(sc)))
            except:
                continue
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[:10]

def save_score(name, score):
    scores = load_scores()
    scores.append((name, score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:10]
    with open(cfg.HIGHEST_SCORE_RECORD_FILEPATH, "w") as f:
        for n, s in scores:
            f.write(f"{n}:{s}\n")

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
            text = score_font.render(f"{i+1}. {name} - {s}", True, (0,0,0))
            rect = text.get_rect(center=(screensize[0]//2, y))
            screen.blit(text, rect)
            y += 45
    exit_text = score_font.render("Presiona cualquier tecla para volver", True, (255,0,0))
    rect = exit_text.get_rect(center=(screensize[0]//2, screensize[1]-60))
    screen.blit(exit_text, rect)
    pygame.display.update()
    wait_key()


def wait_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                return

def showScore(screen, score, lives, speed, speed_bonus=0, vel=0.0, pos=[10, 10]):
    font = pygame.font.Font(cfg.FONTPATH, 28)
    base_text = f"Score: {score} Vidas: {lives} Velocidad {vel:.2f}"
    if speed_bonus and speed_bonus > 0 and speed_bonus < 0.2:
        percent = int(speed_bonus * 100)
        base_text += f" (+{percent}% bonus!)"
    scoretext = font.render(base_text, True, (0,0,0))
    screen.blit(scoretext, pos)

def updateFrame(screen, obstacles, skier, score, lives, speed, speed_bonus=0, vel=0.0):
    screen.fill([255, 255, 255])
    try:
        obstacles.draw(screen)
    except Exception:
        pass
    screen.blit(skier.image, skier.rect)
    showScore(screen, score, lives, speed, speed_bonus, vel)
    pygame.display.update()


def get_player_name(screen, screensize):
    font = pygame.font.Font(cfg.FONTPATH, 36)
    input_box = pygame.Rect(screensize[0]//2 - 150, screensize[1]//2, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    name = ""
    screen.fill((255,255,255))
    text = font.render("Escribe tu nombre y presiona ENTER", True, (0,0,0))
    rect = text.get_rect(center=(screensize[0]//2, screensize[1]//2 - 100))
    screen.blit(text, rect)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and name.strip():
                        return name[:12]
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 12:
                            if event.unicode:
                                name += event.unicode
        
        screen.fill((255,255,255))
        txt_surface = font.render(name, True, color)
        width = max(300, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(text, rect)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()


def showGameOver(screen, screensize, score):
    name = get_player_name(screen, screensize)
    save_score(name, score)
    font = pygame.font.Font(cfg.FONTPATH, 40)
    screen.fill((255,255,255))
    text = font.render(f"Fin del juego - Puntuación: {score}", True, (255,0,0))
    restart = font.render("R - Reiniciar", True, (0,0,255))
    exit = font.render("ESC - Salir", True, (0,0,0))
    text_rect = text.get_rect(center=(screensize[0]//2, 200))
    restart_rect = restart.get_rect(center=(screensize[0]//2, 300))
    exit_rect = exit.get_rect(center=(screensize[0]//2, 380))
    screen.blit(text, text_rect)
    screen.blit(restart, restart_rect)
    screen.blit(exit, exit_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def generate_free_location(existing_locations, attempts=20):
    for _ in range(attempts):
        col = random.randint(0, 9)
        row = random.randint(10, 29)
        location = [col * 64 + 20, row * 64 + 20]
        if location not in existing_locations:
            return location
    return None

def main():
    pygame.init()
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(cfg.BMGPATH)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("Skier")

    while True:
        action = showStartInterface(screen, cfg.SCREENSIZE)
        if action == "scores":
            show_scores(screen, cfg.SCREENSIZE)
            continue

        skier = SkierClass()
        obstacles0 = createObstacles(20, 29)
        obstacles1 = createObstacles(10, 19)
        obstacleFlag = 0
        obstacles = addObstacles(obstacles0, obstacles1)
        clock = pygame.time.Clock()
        distance = 0
        score = 0
        speed = [0, 6]
        base_speed = 6.0
        speed_bonus = 0.0
        added_trees = 0
        added_flags = 0
        last_tree_score_trigger = -1
        last_flag_score_trigger = -1
        speed_levels = [250, 500, 750, 1000]
        achieved_levels = set()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        speed = skier.turn(-1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        speed = skier.turn(1)

            # Aumentar velocidad
            for lvl in speed_levels:
                if score >= lvl and lvl not in achieved_levels:
                    achieved_levels.add(lvl)
                    speed_bonus += 0.05 
                    base_speed = 6.0 * (1 + speed_bonus)
            skier.speed[1] = base_speed - abs(skier.direction) * 2
            speed[1] = skier.speed[1]
            skier.move()
            distance += speed[1]
            if distance >= 640 and obstacleFlag == 0:
                obstacleFlag = 1
                obstacles0 = createObstacles(20, 29)
                obstacles = addObstacles(obstacles0, obstacles1)
            if distance >= 1280 and obstacleFlag == 1:
                obstacleFlag = 0
                distance -= 1280
                for obstacle in obstacles0:
                    obstacle.location[1] -= 1280
                obstacles1 = createObstacles(10, 19)
                obstacles = addObstacles(obstacles0, obstacles1)

            for obstacle in list(obstacles):
                obstacle.move(distance)

            #colisiones
            hitted_obstacles = pygame.sprite.spritecollide(skier, obstacles, False)
            if hitted_obstacles:
                obs = hitted_obstacles[0]
                if obs.attribute == "tree" and not obs.passed:
                    skier.lives -= 1
                    skier.setFall()
                    updateFrame(screen, obstacles, skier, score, skier.lives, speed_bonus, skier.speed[1])
                    pygame.time.delay(1000)
                    skier.setForward()
                    obs.passed = True
                    if skier.lives <= 0:
                        result = showGameOver(screen, cfg.SCREENSIZE, score)
                        if result == "restart":
                            running = False
                            break
                elif obs.attribute == "flag" and not obs.passed:
                    score += 10
                    try:
                        obstacles.remove(obs)
                    except Exception:
                        pass

           #no mover este codigo de aqui
            existing_locations = [ob.location for ob in obstacles]
            if score > 0 and score % 200 == 0 and added_trees < 20 and last_tree_score_trigger != score:
                img_path = cfg.OBSTICE_PATH.get("tree")
                if img_path:
                    for _ in range(2): 
                        if added_trees >=20:
                            break
                        loc = generate_free_location(existing_locations, attempts=30)
                        if loc:
                            obstacle = ObstacleClass(img_path, loc, "tree")
                            obstacles.add(obstacle)
                            added_trees += 1
                            existing_locations.append(loc)
                last_tree_score_trigger = score
            if score > 0 and score % 150 == 0 and added_flags < 10 and last_flag_score_trigger != score:
                img_path = cfg.OBSTICE_PATH.get("flag")
                if img_path:
                    loc = generate_free_location(existing_locations, attempts=30)
                    if loc:
                        obstacle = ObstacleClass(img_path, loc, "flag")
                        obstacles.add(obstacle)
                        added_flags += 1
                        existing_locations.append(loc)
                last_flag_score_trigger = score

 
            updateFrame(screen, obstacles, skier, score, skier.lives, speed, speed_bonus, skier.speed[1])
            clock.tick(cfg.FPS)

if __name__ == "__main__":
    main()