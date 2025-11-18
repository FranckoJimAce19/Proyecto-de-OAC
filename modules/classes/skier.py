import pygame, ctypes
from modules.utils.cfg import SKIER_DLL, SKIER_IMAGE_PATH

class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.setup_prototypes()
        self.skier_ptr = SKIER_DLL.Skier_create()
        self.direction = SKIER_DLL.Skier_getDirection(self.skier_ptr)
        self.imagpaths = SKIER_IMAGE_PATH[:-1]
        self.image = pygame.image.load(self.imagpaths[self.direction])
        self.rect = self.image.get_rect()
        x = ctypes.c_int()
        y = ctypes.c_int()
        SKIER_DLL.Skier_getPosition(self.skier_ptr, ctypes.byref(x), ctypes.byref(y))
        self.rect.center = [x.value, y.value]
        speed_x = ctypes.c_int()
        speed_y = ctypes.c_int()
        SKIER_DLL.Skier_getSpeed(self.skier_ptr, ctypes.byref(speed_x), ctypes.byref(speed_y))
        self.speed = [speed_x.value, speed_y.value]
        self.lives = SKIER_DLL.Skier_getLives(self.skier_ptr)
       

    def turn(self, num):
        SKIER_DLL.Skier_turn(self.skier_ptr, num)
        self.direction = SKIER_DLL.Skier_getDirection(self.skier_ptr)
        self.direction = max(-2, self.direction)
        self.direction = min(2, self.direction)
        center = self.rect.center
        self.image = pygame.image.load(self.imagpaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed_x = ctypes.c_int()
        speed_y = ctypes.c_int()
        SKIER_DLL.Skier_getSpeed(self.skier_ptr, ctypes.byref(speed_x), ctypes.byref(speed_y))
        self.speed = [speed_x.value, speed_y.value]
        return self.speed

    def move(self):
        SKIER_DLL.Skier_move(self.skier_ptr)
        x = ctypes.c_int()
        y = ctypes.c_int()
        SKIER_DLL.Skier_getPosition(self.skier_ptr, ctypes.byref(x), ctypes.byref(y))
        self.rect.centerx = x.value
        self.rect.centerx = max(20, self.rect.centerx)
        self.rect.centerx = min(620, self.rect.centerx)

    def setFall(self):
        self.image = pygame.image.load(SKIER_IMAGE_PATH[-1])

    def setForward(self):
        SKIER_DLL.Skier_setForward(self.skier_ptr)
        self.direction = SKIER_DLL.Skier_getDirection(self.skier_ptr)
        self.image = pygame.image.load(self.imagpaths[self.direction])
        speed_x = ctypes.c_int()
        speed_y = ctypes.c_int()
        SKIER_DLL.Skier_getSpeed(self.skier_ptr, ctypes.byref(speed_x), ctypes.byref(speed_y))
        self.speed = [speed_x.value, speed_y.value]

    def setup_prototypes(self):
        """Configurar los prototipos de las funciones de la DLL"""
        SKIER_DLL.Skier_create.restype = ctypes.c_void_p
        SKIER_DLL.Skier_turn.argtypes = [ctypes.c_void_p, ctypes.c_int]
        SKIER_DLL.Skier_move.argtypes = [ctypes.c_void_p]
        SKIER_DLL.Skier_setForward.argtypes = [ctypes.c_void_p]
        SKIER_DLL.Skier_getDirection.argtypes = [ctypes.c_void_p]
        SKIER_DLL.Skier_getDirection.restype = ctypes.c_int
        SKIER_DLL.Skier_getPosition.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        SKIER_DLL.Skier_getSpeed.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        SKIER_DLL.Skier_getLives.argtypes = [ctypes.c_void_p]
        SKIER_DLL.Skier_getLives.restype = ctypes.c_int