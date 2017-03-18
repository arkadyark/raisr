import os
from search import *
from skirace import *

INF = float('inf')

def heur_dumb(state):
    return 0

def heur_slightly_less_dumb(state):
    return state.pos[1]

def fval_function(sN, weight):
    return weight*sN.hval + sN.state.gval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a ski race state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    g = INF
    g_plus_h = INF
    s = False
    s_found = False
    start_time = os.times()[0]
    se = SearchEngine('custom', 'full')
    se.init_search(initial_state, goal_fn=skirace_goal_state, heur_fn=heur_fn, fval_function = lambda sN: fval_function(sN, weight))
    time_used = 0
    while time_used < timebound:
        time_used = os.times()[0] - start_time
        current_s = se.search(timebound - time_used, (g, INF, g_plus_h))
        if current_s:
            g = current_s.gval - 1
            g_plus_h = g + heur_fn(current_s)
            s_found = True
        else:
            # Nothing better found! Return the best we found
            if s_found:
                return s
        s = current_s
    return s

if __name__ == '__main__':
    """
    SkiRace Problem Set, for testing
    """
    PROBLEMS = (
        set_race(5, ((3, 3), (-3, 6))),
        set_race(5, ((3, 3), (-3, 9), (3, 15), (-3, 21))),
        set_race(3, ((4, 4), (-4, 12), (4, 20), (-4, 28)))
    )

    for i in range(len(PROBLEMS)):
        print("******************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]
        weight = 10
        final = anytime_weighted_astar(s0, heur_fn=heur_slightly_less_dumb, weight=weight, timebound=150)

        if final:
            final.plot_path()
