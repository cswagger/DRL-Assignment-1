import pickle
import numpy as np
import random
with open("q_table_obstacle_safe.pkl", "rb") as f:
    Q = pickle.load(f)

def encode_state(obs):
    wall_flags = tuple(obs[10:14])
    passenger_visible = obs[14]
    destination_visible = obs[15]
    taxi_pos = (obs[0], obs[1])
    stations = [(obs[i], obs[i+1]) for i in range(2, 10, 2)]
    a = 5

    at_station = taxi_pos in stations
    at_passenger = at_station and passenger_visible
    at_destination = at_station and destination_visible

    return (wall_flags, at_passenger, at_destination)

def get_action(obs):
    state = encode_state(obs)
    if state in Q:
        return int(np.argmax(Q[state]))
    else:
        return random.choice([0, 1, 2, 3])  # fallback safe move
