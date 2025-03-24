import pickle
import numpy as np
import random
with open("q_table_safe_clean.pkl", "rb") as f:
    Q = pickle.load(f)

def encode_state(obs):
    wall_flags = tuple(obs[10:14])
    passenger_visible = obs[14]
    destination_visible = obs[15]
    taxi_pos = (obs[0], obs[1])
    stations = [(obs[i], obs[i+1]) for i in range(2, 10, 2)]

    at_station = taxi_pos in stations
    at_passenger = at_station and passenger_visible
    at_destination = at_station and destination_visible

    return (wall_flags, at_passenger, at_destination, passenger_visible)

def get_action(obs):
    state = encode_state(obs)

    # Extract wall flags to ensure safe moves
    obstacle_north = obs[10]
    obstacle_south = obs[11]
    obstacle_east  = obs[12]
    obstacle_west  = obs[13]

    valid_moves = []
    if obstacle_south == 0: valid_moves.append(0)  # South
    if obstacle_north == 0: valid_moves.append(1)  # North
    if obstacle_east  == 0: valid_moves.append(2)  # East
    if obstacle_west  == 0: valid_moves.append(3)  # West

    # With small probability, take a random valid action instead of the greedy one
    if state in Q:
        return int(np.argmax(Q[state]))
    else:
        return random.choice(valid_moves) if valid_moves else random.choice([0, 1, 2, 3])