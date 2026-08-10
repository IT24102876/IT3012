import random


class GreedyGridAgent:
    """A simple agent that moves randomly around the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """
    Simple Reflex Agent.

    The agent makes decisions only from the current percept.
    It does NOT maintain memory or history.
    """

    def sense_and_act(self, percept: dict) -> str:

        # Rule 1:
        # IF food is here THEN move Right
        if percept['food_here']:
            return 'Right'

        # Rule 2:
        # IF there is a wall ahead THEN turn Left
        if percept['wall_ahead']:
            return 'Left'

        # Rule 3:
        # ELSE move Forward (represented by Up)
        return 'Up'


class ModelBasedAgent:
    """
    Model-Based Agent.

    This agent maintains internal state about the environment.
    """

    def __init__(self):
        # Memory of cells that the agent has visited
        self.visited_cells = set()

        # Remember the previous action
        self.last_action = None

        # Current estimated position
        self.current_position = (0, 0)

        # Number of actions taken
        self.action_count = 0

    def sense_and_act(self, percept: dict) -> str:

        self.action_count += 1

        # --------------------------------------------------
        # Update internal state
        # --------------------------------------------------

        # Get current position from the percept.
        #
        # This is only used internally to demonstrate
        # the model-based agent.
        if 'agent_pos' in percept:
            self.current_position = tuple(percept['agent_pos'])

        # Add current position to memory
        self.visited_cells.add(self.current_position)

        # --------------------------------------------------
        # Condition-Action Rules using memory
        # --------------------------------------------------

        # Rule 1:
        # IF food is here THEN collect food
        if percept['food_here']:
            action = 'Right'

        # Rule 2:
        # IF wall is ahead
        elif percept['wall_ahead']:

            # If we previously turned Left and are facing
            # a wall again, choose another direction.
            if self.last_action == 'Left':
                action = 'Right'
            else:
                action = 'Left'

        # Rule 3:
        # If there is no wall, move forward
        else:
            action = 'Up'

        # Remember the action for the next step
        self.last_action = action

        return action