import random
from collections import deque
import heapq


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


class SearchAgent:
    """
    Goal-Based / Planning Search Agent.

    This agent uses uninformed search algorithms:
        - Breadth-First Search (BFS)
        - Depth-First Search (DFS)
        - Uniform-Cost Search (UCS)

    The agent receives the global state of the environment
    and creates an offline plan to reach food.
    """

    def __init__(self):

        # Stores the sequence of actions to execute
        self.plan = []

        # Algorithm currently being used
        # Change this to BFS, DFS, or UCS
        self.active_algo = 'BFS'

    # ==================================================
    # COMMON HELPER FUNCTION
    # ==================================================

    def get_neighbors(self, position, grid_size, walls):
        """
        Return all valid neighboring states.

        Each neighbor is returned as:

            (action, new_position)

        Example:
            ('Up', (0, 1))
        """

        width, height = grid_size

        x, y = position

        possible_moves = [
            ('Up', (x, y + 1)),
            ('Down', (x, y - 1)),
            ('Left', (x - 1, y)),
            ('Right', (x + 1, y))
        ]

        neighbors = []

        for action, new_position in possible_moves:

            nx, ny = new_position

            # Check grid boundaries
            if nx < 0 or nx >= width:
                continue

            if ny < 0 or ny >= height:
                continue

            # Check walls
            if new_position in walls:
                continue

            neighbors.append(
                (action, new_position)
            )

        return neighbors

    # ==================================================
    # BFS
    # ==================================================

    def bfs_search(self, start, goal, walls, grid_size):
        """
        Breadth-First Search.

        BFS uses a FIFO queue.

        It explores the shallowest nodes first and
        therefore finds the shortest path when all
        actions have equal cost.
        """

        walls = set(walls)

        # FIFO queue
        frontier = deque()

        # Store:
        # current position + path taken
        frontier.append(
            (start, [])
        )

        # Reached set prevents repeated states
        reached = {start}

        while frontier:

            # Remove from the front
            current, path = frontier.popleft()

            # Goal test
            if current == goal:
                return path

            # Expand current state
            for action, next_position in self.get_neighbors(
                current,
                grid_size,
                walls
            ):

                # Only visit a state once
                if next_position not in reached:

                    reached.add(next_position)

                    new_path = path + [action]

                    frontier.append(
                        (next_position, new_path)
                    )

        # Goal cannot be reached
        return None

    # ==================================================
    # DFS
    # ==================================================

    def dfs_search(self, start, goal, walls, grid_size):
        """
        Depth-First Search.

        DFS uses a LIFO stack.

        It explores deeper nodes first.
        """

        walls = set(walls)

        # LIFO stack
        frontier = []

        frontier.append(
            (start, [])
        )

        # Reached set
        reached = {start}

        while frontier:

            # Remove the last item
            current, path = frontier.pop()

            # Goal test
            if current == goal:
                return path

            # Expand current state
            for action, next_position in self.get_neighbors(
                current,
                grid_size,
                walls
            ):

                if next_position not in reached:

                    reached.add(next_position)

                    new_path = path + [action]

                    frontier.append(
                        (next_position, new_path)
                    )

        return None

    # ==================================================
    # UCS
    # ==================================================

    def ucs_search(self, start, goal, walls, grid_size):
        """
        Uniform-Cost Search.

        UCS uses a priority queue.

        Nodes are ordered according to total path
        cost g(n).

        Every movement in this grid has a cost of 1.
        """

        walls = set(walls)

        # Priority queue
        frontier = []

        # Used to break ties between equal-cost nodes
        counter = 0

        # Start state has cost 0
        heapq.heappush(
            frontier,
            (0, counter, start, [])
        )

        # Store the cheapest cost found for each state
        reached = {
            start: 0
        }

        while frontier:

            # Remove lowest-cost node
            cost, _, current, path = heapq.heappop(
                frontier
            )

            # Goal test
            if current == goal:
                return path

            # Expand current state
            for action, next_position in self.get_neighbors(
                current,
                grid_size,
                walls
            ):

                # Every movement costs 1
                new_cost = cost + 1

                # Add state if:
                # 1. It has never been reached
                # OR
                # 2. We found a cheaper path
                if (
                    next_position not in reached
                    or new_cost < reached[next_position]
                ):

                    reached[next_position] = new_cost

                    counter += 1

                    new_path = path + [action]

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            counter,
                            next_position,
                            new_path
                        )
                    )

        return None

    # ==================================================
    # FIND CLOSEST FOOD
    # ==================================================

    def find_closest_food(self, start, food_positions):
        """
        Select the closest food using Manhattan distance.
        """

        if not food_positions:
            return None

        closest_food = min(
            food_positions,
            key=lambda food:
                abs(food[0] - start[0])
                + abs(food[1] - start[1])
        )

        return closest_food

    # ==================================================
    # SENSE AND ACT
    # ==================================================

    def sense_and_act(self, percept: dict) -> str:
        """
        Create a complete plan when the current plan
        is empty.

        Then execute one action from the plan.
        """

        # --------------------------------------------------
        # Create a new plan if required
        # --------------------------------------------------

        if not self.plan:

            # Current agent position
            start = tuple(
                percept['agent_pos']
            )

            # Get all food positions
            food_positions = [
                tuple(food)
                for food in percept['all_food']
            ]

            # If there is no food
            if not food_positions:
                return 'Up'

            # Find closest food
            goal = self.find_closest_food(
                start,
                food_positions
            )

            # Global environment information
            grid_size = percept['grid_size']
            walls = percept['walls']

            # --------------------------------------------------
            # Select search algorithm
            # --------------------------------------------------

            if self.active_algo == 'BFS':

                self.plan = self.bfs_search(
                    start,
                    goal,
                    walls,
                    grid_size
                )

            elif self.active_algo == 'DFS':

                self.plan = self.dfs_search(
                    start,
                    goal,
                    walls,
                    grid_size
                )

            elif self.active_algo == 'UCS':

                self.plan = self.ucs_search(
                    start,
                    goal,
                    walls,
                    grid_size
                )

            else:

                raise ValueError(
                    "Unknown search algorithm. "
                    "Use BFS, DFS, or UCS."
                )

            # If no path was found
            if self.plan is None:
                self.plan = []

        # --------------------------------------------------
        # Execute next action
        # --------------------------------------------------

        if self.plan:

            return self.plan.pop(0)

        # Fallback action
        return 'Up'