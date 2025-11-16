def updateSpeed(score, speed_bonus, base_speed, speed_levels, achieved_levels, direction):
    for lvl in [l for l in speed_levels if score >= l and l not in achieved_levels]:
        achieved_levels.add(lvl)
        speed_bonus += 0.16666667
        base_speed = 6.0 * (1 + speed_bonus)
    
    return speed_bonus, base_speed, base_speed - abs(direction) * 2
