import pygame, random, ctypes
from modules.utils.cfg import SKIER_DLL, OBSTICE_PATH
from modules.classes.obstacle import ObstacleClass

def createObstacles(s, e, num, obs="None"):
    obstacles = pygame.sprite.Group()
    MAX_OBS = 50
    location = ctypes.c_int * 2
    locations_array = (location * MAX_OBS)()
    attribute = ctypes.c_char * 20
    attributes_array = (attribute * MAX_OBS)()
    num_obstacles = ctypes.c_int(0)
    obs_bytes = obs.encode('utf-8') if obs != "None" else "None".encode('utf-8')
    SKIER_DLL.createObstacles(s, e, num, obs_bytes, locations_array, attributes_array, ctypes.byref(num_obstacles))
    for i in range(num_obstacles.value):
        location = [locations_array[i][0], locations_array[i][1]]
        attribute = attributes_array[i].value.decode('utf-8')
        img_path = OBSTICE_PATH[attribute]
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
    trees_ptr = ctypes.c_int(added_trees)
    flags_ptr = ctypes.c_int(added_flags)
    SKIER_DLL.updateObstacles(score, ctypes.byref(trees_ptr), ctypes.byref(flags_ptr))
    return trees_ptr.value, flags_ptr.value

def setup_prototupes(self):
    SKIER_DLL.createObstacles.argtypes = [
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_int * 2),
        ctypes.POINTER(ctypes.c_char * 20),
        ctypes.POINTER(ctypes.c_int)  
    ]
    SKIER_DLL.updateObstacles.argtypes = [
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int)
    ]