import ctypes
from modules.utils.cfg import SKIER_DLL

class GameStateClass:
    def __init__(self):
        self.setup_prototypes()
        self.state_ptr = SKIER_DLL.GameState_create()
    
    def getValues(self):
        state_struct = ctypes.cast(self.state_ptr, ctypes.POINTER(GameState)).contents
        return {
            'distance': state_struct.distance,
            'score': state_struct.score,
            'obstaclesFlag': state_struct.obstaclesFlag,
            'added_trees': state_struct.added_trees,
            'added_flags': state_struct.added_flags,
            'base_speed': state_struct.base_speed,
            'speed_bonus': state_struct.speed_bonus
        }
    
    def updateDistance(self, speed_y):
        SKIER_DLL.GameState_updateDistance(self.state_ptr, speed_y)
    
    def addScore(self, points):
        SKIER_DLL.GameState_addScore(self.state_ptr, points)
    
    def updateObstaclesCycle(self, speed_y):
        return SKIER_DLL.updateObstaclesCycle(self.state_ptr, speed_y)
    
    def setSpeedBonus(self, speed_bonus):
        state = ctypes.cast(self.state_ptr, ctypes.POINTER(GameState)).contents
        state.speed_bonus = speed_bonus
    
    def setBaseSpeed(self, base_speed):
        state = ctypes.cast(self.state_ptr, ctypes.POINTER(GameState)).contents
        state.base_speed = base_speed
    
    def setup_prototypes(self):
        SKIER_DLL.GameState_create.restype = ctypes.c_void_p
        SKIER_DLL.GameState_create.argtypes = []
        SKIER_DLL.GameState_updateDistance.restype = None
        SKIER_DLL.GameState_updateDistance.argtypes = [ctypes.c_void_p, ctypes.c_int]
        SKIER_DLL.GameState_addScore.restype = None
        SKIER_DLL.GameState_addScore.argtypes = [ctypes.c_void_p, ctypes.c_int]
        SKIER_DLL.updateObstaclesCycle.restype = ctypes.c_int
        SKIER_DLL.updateObstaclesCycle.argtypes = [ctypes.c_void_p, ctypes.c_int]


class GameState(ctypes.Structure):
    _fields_ = [
        ("distance", ctypes.c_int),
        ("score", ctypes.c_int),
        ("obstaclesFlag", ctypes.c_int),
        ("added_trees", ctypes.c_int),
        ("added_flags", ctypes.c_int),
        ("base_speed", ctypes.c_int),
        ("speed_bonus", ctypes.c_int),
    ]
