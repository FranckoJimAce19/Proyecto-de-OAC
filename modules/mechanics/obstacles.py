import pygame, random
from modules.utils import cfg
from modules.classes.obstacle import ObstacleClass

def createObstacles(s, e, num, obs="None"):
    obstacles = pygame.sprite.Group()
    ref = num
    locations = []
    for i in range(10+num):
        row = random.randint(s, e)
        col = random.randint(0, 9)
        location = [col * 64 + 20, row * 64 + 20]
        if location not in locations:
            locations.append(location)
            if (obs == "tree" or obs == "flag") and (ref != 0 and ref <= num):
                attribute = obs
                ref -= 1
            else:
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


def updateObstacles(score, added_trees, added_flags,):
    # Árboles
    if score > 0 and score % 200 == 0 and added_trees < 20:
        added_trees += 2
    # Banderas
    if score > 0 and score % 200 == 0 and added_flags < 10:
        added_flags += 1
    return added_trees, added_flags