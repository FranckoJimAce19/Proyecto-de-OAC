import pygame, ctypes
from modules.utils.cfg import SKIER_DLL

class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, img_path, location, attribute):
        pygame.sprite.Sprite.__init__(self)   
        self.setup_prototypes()
        self.obstacle_ptr = SKIER_DLL.Obstacle_create(location[0], location[1], ctypes.c_char_p(attribute.encode('utf-8')))
        self.img_path = img_path
        self.image = pygame.image.load(self.img_path)
        self.rect = self.image.get_rect()
        self.rect.center = self.getLocation()
        self.attribute = SKIER_DLL.Obstacle_getAttribute(self.obstacle_ptr).decode('utf-8')
        self.passed = SKIER_DLL.Obstacle_getPassed(self.obstacle_ptr)
        
    def move(self, num):
        dy = SKIER_DLL.Obstacle_move(self.obstacle_ptr, num)
        self.rect.centery = dy
    
    def setPassed(self, val):
        SKIER_DLL.Obstacle_setPassed(self.obstacle_ptr, int(val))

    def getLocation(self):
        x = ctypes.c_int(); y = ctypes.c_int()
        SKIER_DLL.Obstacle_getPosition(self.obstacle_ptr, ctypes.byref(x), ctypes.byref(y))
        return [x.value, y.value]

    def setLocation(self, location):
        SKIER_DLL.Obstacle_setPosition(self.obstacle_ptr, location[0], location[1])
    
    def setup_prototypes(self):
        """Configurar los prototipos de las funciones de la DLL"""
        SKIER_DLL.Obstacle_create.restype = ctypes.c_void_p
        SKIER_DLL.Obstacle_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
        SKIER_DLL.Obstacle_move.argtypes = [ctypes.c_void_p, ctypes.c_int]
        SKIER_DLL.Obstacle_getPosition.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        SKIER_DLL.Obstacle_getAttribute.argtypes = [ctypes.c_void_p]
        SKIER_DLL.Obstacle_setPosition.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        SKIER_DLL.Obstacle_getAttribute.restype = ctypes.c_char_p
        SKIER_DLL.Obstacle_getPassed.argtypes = [ctypes.c_void_p]
        SKIER_DLL.Obstacle_getPassed.restype = ctypes.c_bool
        SKIER_DLL.Obstacle_setPassed.argtypes = [ctypes.c_void_p, ctypes.c_bool]