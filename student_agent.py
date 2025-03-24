import random

step = 0
has_passenger = False

def is_on_station(pos, stations):
    return pos in stations

def is_isolated_station(pos, stations):
    r, c = pos
    for s in stations:
        if s == pos:
            continue
        sr, sc = s
        if abs(sr - r) + abs(sc - c) == 1:
            return False  # adjacent station exists
    return True

def get_action(obs):
    global step, has_passenger
    step += 1

    taxi_r, taxi_c = obs[0], obs[1]
    taxi_pos = (taxi_r, taxi_c)
    stations = [(obs[i], obs[i+1]) for i in range(2, 10, 2)]

    passenger_visible = obs[14]
    destination_visible = obs[15]

    # Attempt pickup if valid
    if not has_passenger and passenger_visible and is_on_station(taxi_pos, stations) and is_isolated_station(taxi_pos, stations):
        has_passenger = True
        return 4  # Pickup

    # Attempt dropoff if valid
    if has_passenger and destination_visible and is_on_station(taxi_pos, stations) and is_isolated_station(taxi_pos, stations):
        has_passenger = False
        return 5  # Dropoff

    # Extract obstacle info
    obstacle_north = obs[10]
    obstacle_south = obs[11]
    obstacle_east  = obs[12]
    obstacle_west  = obs[13]

    # Build list of safe movement directions
    valid_moves = []
    if obstacle_south == 0:
        valid_moves.append(0)  # South
    if obstacle_north == 0:
        valid_moves.append(1)  # North
    if obstacle_east == 0:
        valid_moves.append(2)  # East
    if obstacle_west == 0:
        valid_moves.append(3)  # West

    if valid_moves:
        return random.choice(valid_moves)
    else:
        return random.choice([4, 5])  # fallback if stuck
