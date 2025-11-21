import ctypes
from modules.utils.cfg import SKIER_DLL

def updateSpeed(score, speed_bonus, base_speed, speed_levels, achieved_levels, direction):
    levels_count = len(speed_levels)
    speed_levels_array = (ctypes.c_int * levels_count)(*speed_levels)
    achieved_list = list(achieved_levels)
    achieved_count = len(achieved_list)
    MAX_ACHIEVED = 50
    achieved_levels_array = (ctypes.c_int * MAX_ACHIEVED)(*achieved_list + [0] * (MAX_ACHIEVED - achieved_count))
    achieved_count_ptr = ctypes.c_int(achieved_count)
    speed_bonus_ptr = ctypes.c_int(speed_bonus)
    base_speed_ptr = ctypes.c_int(base_speed)
    current_speed_ptr = ctypes.c_int(0)
    SKIER_DLL.updateSpeed(
        score,
        ctypes.byref(speed_bonus_ptr),
        ctypes.byref(base_speed_ptr),
        speed_levels_array,
        levels_count,
        achieved_levels_array,
        ctypes.byref(achieved_count_ptr),
        direction,
        ctypes.byref(current_speed_ptr)        
    )
    achieved_levels.clear()
    for i in range(achieved_count_ptr.value):
        achieved_levels.add(achieved_levels_array[i])
    return speed_bonus_ptr.value, base_speed_ptr.value, current_speed_ptr.value

def setup_prototypes():
    SKIER_DLL.updateSpeed.argtypes = [
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
    ]