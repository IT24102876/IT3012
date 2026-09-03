import random
from collections import deque
import heapq

from logic_engine import KnowledgeBase


# ==========================================================
# GREEDY GRID AGENT
# ==========================================================

class GreedyGridAgent:
    """
    A simple agent that moves randomly around the grid.
    """

    def __init__(self):
        self.actions_pool = [
            'Up',
            'Down',
            'Left',
            'Right'
        ]

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(
            self.actions_pool
        )


# ==========================================================
# SIMPLE REFLEX AGENT
# ==========================================================

class SimpleReflexAgent:
    """
    Simple Reflex Agent.

    The agent makes decisions only from
    the current percept.
    """

    def sense_and_act(
        self,
        percept: dict
    ) -> str:

        # Rule 1:
        # IF food is here THEN move Right

        if percept['food_here']:
            return 'Right'

        # Rule 2:
        # IF wall ahead THEN turn Left

        if percept['wall_ahead']:
            return 'Left'

        # Rule 3:
        # Otherwise move Up

        return 'Up'


# ==========================================================
# MODEL BASED AGENT
# ==========================================================

class ModelBasedAgent:
    """
    Model-Based Agent.

    Maintains internal state about the environment.
    """

    def __init__(self):

        # Memory of visited cells
        self.visited_cells = set()

        # Previous action
        self.last_action = None

        # Current estimated position
        self.current_position = (0, 0)

        # Number of actions
        self.action_count = 0

    def sense_and_act(
        self,
        percept: dict
    ) -> str:

        self.action_count += 1

        # --------------------------------------------------
        # Update internal state
        # --------------------------------------------------

        if 'agent_pos' in percept:

            self.current_position = tuple(
                percept['agent_pos']
            )

        self.visited_cells.add(
            self.current_position
        )

        # --------------------------------------------------
        # Condition-Action Rules
        # --------------------------------------------------

        if percept['food_here']:

            action = 'Right'

        elif percept['wall_ahead']:

            if self.last_action == 'Left':

                action = 'Right'

            else:

                action = 'Left'

        else:

            action = 'Up'

        # Remember action
        self.last_action = action

        return action


# ==========================================================
# SEARCH AGENT
# ==========================================================

