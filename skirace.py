"""SkiRace routines.

    A) Class SkiRaceState

    A specializion of the StateSpace Class that is tailored to the game of SkiRace.

    B) class Direction

    An encoding of the directions of movement that are possible for robots in SkiRace.

    Code also contains a list of 40 SkiRace problems for the purpose of testing.
"""

from search import *

class SkiRaceState(StateSpace):

    def __init__(self, action, gval, parent, width, height, robot, boxes, storage, obstacles,
                 restrictions=None, box_colours=None, storage_colours=None):
        """
        Create a new SkiRace state.

        @param width: The room's X dimension (excluding walls).
        @param height: The room's Y dimension (excluding walls).
        @param robot: A tuple of the robot's location.
        @param boxes: A dictionary where the keys are the coordinates of each box, and the values are the index of that box's restriction.
        @param storage: A dictionary where the keys are the coordinates of each storage point, and the values are the index of that storage point.
        @param obstacles: A frozenset of all the impassable obstacles.
        @param restrictions: A tuple of frozensets of valid storage coordinates for each box. None means that all storage locations are valid.
        @param box_colours: A mapping from each box to the colour to use with the visualizer.
        @param storage_colours: A mapping from each storage location to the colour to use with the visualizer.
        """
        StateSpace.__init__(self, action, gval, parent)
        self.pos = (x, y)
        self.speed = speed
        self.next_gate = (gate_x, gate_y)
        self.time_so_far = time_so_far

    def successors(self):
        """
        Generate all the actions that can be performed from this state, and the states those actions will create.
        """
        successors = []
        #TODO: Add the successors!
        return successors

    def hashable_state(self):
        """
        Return a data item that can be used as a dictionary key to UNIQUELY represent a state.
        """
        return hash((self.robot, frozenset(self.boxes.items())))

def skirace_goal_state(state):
  """
  Returns True if we have reached a goal state.

  @param state: a sokoban state
  OUTPUT: True (if goal) or False (if not)
  """
  if state.restrictions is None:
    for box in state.boxes:
      if box not in state.storage:
        return False
    return True
  for box in state.boxes:
    if box not in state.restrictions[state.boxes[box]]:
      return False
  return True

def generate_coordinate_rect(x_start, x_finish, y_start, y_finish):
    """
    Generate tuples for coordinates in rectangle (x_start, x_finish) -> (y_start, y_finish)
    """
    coords = []
    for i in range(x_start, x_finish):
        for j in range(y_start, y_finish):
            coords.append((i, j))
    return coords

