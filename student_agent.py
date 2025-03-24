# student_agent.py
import random
from collections import deque

step = 0
has_passenger = False
phase = 0  # 0: pickup, 1: dropoff
current_target_idx = 0
recent_positions = deque(maxlen=5)
random_walk_steps = 0

# Utility
ACTIONS = [0, 1, 2, 3, 4, 5]  # [South, North, East, West, Pickup, Dropoff]
DIRECTION_VECTORS = {0: (1, 0), 1: (-1, 0), 2: (0, 1), 3: (0, -1)}

def get_action(obs):
    global step, has_passenger, phase, current_target_idx, recent_positions, random_walk_steps
    step += 1

    taxi_r, taxi_c = obs[0], obs[1]
    taxi_pos = (taxi_r, taxi_c)
    stations = [(obs[i], obs[i+1]) for i in range(2, 10, 2)]
    passenger_visible = obs[14]
    destination_visible = obs[15]
    wall_flags = obs[10:14]  # north, south, east, west

    # === Dropoff logic ===
    if has_passenger and taxi_pos in stations and destination_visible:
        has_passenger = False
        phase = 0
        return 5  # Dropoff

    # === Pickup logic ===
    if not has_passenger and taxi_pos in stations and passenger_visible:
        has_passenger = True
        phase = 1
        return 4  # Pickup

    # === Movement logic ===
    target_station = stations[current_target_idx]

    if taxi_pos == target_station:
        # Move to next station
        current_target_idx = (current_target_idx + 1) % 4
        target_station = stations[current_target_idx]
        random_walk_steps = 0  # reset walk counter

    dx = target_station[0] - taxi_r
    dy = target_station[1] - taxi_c

    directions = []
    if dx < 0 and not wall_flags[0]:  # north
        directions.append(1)
    if dx > 0 and not wall_flags[1]:  # south
        directions.append(0)
    if dy > 0 and not wall_flags[2]:  # east
        directions.append(2)
    if dy < 0 and not wall_flags[3]:  # west
        directions.append(3)

    # Try to go toward target
    if directions:
        action = random.choice(directions)
        next_vec = DIRECTION_VECTORS[action]
        next_pos = (taxi_r + next_vec[0], taxi_c + next_vec[1])
        if next_pos not in recent_positions:
            recent_positions.append(next_pos)
            return action

    # === Random walk (when stuck) ===
    random_walk_steps += 1
    valid_random_moves = [a for a in range(4) if not wall_flags[a ^ (1 if a % 2 == 0 else -1)]]
    if valid_random_moves:
        action = random.choice(valid_random_moves)
        next_vec = DIRECTION_VECTORS[action]
        next_pos = (taxi_r + next_vec[0], taxi_c + next_vec[1])
        recent_positions.append(next_pos)
        return action

    # === Fallback ===
    return random.choice([4, 5])  # attempt pickup/dropoff if fully stuck