class SearchAgent:
    """
    Search / Planning Agent.

    Supports:

        BFS
        DFS
        UCS
        A*

    Practical 04 additionally uses a
    Knowledge Base and Forward Chaining
    to check whether a tile is logically
    feasible before expanding it.
    """

    def __init__(self):

        # Current plan
        self.plan = []

        # Selected algorithm
        self.active_algo = 'BFS'

        # Planning counter
        self.planning_count = 0

        # --------------------------------------------------
        # Knowledge Base
        # --------------------------------------------------

        self.kb = KnowledgeBase()

        # --------------------------------------------------
        # Practical 04 Rules
        # --------------------------------------------------

        # Rule 1:
        #
        # TargetVisible AND HasDust
        #             ->
        #        SafeToEngage

        self.kb.tell_rule(
            [
                'TargetVisible',
                'HasDust'
            ],
            'SafeToEngage'
        )

        # Rule 2:
        #
        # SafeToEngage AND BloodseekerMissing
        #             ->
        #              Retreat

        self.kb.tell_rule(
            [
                'SafeToEngage',
                'BloodseekerMissing'
            ],
            'Retreat'
        )

    # ======================================================
    # GET VALID NEIGHBOURS
    # ======================================================

    def get_neighbors(
        self,
        position,
        grid_size,
        walls
    ):

        """
        Return valid neighboring states.

        Each result:

            (action, new_position)
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

            # --------------------------------------------------
            # Boundary check
            # --------------------------------------------------

            if nx < 0 or nx >= width:
                continue

            if ny < 0 or ny >= height:
                continue

            # --------------------------------------------------
            # Wall check
            # --------------------------------------------------

            if new_position in walls:
                continue

            neighbors.append(
                (
                    action,
                    new_position
                )
            )

        return neighbors

    # ======================================================
    # BFS
    # ======================================================

    def bfs_search(
        self,
        start,
        goal,
        walls,
        grid_size
    ):

        """
        Breadth-First Search.
        """

        walls = set(walls)

        frontier = deque()

        frontier.append(
            (
                start,
                []
            )
        )

        reached = {
            start
        }

        while frontier:

            current, path = (
                frontier.popleft()
            )

            # Goal test
            if current == goal:

                return path

            # Expand node
            for action, next_position in (
                self.get_neighbors(
                    current,
                    grid_size,
                    walls
                )
            ):

                if next_position not in reached:

                    reached.add(
                        next_position
                    )

                    new_path = (
                        path + [action]
                    )

                    frontier.append(
                        (
                            next_position,
                            new_path
                        )
                    )

        return None

    # ======================================================
    # DFS
    # ======================================================

    def dfs_search(
        self,
        start,
        goal,
        walls,
        grid_size
    ):

        """
        Depth-First Search.
        """

        walls = set(walls)

        frontier = []

        frontier.append(
            (
                start,
                []
            )
        )

        reached = {
            start
        }

        while frontier:

            current, path = (
                frontier.pop()
            )

            # Goal test
            if current == goal:

                return path

            # Expand node
            for action, next_position in (
                self.get_neighbors(
                    current,
                    grid_size,
                    walls
                )
            ):

                if next_position not in reached:

                    reached.add(
                        next_position
                    )

                    new_path = (
                        path + [action]
                    )

                    frontier.append(
                        (
                            next_position,
                            new_path
                        )
                    )

        return None

    # ======================================================
    # UCS
    # ======================================================

    def ucs_search(
        self,
        start,
        goal,
        walls,
        grid_size
    ):

        """
        Uniform-Cost Search.

        Every movement has a cost of 1.
        """

        walls = set(walls)

        frontier = []

        counter = 0

        heapq.heappush(
            frontier,
            (
                0,
                counter,
                start,
                []
            )
        )

        reached = {
            start: 0
        }

        while frontier:

            cost, _, current, path = (
                heapq.heappop(
                    frontier
                )
            )

            # Goal test
            if current == goal:

                return path

            # Expand node
            for action, next_position in (
                self.get_neighbors(
                    current,
                    grid_size,
                    walls
                )
            ):

                new_cost = cost + 1

                if (
                    next_position not in reached
                    or new_cost < reached[
                        next_position
                    ]
                ):

                    reached[
                        next_position
                    ] = new_cost

                    counter += 1

                    new_path = (
                        path + [action]
                    )

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

    # ======================================================
    # A* HEURISTIC
    # ======================================================

    def manhattan_distance(
        self,
        position,
        goal
    ):

        """
        Manhattan distance:

        |x1 - x2| + |y1 - y2|
        """

        return (
            abs(position[0] - goal[0])
            +
            abs(position[1] - goal[1])
        )

    # ======================================================
    # PRACTICAL 04 LOGIC CHECK
    # ======================================================

    def is_tile_feasible(
        self,
        tile,
        percept
    ):

        """
        Check whether a tile is logically feasible
        using the Knowledge Base.

        Practical 04:

        1. Clear current facts.
        2. Add percept facts.
        3. Run forward chaining.
        4. If Retreat is deduced,
           the tile is infeasible.
        """

        # Clear old facts
        self.kb.clear_facts()

        # --------------------------------------------------
        # Read tile information
        # --------------------------------------------------

        # The visual environment may provide information
        # about target visibility and dust.

        target_visible = False
        has_dust = False
        bloodseeker_missing = False

        # --------------------------------------------------
        # Percept information
        # --------------------------------------------------

        if 'target_visible' in percept:

            target_visible = (
                tile in percept[
                    'target_visible'
                ]
            )

        if 'has_dust' in percept:

            has_dust = (
                tile in percept[
                    'has_dust'
                ]
            )

        if 'bloodseeker_missing' in percept:

            bloodseeker_missing = (
                percept[
                    'bloodseeker_missing'
                ]
            )

        # --------------------------------------------------
        # Add facts
        # --------------------------------------------------

        if target_visible:

            self.kb.tell_fact(
                'TargetVisible'
            )

        if has_dust:

            self.kb.tell_fact(
                'HasDust'
            )

        if bloodseeker_missing:

            self.kb.tell_fact(
                'BloodseekerMissing'
            )

        # --------------------------------------------------
        # Forward chaining
        # --------------------------------------------------

        self.kb.forward_chain()

        # --------------------------------------------------
        # Retreat means infeasible
        # --------------------------------------------------

        if 'Retreat' in self.kb.facts:

            return False

        return True

    # ======================================================
    # A*
    # ======================================================

    def astar_search(
        self,
        start,
        goal,
        walls,
        grid_size,
        percept=None
    ):

        """
        A* Search with Knowledge Base feasibility checking.

        f(n) = g(n) + h(n)

        g(n):
            Cost from start.

        h(n):
            Manhattan distance to goal.
        """

        walls = set(walls)

        if percept is None:

            percept = {}

        frontier = []

        counter = 0

        start_h = self.manhattan_distance(
            start,
            goal
        )

        heapq.heappush(
            frontier,
            (
                start_h,
                0,
                counter,
                start,
                []
            )
        )

        reached = {
            start: 0
        }

        while frontier:

            (
                f_cost,
                current_cost,
                _,
                current,
                path
            ) = heapq.heappop(
                frontier
            )

            # Goal test
            if current == goal:

                return path

            # --------------------------------------------------
            # Generate neighbours
            # --------------------------------------------------

            for action, next_position in (
                self.get_neighbors(
                    current,
                    grid_size,
                    walls
                )
            ):

                # --------------------------------------------------
                # Practical 04:
                # Check logical feasibility
                # before adding the node.
                # --------------------------------------------------

                if not self.is_tile_feasible(
                    next_position,
                    percept
                ):

                    continue

                # --------------------------------------------------
                # Calculate costs
                # --------------------------------------------------

                new_cost = (
                    current_cost + 1
                )

                if (
                    next_position not in reached
                    or new_cost < reached[
                        next_position
                    ]
                ):

                    reached[
                        next_position
                    ] = new_cost

                    heuristic = (
                        self.manhattan_distance(
                            next_position,
                            goal
                        )
                    )

                    total_cost = (
                        new_cost
                        +
                        heuristic
                    )

                    counter += 1

                    new_path = (
                        path + [action]
                    )

                    heapq.heappush(
                        frontier,
                        (
                            total_cost,
                            new_cost,
                            counter,
                            next_position,
                            new_path
                        )
                    )

        return None

    # ======================================================
    # FIND CLOSEST FOOD
    # ======================================================

    def find_closest_food(
        self,
        start,
        food_positions
    ):

        """
        Find closest food using Manhattan distance.
        """

        if not food_positions:

            return None

        return min(
            food_positions,
            key=lambda food:
                abs(food[0] - start[0])
                +
                abs(food[1] - start[1])
        )

    # ======================================================
    # CREATE PLAN
    # ======================================================

    def create_plan(
        self,
        percept
    ):

        """
        Create a path to the closest food.
        """

        start = tuple(
            percept['agent_pos']
        )

        food_positions = [

            tuple(food)

            for food in percept[
                'all_food'
            ]

        ]

        if not food_positions:

            return []

        # Find closest food
        goal = self.find_closest_food(
            start,
            food_positions
        )

        grid_size = (
            percept['grid_size']
        )

        walls = set(

            tuple(wall)

            for wall in percept[
                'walls'
            ]

        )

        self.planning_count += 1

        # --------------------------------------------------
        # Select algorithm
        # --------------------------------------------------

        if self.active_algo == 'BFS':

            plan = self.bfs_search(
                start,
                goal,
                walls,
                grid_size
            )

        elif self.active_algo == 'DFS':

            plan = self.dfs_search(
                start,
                goal,
                walls,
                grid_size
            )

        elif self.active_algo == 'UCS':

            plan = self.ucs_search(
                start,
                goal,
                walls,
                grid_size
            )

        elif self.active_algo == 'A*':

            plan = self.astar_search(
                start,
                goal,
                walls,
                grid_size,
                percept
            )

        else:

            raise ValueError(
                "Unknown algorithm: "
                + str(
                    self.active_algo
                )
            )

        if plan is None:

            return []

        return plan

    # ======================================================
    # SENSE AND ACT
    # ======================================================

    def sense_and_act(
        self,
        percept
    ):

        """
        Create a plan if needed,
        then execute one action.
        """

        # Create new plan
        if not self.plan:

            self.plan = (
                self.create_plan(
                    percept
                )
            )

        # Execute next action
        if self.plan:

            return self.plan.pop(0)

        # No path
        return 'Stay'