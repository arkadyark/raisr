from skirace import DEGREES_PER_SECOND, BRANCHING_FACTOR
from search import anytime_weighted_astar
import math
import copy
import physics

INF = float('inf')
preprocessing = {}
def heur_dumb(state):
    return 0 if is_worthwhile(state) else INF

def heur_slightly_less_dumb(state):
    if state.next_gate == None: return 0
    if (state.pos == (0, 0)):
        prev_gate = None
        for gate in reversed(state.all_gates):
            if not prev_gate:
                preprocessing[gate] = 0
                prev_gate = gate
            else:
                preprocessing[gate] = preprocessing[prev_gate] + euclidean_distance(gate, prev_gate)
    makeable, x_distance = is_gate_makeable(state)
    if makeable:
        return 1/state.v * (euclidean_distance(state.pos, state.next_gate) + preprocessing[state.next_gate])
    else:
        return INF

def projected_distance(pos, direction, next_gate):
    return 0

def euclidean_distance(v1, v2):
    return ((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)**(0.5)

def is_gate_makeable(state):
    if state.next_gate == None: return True
    prev_pos = state.pos
    p = state.pos
    v = state.v
    angle = state.action
    v, p = physics.execute_step(angle, v, p)

    while p[1] < state.next_gate[1]:
        min_angle = -DEGREES_PER_SECOND * physics.dt / 2. + angle
        step = DEGREES_PER_SECOND * physics.dt / (BRANCHING_FACTOR - 1)
        possible_angles = [min_angle + i * step for i in range(BRANCHING_FACTOR)]
        # Filter out invalid angles - can only go down the hill
        possible_angles = [a for a in possible_angles if -math.pi/2 <= a <= math.pi/2]
        #if p[0] < state.next_gate[0]:
        if state.gates.index(state.next_gate) % 2 == 0:
            angle = min(possible_angles)
        else:
            angle = max(possible_angles)

        prev_pos = p
        v , p = physics.execute_step(angle, v, p )

    x_dist = abs(state.next_gate[0] - p[0])
    if state.gates.index(state.next_gate) % 2 == 0:
        if (state.next_gate[0] - prev_pos[0]) * (p[1] - prev_pos[1]) < (state.next_gate[1]- prev_pos[1]) * (p[0] - prev_pos[0]):
            return True, x_dist
    else:
        if (state.next_gate[0] - prev_pos[0]) * (p[1] - prev_pos[1]) > (state.next_gate[1]- prev_pos[1]) * (p[0] - prev_pos[0]):
            return True, x_dist
    return False, None
