import ctypes
from modules.utils.cfg import SKIER_DLL
from modules.classes.gameState import GameStateClass, GameState

def createGameState():
    game_state = GameStateClass()
    return game_state

def getGameStateValues(game_state):
    if isinstance(game_state, GameStateClass):
        return game_state.getValues()
    else:
        state = ctypes.cast(game_state, ctypes.POINTER(GameState)).contents
        return {
            'distance': state.distance,
            'score': state.score,
            'obstaclesFlag': state.obstaclesFlag,
            'added_trees': state.added_trees,
            'added_flags': state.added_flags,
            'base_speed': state.base_speed,
            'speed_bonus': state.speed_bonus
        }

def updateDistance(game_state, speed_y):
    if isinstance(game_state, GameStateClass):
        game_state.updateDistance(speed_y)
    else:
        SKIER_DLL.GameState_updateDistance(game_state, speed_y)

def addScore(game_state, points):
    if isinstance(game_state, GameStateClass):
        game_state.addScore(points)
    else:
        SKIER_DLL.GameState_addScore(game_state, points)

def updateObstaclesCycle(game_state, speed_y):
    if isinstance(game_state, GameStateClass):
        return game_state.updateObstaclesCycle(speed_y)
    else:
        return SKIER_DLL.updateObstaclesCycle(game_state, speed_y)

def checkCollision(x1, y1, w1, h1, x2, y2, w2, h2):
    setup_collision_prototypes()
    result = SKIER_DLL.checkCollision(x1, y1, w1, h1, x2, y2, w2, h2)
    return result == 1

def setSpeedBonus(game_state, speed_bonus):
    if isinstance(game_state, GameStateClass):
        game_state.setSpeedBonus(speed_bonus)
    else:
        state = ctypes.cast(game_state, ctypes.POINTER(GameState)).contents
        state.speed_bonus = speed_bonus

def setBaseSpeed(game_state, base_speed):
    if isinstance(game_state, GameStateClass):
        game_state.setBaseSpeed(base_speed)
    else:
        state = ctypes.cast(game_state, ctypes.POINTER(GameState)).contents
        state.base_speed = base_speed

def setup_collision_prototypes():
    SKIER_DLL.checkCollision.restype = ctypes.c_int
    SKIER_DLL.checkCollision.argtypes = [
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int 
    ]