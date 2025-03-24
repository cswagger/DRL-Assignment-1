# # student_agent.py
# import pickle
# import numpy as np

# with open("q_table_compact.pkl", "rb") as f:
#     Q = pickle.load(f)

# ACTIONS = [0, 1, 2, 3, 4, 5]

# # Internal memory
# has_passenger = False
# current_target_idx = 0
# stations = []

# def sign(x):
#     if x < 0: return -1
#     elif x > 0: return 1
#     return 0

# def encode_state(obs, has_passenger, target):
#     taxi_r, taxi_c = obs[0], obs[1]
#     dx = target[0] - taxi_r
#     dy = target[1] - taxi_c
#     target_dir = (sign(dx) + 1, sign(dy) + 1)

#     obstacle_north = int(obs[10])
#     obstacle_south = int(obs[11])
#     obstacle_east  = int(obs[12])
#     obstacle_west  = int(obs[13])

#     at_passenger = int(obs[14] and not has_passenger and (taxi_r, taxi_c) in [(obs[i], obs[i+1]) for i in range(2, 10, 2)])
#     at_destination = int(obs[15] and has_passenger and (taxi_r, taxi_c) in [(obs[i], obs[i+1]) for i in range(2, 10, 2)])

#     return (target_dir[0], target_dir[1],
#             obstacle_north, obstacle_south, obstacle_east, obstacle_west,
#             at_passenger, at_destination, int(has_passenger))

# def get_action(obs):
#     global has_passenger, current_target_idx, stations

#     if not stations:
#         stations = [(obs[i], obs[i+1]) for i in range(2, 10, 2)]

#     taxi_r, taxi_c = obs[0], obs[1]
#     taxi_pos = (taxi_r, taxi_c)

#     if not has_passenger:
#         if taxi_pos == stations[current_target_idx] and not obs[14]:
#             current_target_idx = (current_target_idx + 1) % 4
#         target = stations[current_target_idx]
#     else:
#         target = obs[8], obs[9]  # destination remains fixed once picked up

#     state = encode_state(obs, has_passenger, target)

#     # Avoid invalid actions
#     invalid_actions = set()
#     if state[2]: invalid_actions.add(1)  # north
#     if state[3]: invalid_actions.add(0)  # south
#     if state[4]: invalid_actions.add(2)  # east
#     if state[5]: invalid_actions.add(3)  # west
#     if state

#     q_vals = Q.get(state, np.zeros(len(ACTIONS))).copy()
#     for a in invalid_actions:
#         q_vals[a] = -np.inf
#     action = int(np.argmax(q_vals))

#     # Inferred passenger pickup/drop-off logic
#     if not has_passenger and action == 4 and state[6]:
#         has_passenger = True
#         current_target_idx = 0
#     elif has_passenger and action == 5 and state[7]:
#         has_passenger = False
#         current_target_idx = 0
#         stations = []

#     return action
# student_agent.py
# Slightly smarter oscillating agent that avoids walls

import random

step = 0
ACTIONS = [0, 1, 2, 3, 4, 5]  # [South, North, East, West, Pickup, Dropoff]

def get_action(obs):
    global step
    step += 1

    # Extract obstacle info
    obstacle_north = obs[10]
    obstacle_south = obs[11]
    obstacle_east  = obs[12]
    obstacle_west  = obs[13]

    # Build a list of safe movement directions
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
        # All directions blocked? Try pickup or dropoff anyway
        return random.choice([4, 5])