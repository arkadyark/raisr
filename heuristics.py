from skirace import DEGREES_PER_SECOND, BRANCHING_FACTOR
from search import anytime_weighted_astar
import math
import copy
import physics

INF = float('inf')

def heur_dumb(state):
    return 0 if is_worthwhile(state) else INF

def heur_slightly_less_dumb(state):
    if is_gate_makeable(state):
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
    prev_pos = None
    p = state.pos
    v = state.v
    angle = state.action

    while p[1] < state.next_gate[1]:
        min_angle = -DEGREES_PER_SECOND * physics.dt / 2. + angle
        step = DEGREES_PER_SECOND * physics.dt / (BRANCHING_FACTOR - 1)
        possible_angles = [min_angle + i * step for i in range(BRANCHING_FACTOR)]
        # Filter out invalid angles - can only go down the hill
        possible_angles = [a for a in possible_angles if -math.pi/2 <= a <= math.pi/2]
        if p[0] < state.next_gate[0]:
            angle = min(possible_angles)
        else:
            angle = max(possible_angles)

        prev_pos = p
        v , p = physics.execute_step(angle, v, p )

    if state.gates.index(state.next_gate) % 2 == 0:
        return (state.next_gate[0] - prev_pos[0]) * (p[1] - prev_pos[1]) < (state.next_gate[1]- prev_pos[1]) * (p[0] - prev_pos[0])
    else:
        return (state.next_gate[0] - prev_pos[0]) * (p[1] - prev_pos[1]) > (state.next_gate[1]- prev_pos[1]) * (p[0] - prev_pos[0])

    # # If we go all the way in one direction, can we make it?
    #estimated_time = euclidean_distance(state.next_gate, state.pos) / state.v
    #angle_to_gate = math.atan((state.next_gate[1] - state.pos[1])/(state.next_gate[0] - state.pos[0]))
    #return abs(angle_to_gate) < estimated_time * DEGREES_PER_SECOND
