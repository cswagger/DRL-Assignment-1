import random

step = 0
has_passenger = False
phase = 0  # 0: searching for passenger, 1: delivering
target_idx = 0
blocked_timer = 0  # countdown for random walk when blocked

def is_on_station(pos, stations):
    return pos in stations

def is_isolated_station(pos, stations):
    r, c = pos
    for s in stations:
        if s == pos:
            continue
        sr, sc = s
        if abs(sr - r) + abs(sc - c) == 1:
            return False
    return True

def get_action(obs):
    global step, has_passenger, phase, target_idx, blocked_timer
    step += 1

    taxi_r, taxi_c = obs[0], obs[1]
    taxi_pos = (taxi_r, taxi_c)
    stations = [(obs[i], obs[i+1]) for i in range(2, 10, 2)]
    passenger_visible = obs[14]
    destination_visible = obs[15]

    obstacle_north = obs[10]
    obstacle_south = obs[11]
    obstacle_east  = obs[12]
    obstacle_west  = obs[13]

    # === Phase switch ===
    if not has_passenger and passenger_visible and is_on_station(taxi_pos, stations) and is_isolated_station(taxi_pos, stations):
        has_passenger = True
        phase = 1
        target_idx = 0
        return 4  # Pickup

    if has_passenger and destination_visible and is_on_station(taxi_pos, stations) and is_isolated_station(taxi_pos, stations):
        has_passenger = False
        phase = 0
        target_idx = 0
        return 5  # Dropoff

    # === Set Target ===
    target = stations[target_idx]

    if taxi_pos == target:
        target_idx = (target_idx + 1) % 4
        target = stations[target_idx]

    # === Obstacle-aware movement toward target ===
    dx = target[0] - taxi_r
    dy = target[1] - taxi_c

    move_candidates = []

    if dx < 0 and obstacle_north == 0:
        move_candidates.append(1)  # North
    if dx > 0 and obstacle_south == 0:
        move_candidates.append(0)  # South
    if dy < 0 and obstacle_west == 0:
        move_candidates.append(3)  # West
    if dy > 0 and obstacle_east == 0:
        move_candidates.append(2)  # East

    if move_candidates:
        blocked_timer = 0
        return random.choice(move_candidates)

    # === Temporarily blocked → random walk ===
    if blocked_timer > 0:
        blocked_timer -= 1
        valid_moves = []
        if obstacle_south == 0: valid_moves.append(0)
        if obstacle_north == 0: valid_moves.append(1)
        if obstacle_east  == 0: valid_moves.append(2)
        if obstacle_west  == 0: valid_moves.append(3)
        return random.choice(valid_moves) if valid_moves else random.choice([4, 5])
    else:
        blocked_timer = 5
        return get_action(obs)  # try again with random walk logic next time




# from simple_custom_taxi_env import generate_custom_env_config
# from simple_custom_taxi_env import run_agent

# config = generate_custom_env_config(grid_size=6, wall_count=5)
# run_agent("student_agent.py", config, render=True)