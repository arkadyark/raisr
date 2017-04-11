import os
from heuristics import *
from skirace import set_race
from search import *
from visualizer import *

if __name__ == '__main__':
    """
    SkiRace Problem Set, for testing
    """
    PROBLEMS = (
# straight top section, turny bottom section
        # ANCEDOTAL EXPERIMENTS:
        set_race(2, ((0, 5), (0, 10), (0, 15), (0, 20), (0, 26), (-6, 32), (-2, 38), (-4, 44))),
        # less straight top section, turny bottom section
        #set_race(2, ((1, 5), (-1, 10), (1, 15), (-1, 20), (1, 26), (-6, 32), (-2, 38), (-4, 44))),

        #progressively tighter course (by height)
        set_race(2, ( (5, 5), (0, 9), (5, 13), (0, 16)))
        # START SPEED EXPERIMENTS:
        # set_race(2, ((4, 4), (0, 12), (4, 20), (0, 28))),
        # set_race(3, ((4, 4), (0, 12), (4, 20), (0, 28))),
        # set_race(4, ((4, 4), (0, 12), (4, 20), (0, 28))),
        # set_race(5, ((4, 4), (0, 12), (4, 20), (0, 28))),
        # set_race(6, ((4, 4), (0, 12), (4, 20), (0, 28))),
        # set_race(10, ((4, 4), (0, 12), (4, 20), (0, 28)))
        # END OF INCLINE EXPERIMENTS
        # #GATES EXPERIMENTS
        #set_race(4, ((4, 4), (0, 12), (4, 20), (0, 28))),
        #set_race(4, ((4, 4), (0, 12), (4, 20), (0, 28), (4, 36))),
        #set_race(4, ((4, 4), (0, 12), (4, 20), (0, 28), (4, 36), (0, 42))),
        #set_race(4, ((4, 4), (0, 12), (4, 20), (0, 28), (4, 36), (0, 42), (4, 50))),
        #set_race(4, ((4, 4), (0, 12), (4, 20), (0, 28), (4, 36), (0, 42), (4, 50), (0,58)))
        # END #GATES EXPERIMENTS

        # Y-COMPRESSION EXPERIMENTS
        # set_race(4, ((4, 4), (0, 12), (4, 20), (0, 28))),
        # set_race(4, ((4, 4), (0, 11), (4, 18), (0, 25))),
        # set_race(4, ((4, 4), (0, 10), (4, 16), (0, 22))),
        # set_race(4, ((4, 4), (0, 9), (4, 14), (0, 19))),
        # set_race(4, ((4, 4), (0, 8), (4, 12), (0, 16))),
        # set_race(4, ((4, 4), (0, 7), (4, 10), (0, 13)))
        # END Y-COMPRESSION EXPERIMENTS

        # X-COMPRESSION EXPERIMENTS
        # set_race(4, ((4, 4), (0, 12), (4, 20), (0, 28))),
        # set_race(4, ((5, 4), (0, 12), (5, 20), (0, 28))),
        # set_race(4, ((6, 4), (0, 12), (6, 20), (0, 28))),
        # set_race(4, ((7, 4), (0, 12), (4, 20), (0, 28))),
        # set_race(4, ((8, 4), (0, 12), (8, 20), (0, 28)))
        # END X-COMPRESSION EXPERIMENTS

        # constant width, incline of 3
        #set_race(3, ((4, 4), (-4, 12), (4, 20), (-4, 28))),
    )

    for i in range(len(PROBLEMS)):
        print("******************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]
        weight = 10
        final = anytime_weighted_astar(s0, heur_fn=heur_slightly_less_dumb, weight=weight, timebound=3000)

        if final:
            #final.plot_path()
            vis = Visualizer(final)
