import math

M = 60
G = 9.8
AIR_DRAG = 0.15
FRICTION = 0.3

def make_turn(a, b, left_foot_turn):
    '''
    Function that creates a parameterized half-ellipse
    '''
    def turn(t):
        if left_foot_turn:
            return (a*math.sin(t*math.pi), -b*math.cos(t*math.pi) + b)
        else:
            return (-a*math.sin(t*math.pi), -b*math.cos(t*math.pi) + b)
    return turn

def get_duration(turn, t_final, v_initial, n_points=500):
    last_pos = turn(0)
    v = v_initial
    duration = 0
    for i in range(1, n_points):
        current_pos = turn(i/float(n_points))
        delta = (current_pos[0] - last_pos[0], current_pos[1] - last_pos[1])
        d = (delta[0]**2 + delta[1]**2)**(0.5)
        work_done = M*G*delta[1] - (AIR_DRAG*v**2 + M*G*FRICTION)*d
        print v**2, 2*work_done/M, M*G*delta[1], M*G*FRICTION*d, delta[1], d
        v_final = (max(v**2 + 2*work_done/M, 0))**(0.5)
        duration +=  2*d/(v + v_final)
        v = v_final
        last_pos = current_pos
    return duration, v

v = 1
t = 0
for i in range(100):
    turn = make_turn(1 + i, 1, i % 2)
    turn_t, v = get_duration(turn, v)
    t += turn_t
    print t, v
