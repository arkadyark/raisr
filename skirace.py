"""SkiRace routines.

    A) Class SkiRaceState

    A specializion of the StateSpace Class that is tailored to the game of SkiRace.

    B) class Direction

    An encoding of the directions of movement that are possible for robots in SkiRace.

    Code also contains a list of 40 SkiRace problems for the purpose of testing.
"""

from search import *
import physics

class SkiRaceState(StateSpace):
    def __init__(self, action, time_so_far, parent, v, pos, gates):
        """
        Create a new SkiRace state.
        """
        StateSpace.__init__(self, action, time_so_far, parent)
        self.v = v
        self.pos = pos
        self.gates = gates
        self.next_gate = self.get_next_gate(pos, gates)
        self.time_so_far = time_so_far

    def get_next_gate(self, pos, gates):
        """
        Return the next gate in the course
        """
        for i in range(len(gates) - 1):
            if gates[i][1] < pos[1] < gates[i + 1][1]:
                return gates[i + 1]

    def successors(self):
        """
        Generate all the actions that can be performed from this state, and the states those actions will create.
        """
        successors = []
        angle = math.atan(v[1] / v[0])
        # Generate 10 possible angles from -0.1 to 0.1 radians away
        # TODO: Parameterize this / relate to dt
        possible_angles = [angle + 0.02*i for i in range(-5, 6)]
        # Filter out invalid angles - can only go down the hill
        possible_angles = [a for a in possible_angles if 0 <= a <= math.pi]
        for angle in possible_angles:
            v_next, pos_next = physics.execute_step(angle, self.v, self.pos)
            if self.goes_around_gate(pos_next, self.next_gate):
                next_state = SkiRaceState(angle, \
                        self.time_so_far + physics.dt, \
                        self, v_next, pos_next, gates)
                successors.append(next_state)
        return successors

    def hashable_state(self):
        """
        Return a data item that can be used as a dictionary key to UNIQUELY represent a state.
        """
        return hash((self.pos, self.v, self.time_so_far))

    def goes_around_gate(self, pos, next_gate):
        """
        Return whether or not pos goes around the next gate
        """
        return True

def skirace_goal_state(state):
  """
  Returns True if we have crossed the finish line
  """
  return state.pos[1] > state.gates[-1][1]

def set_race(v_init, gates):
    """
    Returns initial state of a race, given the gates
    Add on a 'finish line' gate
    """
    left_foot_last = len(gates) % 2
    finish_line = (gates[-1][0] + (-1)**(left_foot_last)*10,
            gates[-1][1] + 10)
    return SkiRaceState(0, # initial angle
        0, # initial time
        None, # parent
        v_init, # initial speed
        (0, 0), # initial position
        frozenset(gates + tuple(finish_line)))

"""
SkiRace Problem Set, for testing
"""
PROBLEMS = (
    set_race(5, ((3, 3), (-3, 9), (3, 15), (-3, 21))),
    set_race(3, ((4, 4), (-4, 12), (4, 20), (-4, 28)))
)