"""
SkiRace Problem Set, for testing
"""
PROBLEMS = (
    SkiRaceState("START", 0, None, 4, 4, # dimensions
                 (0, 3), #robot
                 {(1, 2): 0, (1, 1): 1}, #boxes
                 {(2, 1): 0, (2, 2): 1}, #storage
                 frozenset(((0, 0), (1, 0), (3, 3))), #obstacles
                 (frozenset(((2, 1),)), frozenset(((2, 2),))), #restrictions,
                 {0: 'cyan', 1: 'magenta'}, #box colours
                 {0: 'cyan', 1: 'magenta'} #storage colours
                 ),
    SkiRaceState("START", 0, None, 6, 4, # dimensions
             (5, 3), #robot
             {(1, 1): 0, (3, 1): 1}, #boxes
             {(2, 0): 0, (2, 2): 1}, #storage
             frozenset(((2, 1), (0, 0), (5, 0), (0, 3), (1, 3), (2, 3), (3, 3))), #obstacles
             (frozenset(((2, 0),)), frozenset(((2, 2),))), #restrictions,
             {0: 'cyan', 1: 'magenta'}, #box colours
             {0: 'cyan', 1: 'magenta'} #storage colours
             ),
    SkiRaceState("START", 0, None, 5, 4, # dimensions
             (0, 3), #robot
             {(2, 1): 0, (3, 1): 1}, #boxes
             {(2, 1): 0, (3, 1): 1}, #storage
             frozenset(((0, 0), (4, 0), (2, 3), (3, 3), (4, 3))), #obstacles
             (frozenset(((3, 1),)), frozenset(((2, 1),))), #restrictions,
             {0: 'cyan', 1: 'magenta'}, #box colours
             {1: 'cyan', 0: 'magenta'} #storage colours
             ),
    SkiRaceState("START", 0, None, 5, 5, # dimensions
                 (2, 1), # robot
                 {(1, 1): 0, (1, 3): 1, (3, 1): 2, (3, 3): 3}, #boxes
                 {(0, 0): 0, (0, 4): 1, (4, 0): 2, (4, 4): 3}, #storage
                 frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4))), #obstacles
                 None #restrictions
                 ),
    SkiRaceState("START", 0, None, 5, 5, # dimensions
                 (4, 0), #robot
                 {(3, 1): 0, (3, 2): 1, (3, 3): 2}, #boxes
                 {(0, 0): 0, (0, 2): 1, (0, 4): 2}, #storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4))), #obstacles
                 None #restrictions
                 ),
    SkiRaceState("START", 0, None, 5, 5, # dimensions
                 (4, 0), #robot
                 {(3, 1): 0, (3, 2): 1, (3, 3): 2}, #boxes
                 {(0, 0): 0, (0, 2): 1, (0, 4): 2}, #storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4))), #obstacles
                 None #restrictions
                 ),
    SkiRaceState("START", 0, None, 6, 4, # dimensions
         (5, 3), #robot
         {(3, 1): 0, (2, 2): 1, (3, 2): 2, (4, 2): 3}, #boxes
         {(0, 0): 0, (2, 0): 1, (1, 0): 2, (1, 1): 3}, #storage
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                   + generate_coordinate_rect(0, 3, 3, 4))), #obstacles
         (frozenset(((0, 0),)), frozenset(((2, 0),)), frozenset(((1, 0),)), frozenset(((1, 1),))), #restrictions,
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'}, #box colours
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'} #storage colours
         ),
    SkiRaceState("START", 0, None, 6, 4, # dimensions
         (5, 3), #robot
         {(3, 1): 0, (2, 2): 1, (3, 2): 2, (4, 2): 3}, #boxes
         {(0, 0): 0, (2, 0): 1, (1, 0): 2, (1, 1): 3}, #storage
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                   + generate_coordinate_rect(0, 3, 3, 4))), #obstacles
         (frozenset(((0, 0),)), frozenset(((2, 0),)), frozenset(((1, 0),)), frozenset(((0, 0), (2, 0), (1, 0), (1, 1),))), #restrictions,
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'normal'}, #box colours
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'} #storage colours
         ),
    SkiRaceState("START", 0, None, 8, 6, # dimensions
         (1, 2), #robot
         {(1, 3): 0, (2, 3): 1, (3, 3): 2, (4, 3): 3, (5, 3): 4}, #boxes
         {(7, 0): 0, (7, 1): 1, (7, 2): 2, (7, 3): 3, (7, 4): 4}, #storage
         frozenset((generate_coordinate_rect(0, 7, 0, 2) + [(0, 2), (6, 2), (7, 5)]
         + generate_coordinate_rect(0, 5, 5, 6))), #obstacles
         (frozenset(((7, 0),)), frozenset(((7, 1),)), frozenset(((7, 2),)), frozenset(((7, 3),)), frozenset(((7, 4),))), #restrictions,
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green'}, #box colours
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green'} #storage colours
         ),
    SkiRaceState("START", 0, None, 6, 5, # dimensions
         (5, 2), #robot
         {(3, 1): 0, (3, 2): 1, (3, 3): 2, (4, 2): 3}, #boxes
         {(1, 2): 0, (2, 2): 1, (3, 2): 2, (0, 2): 3}, #storage
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                    + generate_coordinate_rect(3, 6, 4, 5))
                    + [(1, 1), (1, 3)]), #obstacles
         (frozenset(((1, 2),)), frozenset(((2, 2),)), frozenset(((3, 2),)), frozenset(((0, 2),)), frozenset(((7, 4),))), #restrictions,
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green'}, #box colours
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green'} #storage colours
         ),
    )

"""
SkiRace Turn: encodes directions of movement that are possible for each robot.
"""
class Turn():
    """
    A turn in the course.
    """

    def __init__(self, L_x, L_y, t):
        """
        Creates a new direction.
        @param name: The direction's name.
        @param delta: The coordinate modification needed for moving in the specified direction.
        """
        self.L_x = L_x
        self.L_y = L_y
        self.t = t

    def __hash__(self):
        """
        The hash method must be implemented for actions to be inserted into sets
        and dictionaries.
        @return: The hash value of the action.
        """
        return hash(self.name)

    def __str__(self):
        """
        @return: The string representation of this object when *str* is called.
        """
        return str(self.name)

    def __repr__(self):
        return self.__str__()

    def move(self, race_state):
        """
        Execute the current turn on the given race state, returning the resulting state
        """
        #TODO

