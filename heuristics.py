from skirace import DEGREES_PER_SECOND
from search import anytime_weighted_astar
import math
import copy

INF = float('inf')

def heur_dumb(state):
    return 0 if is_worthwhile(state) else INF

def heur_slightly_less_dumb(state):
    if is_worthwhile(state) and is_gate_makeable(state):
        if state.next_gate != None:
            return -state.v * euclidean_distance(state.pos, state.next_gate)
        else:
            return -state.v
    else:
        return INF

def euclidean_distance(v1, v2):
    return ((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)**(0.5)

def is_gate_makeable(state):
    if state.next_gate == None: return True
    # If we go all the way in one direction, can we make it?
    estimated_time = euclidean_distance(state.next_gate, state.pos) / state.v
    angle_to_gate = math.atan((state.next_gate[1] - state.pos[1])/(state.next_gate[0] - state.pos[0]))
    return abs(angle_to_gate) < estimated_time * DEGREES_PER_SECOND

def is_worthwhile(state):
    if state.next_gate == None: return True
    if state.next_gate[0] < state.pos[0]:
        return state.action > 0
    else:
        return state.action < 0
