#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Sokoban warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
import os
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS, sokoban_goal_state #for Sokoban specific classes and problems
from heapq import *
from math import isinf

INF = float('inf')

#SOKOBAN HEURISTICS
def heur_displaced(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
      count += 1
    return count

def heur_manhattan_distance(state):
    '''admissible sokoban heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    sum_distance = 0
    for box in state.boxes:
        closest = INF
        for storage in state.storage:
            if state.restrictions and not storage in state.restrictions[state.boxes[box]]:
                continue
            manhattan_dist = abs(storage[0] - box[0]) + abs(storage[1] - box[1])
            if manhattan_dist < closest:
                closest = manhattan_dist
        sum_distance += closest
    return sum_distance

def heur_alternate(state):
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    if state.action in ("Start", "START", "start"):
        # On the first call, get all the distances
        heur_alternate.distances = preprocess(state)
        # Throw away the possible squares that are unreachable
        heur_alternate.restrictions = [[] for i in range(max(state.boxes.values()) + 1)]
        for box in state.boxes:
            for storage in state.storage:
                if (not state.restrictions or storage in state.restrictions[state.boxes[box]]) and heur_alternate.distances[box, storage] < 2**31:
                    heur_alternate.restrictions[state.boxes[box]].append(storage)

    if screwed(state, heur_alternate.distances):
        # If we get a deadlock, back off
        return INF

    occupied = []
    sum_distance = 0
    # Go through each box, in order of restriction
    for box in sorted(state.boxes, key=lambda k: len(heur_alternate.restrictions[state.boxes[k]])):

        # Try to find an unoccupied square
        closest = INF
        best = None
        for storage in state.storage:
            if not storage in heur_alternate.restrictions[state.boxes[box]] or storage in occupied:
                continue
            dist = heur_alternate.distances[box, storage]
            if dist < closest:
                closest = dist
                best = storage

        # If we couldn't find any unoccupied one, just pick any
        if best == None:
            for storage in state.storage:
                if not storage in heur_alternate.restrictions[state.boxes[box]]:
                    continue
                dist = heur_alternate.distances[box, storage]
                if dist < closest:
                    closest = dist
                    best = storage

        # If we still can't find anything, we're screwed
        if best == None:
            return closest
        occupied.append(best)
        sum_distance += closest

        # Add manhattan distance to get player to the box
        if best != box:
            sum_distance += abs(state.robot[0] - box[0]) + abs(state.robot[1] - box[1])
    return sum_distance

def screwed(state, distances):
    for box in state.boxes:
        valid_storage = False
        for storage in state.storage:
            if (state.restrictions and not storage in state.restrictions[state.boxes[box]]):
                continue
            if distances[box, storage] < 2**31:
                valid_storage = True
                break
        if not valid_storage:
            return True
    return False

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def out_of_bounds(a, obstacles, width, height):
    return a[0] < 0 or a[0] >= width or a[1] < 0 or a[1] >= height or a in obstacles

def shortest_path(a, b, obstacles, width, height):
    # Simple implementation of A* algorithm for shortest path
    # with manhattan_distance as a heuristic
    DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
    gscore = {a:0}
    fscore = {a:manhattan_distance(a,b)}
    frontier = []
    visited = set()
    parents = {}

    heappush(frontier, (fscore[a], a))
    while frontier:
        current = heappop(frontier)
        if current[1] == b:
            return current[0]

        current = current[1]
        visited.add(current)

        # Check if we are against walls or obstacles, in which case we cannot move in the opposite direction
        restrictions = (current[0] == width - 1 or (current[0] + 1, current[1]) in obstacles,
                current[0] == 0 or (current[0] - 1, current[1]) in obstacles, \
                current[1] == height - 1 or (current[0], current[1] + 1) in obstacles, \
                current[1] == 0 or (current[0], current[1] - 1) in obstacles)
        valid_directions = [DIRECTIONS[i] for i in range(len(DIRECTIONS)) if not restrictions[i]]

        for i,j in valid_directions:
            neighbor = (current[0] + i, current[1] + j)
            neighbor_g_score = gscore[current] + 1

            if out_of_bounds(neighbor, obstacles, width, height):
                continue
            if neighbor in visited:
                continue

            parents[neighbor] = current

            gscore[neighbor] = neighbor_g_score
            fscore[neighbor] = neighbor_g_score + manhattan_distance(neighbor, b)
            heappush(frontier, (fscore[neighbor], neighbor))

    return 2**31

def preprocess(state):
    # Preprocess the state to get the shortest_path ,istances from each square
    distances = {}
    for x in range(state.width):
        for y in range(state.height):
            if not (x, y) in state.obstacles:
                for storage in state.storage:
                    distances[(x, y), storage] = shortest_path((x, y), storage, state.obstacles, state.width, state.height)
    return distances

def fval_function(sN, weight):
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    return weight*sN.hval + sN.state.gval

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    g = INF
    s = False
    s_found = False
    start_time = os.times()[0]
    se = SearchEngine('best_first', 'full')
    se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn)
    #se.trace_on()
    time_used = 0
    while time_used < timebound:
        time_used = os.times()[0] - start_time
        current_s = se.search(timebound - time_used, (g,INF, INF))
        if current_s:
            g = current_s.gval - 1
            s_found = True
        else:
            if s_found:
                return s
        s = current_s
    return s

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10, silent=False):
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    g = INF
    g_plus_h = INF
    s = False
    s_found = False
    start_time = os.times()[0]
    se = SearchEngine('custom', 'full', silent=silent)
    se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function = lambda sN: fval_function(sN, weight))
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

if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")
  print("Running A-star")

  for i in range(0, 10): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    se.init_search(s0, goal_fn=sokoban_goal_state, heur_fn=heur_manhattan_distance)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit
  print("Running Anytime Weighted A-star")

  for i in range(0, 10):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10
    final = anytime_weighted_astar(s0, heur_fn=heur_alternate, weight=weight, timebound=timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")


