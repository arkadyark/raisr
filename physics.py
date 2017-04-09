import math

M = 50.
G = 9.8
AIR_DRAG = 0.3
FRICTION = 0.3 #0.27
DEG_TO_RAD = math.pi / 180
THETA = 30 * DEG_TO_RAD
dt = 0.15

def execute_step(control_angle, v_initial, pos):
    control_angle += math.pi/2 # Angle relative to vertical
    v = [v_initial * math.cos(control_angle), v_initial * math.sin(control_angle)]
    pos = (pos[0] + v[0] * dt, pos[1] + v[1] * dt)
    a = [-AIR_DRAG * v[0]**2/M - G*math.cos(THETA)*FRICTION*math.cos(control_angle), \
         G*math.sin(THETA) - AIR_DRAG*v[1]**2/M - G*math.cos(THETA)*FRICTION*math.sin(control_angle)]
    v_final = (v[0] + a[0]*dt, v[1] + a[1]*dt)
    v_final = math.sqrt(v_final[0]**2 + v_final[1]**2)
    return v_final, pos

if __name__ == '__main__':
    # Demo physics
    import matplotlib.pyplot as plt
    pos = (0, 0)
    xs = []
    ys = []
    v = 10

    print("TURN 1")
    for i in range(50):
        v, pos = execute_step((30 - 100*i/50.) * DEG_TO_RAD, v, pos)
        xs.append(pos[0])
        ys.append(pos[1])

    print("TURN 2")
    for i in range(50):
        v, pos = execute_step((-70 + 100*i/50.) * DEG_TO_RAD, v, pos)
        xs.append(pos[0])
        ys.append(pos[1])

    print("TURN 3")
    for i in range(50):
        v, pos = execute_step((30 - 100*i/50.) * DEG_TO_RAD, v, pos)
        xs.append(pos[0])
        ys.append(pos[1])

    print("TURN 4")
    for i in range(50):
        v, pos = execute_step((-70 + 100*i/50.) * DEG_TO_RAD, v, pos)
        xs.append(pos[0])
        ys.append(pos[1])

    plt.plot(xs, ys)
    plt.show()
