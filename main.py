import sys, pygame
from modules.utils import cfg
from modules.classes.skier import SkierClass
from modules.mechanics.obstacles import createObstacles, addObstacles, updateObstacles
from modules.mechanics.speed import updateSpeed
from modules.mechanics import gameLogic as GL 
from modules.ui.render import updateFrame
from modules.ui.menus import showStartInterface
from modules.ui.scoreboard import show_scores
from modules.ui.gameover import showGameOver

def main():
    pygame.init()
    try:
        pygame.mixer.init()
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
        game_state = GL.createGameState()
        speed = [0, 6]
        speed_levels = [250, 500, 750, 1000, 1500, 2000]
        achieved_levels = set()
        obstacles0 = createObstacles(20, 29, 0, "tree")
        obstacles1 = createObstacles(10, 19, 0, "flag")
        obstacles = addObstacles(obstacles0, obstacles1)
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        speed = skier.turn(-1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        speed = skier.turn(1)
            state = GL.getGameStateValues(game_state)
            speed_bonus, base_speed, current_vert = updateSpeed(
                state['score'], 
                state['speed_bonus'], 
                state['base_speed'], 
                speed_levels, 
                achieved_levels, 
                skier.direction
            )
            GL.setSpeedBonus(game_state, speed_bonus)
            GL.setBaseSpeed(game_state, base_speed)
            skier.speed[1] = current_vert
            speed[1] = skier.speed[1]
            skier.move()
            GL.updateDistance(game_state, speed[1])
            cycle_update = GL.updateObstaclesCycle(game_state, speed[1])
            state = GL.getGameStateValues(game_state)
            if cycle_update == 1:
                obstacles0 = createObstacles(20, 29, state['added_trees'], "tree")
                obstacles = addObstacles(obstacles0, obstacles1)
            elif cycle_update == 2:
                for obstacle in obstacles0:
                    location = obstacle.getLocation()
                    location[1] = location[1] - 1280
                    obstacle.setLocation(location)
                obstacles1 = createObstacles(10, 19, state['added_flags'], "flag")
                obstacles = addObstacles(obstacles0, obstacles1)
            for obstacle in obstacles:
                obstacle.move(state['distance'])
            hitted_obstacles = pygame.sprite.spritecollide(skier, obstacles, False)
            if hitted_obstacles:
                obs = hitted_obstacles[0]
                if obs.attribute == "tree" and not obs.passed:
                    skier.lives -= 1
                    skier.setFall()
                    updateFrame(screen, obstacles, skier, state['score'], skier.lives, speed, state['speed_bonus'], skier.speed[1])
                    pygame.time.delay(1000)
                    skier.setForward()
                    obs.passed = True
                    if skier.lives <= 0:
                        result = showGameOver(screen, cfg.SCREENSIZE, state['score'])
                        if result == "restart":
                            running = False
                            break
                elif obs.attribute == "flag" and not obs.passed:
                    GL.addScore(game_state, 250)
                    state = GL.getGameStateValues(game_state)
                    obs.passed = True
                    try:
                        obstacles.remove(obs)
                    except Exception:
                        pass
            updateObstacles(state['score'], state['added_trees'], state['added_flags'])
            updateFrame(screen, obstacles, skier, state['score'], skier.lives, speed, state['speed_bonus'], skier.speed[1])
            clock.tick(cfg.FPS)

if __name__ == "__main__":
    main()
