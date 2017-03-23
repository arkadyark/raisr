INF = float('inf')

def heur_dumb(state):
    return 0 if is_worthwhile(state) else INF

def heur_slightly_less_dumb(state):
    if is_worthwhile(state):
        return -state.v
    else:
        return INF

def is_worthwhile(state):
    if state.next_gate == None: return True
    if state.next_gate[0] < state.pos[0]:
        return state.action > 0
    else:
        return state.action < 0
