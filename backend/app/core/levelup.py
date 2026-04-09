LEVEL_THRESHOLDS = [0, 1, 2, 4, 8, 100]


def handle_xp_change(xp_change: int, level_xp: int, current_level: int, streak: int):
    new_xp = level_xp + (xp_change if xp_change < 0 else xp_change * streak)
    if new_xp < 0:
        return {"level_xp": 0, "current_level": current_level}
    else:
        while LEVEL_THRESHOLDS[current_level] <= new_xp and current_level < 5:
            current_level += 1
            new_xp -= LEVEL_THRESHOLDS[current_level]
        return {"level_xp": new_xp, "current_level": current_level}
