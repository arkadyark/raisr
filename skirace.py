"""SkiRace routines.

    A) Class SkiRaceState

    A specializion of the StateSpace Class that is tailored to the game of SkiRace.

    B) class Direction

    An encoding of the directions of movement that are possible for robots in SkiRace.

    Code also contains a list of 40 SkiRace problems for the purpose of testing.
"""

from search import *
import physics
import math

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
        if pos[1] < gates[0][1]: return gates[0]
        for i in range(len(gates) - 1):
            if gates[i][1] < pos[1] < gates[i + 1][1]:
                return gates[i + 1]

    def successors(self):
        """
        Generate all the actions that can be performed from this state, and the states those actions will create.
        """
        successors = []
        angle = self.action
        # Generate 10 possible angles from -0.1 to 0.1 radians away
        # TODO: Parameterize this / relate to dt
        possible_angles = [angle + 0.02*i for i in range(-2, 3)]
        # Filter out invalid angles - can only go down the hill
        possible_angles = [a for a in possible_angles if -math.pi/2 <= a <= math.pi/2]
        for angle in possible_angles:
            v_next, pos_next = physics.execute_step(angle, self.v, self.pos)
            if self.goes_around_gate(pos_next, self.next_gate):
                next_state = SkiRaceState(angle, \
                        self.time_so_far + physics.dt, \
                        self, v_next, pos_next, self.gates)
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

    def plot_path(self):
        """
        Plot the solution
        """
        import matplotlib.pyplot as plt
        xs = []
        ys = []
        bounds = [min(i[0] for i in self.gates) - 5,
                max(i[0] for i in self.gates) + 5,
                0, max(i[1] for i in self.gates) + 5]
        parent = self.parent
        while parent:
            xs.insert(0, parent.pos[0])
            ys.insert(0, parent.pos[1])
            parent = parent.parent
        plt.plot(xs, ys)
        for i in range(len(self.gates) - 1):
            gate = self.gates[i]
            color = "b" if i % 2 else "r"
            plt.scatter(gate[0], gate[1], c=color)
        plt.plot((bounds[0], bounds[1]), (self.gates[-1][1], self.gates[-1][1]))
        plt.axis(bounds)
        plt.show()

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
    left_foot_last = len(gates) % 2 + 1
    finish_line = (gates[-1][0] + (-1)**(left_foot_last)*5,
            gates[-1][1] + 5)
    print(finish_line)
    return SkiRaceState(0, # initial angle
        0, # initial time
        None, # parent
        v_init, # initial speed
        (0, 0), # initial position
        gates + ((finish_line,)))

