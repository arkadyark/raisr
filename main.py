import os
from heuristics import *
from skirace import set_race
from search import *

if __name__ == '__main__':
    """
    SkiRace Problem Set, for testing
    """
    PROBLEMS = (
        set_race(3, ((1, 3), (-1, 6))),
        set_race(2, ((1, 5), (-1, 10), (1, 15), (-1, 20), (1, 26), (-4, 32), (-2, 38), (-4, 44)))
        #set_race(3, ((1, 3), (-1, 9), (2, 15), (-2, 25), (2, 35), (-2, 45), (2, 55), (-2, 65), (2, 75), (-2, 85), (2, 95), (-2, 105))),
        #set_race(3, ((4, 4), (-4, 12), (4, 20), (-4, 28)))
    )

    for i in range(len(PROBLEMS)):
        print("******************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]
        weight = 10
        final = anytime_weighted_astar(s0, heur_fn=heur_slightly_less_dumb, weight=weight, timebound=3000)

        if final:
            final.plot_path()
