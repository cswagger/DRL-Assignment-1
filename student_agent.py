# student_agent.py
import random
from collections import deque

step = 0
has_passenger = False
phase = 0  # 0: pickup, 1: dropoff
current_target_idx = 0
recent_positions = deque(maxlen=5)
random_walk_steps = 0
visited_stations_phase = set()
guessed_destination_idx = None

# Utility
ACTIONS = [0, 1, 2, 3, 4, 5]  # [South, North, East, West, Pickup, Dropoff]
DIRECTION_VECTORS = {0: (1, 0), 1: (-1, 0), 2: (0, 1), 3: (0, -1)}

def get_action(obs):
    global step, has_passenger, phase, current_target_idx
    global recent_positions, random_walk_steps, visited_stations_phase
    global guessed_destination_idx

    step += 1

    taxi_r, taxi_c = obs[0], obs[1]
    taxi_pos = (taxi_r, taxi_c)
    stations = [(obs[i], obs[i+1]) for i in range(2, 10, 2)]
    passenger_visible = obs[14]
    destination_visible = obs[15]
    wall_flags = obs[10:14]  # [north, south, east, west]

    # === Guess destination if visible (pre-pickup) ===
    if not has_passenger and destination_visible:
        for i, station in enumerate(stations):
            if abs(taxi_r - station[0]) + abs(taxi_c - station[1]) <= 1:
                guessed_destination_idx = i

    # === Dropoff logic ===
    if has_passenger and taxi_pos in stations and destination_visible:
        has_passenger = False
        phase = 0
        visited_stations_phase.clear()
        guessed_destination_idx = None
        return 5  # Dropoff

    # === Pickup logic ===
    if not has_passenger and taxi_pos in stations and passenger_visible:
        has_passenger = True
        phase = 1
        visited_stations_phase.clear()
        current_target_idx = guessed_destination_idx if guessed_destination_idx is not None else 0
        return 4  # Pickup

    # === Target management ===
    if taxi_pos == stations[current_target_idx]:
        visited_stations_phase.add(current_target_idx)
        if len(visited_stations_phase) < 4:
            for i in range(1, 5):
                next_idx = (current_target_idx + i) % 4
                if next_idx not in visited_stations_phase:
                    current_target_idx = next_idx
                    break
        random_walk_steps = 0

    target_station = stations[current_target_idx]
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

    # === Random walk (when stuck or surrounded) ===
    random_walk_steps += 1
    valid_random_moves = []
    for a in range(4):
        move = DIRECTION_VECTORS[a]
        next_pos = (taxi_r + move[0], taxi_c + move[1])
        if not wall_flags[a] and next_pos not in recent_positions:
            valid_random_moves.append(a)

    if valid_random_moves:
        action = random.choice(valid_random_moves)
        next_vec = DIRECTION_VECTORS[action]
        next_pos = (taxi_r + next_vec[0], taxi_c + next_vec[1])
        recent_positions.append(next_pos)
        return action

    # === Fallback ===
    return random.choice([4, 5])  # attempt pickup/dropoff if fully stuck