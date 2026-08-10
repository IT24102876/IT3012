class GridHuntGame:
    """
    Partially Observable Grid Environment.

    The agent does not receive the complete environment.
    It only receives local information such as:
        - Is there food here?
        - Is there a wall ahead?
    """

    def __init__(self, width=4, height=4):

        self.width = width
        self.height = height

        # Agent starts at (0, 0)
        self.agent_pos = [0, 0]

        # Food positions
        self.food_positions = {
            (1, 2),
            (2, 3),
            (3, 0),
            (2, 1)
        }

        # Wall positions
        self.walls = {
            (1, 1),
            (2, 2)
        }

        self.score = 0
        self.steps = 0

    def get_percept(self, agent=None):
        """
        Return only local percept information.

        The agent does NOT receive the complete map.
        """

        return {
            # Food at the current location
            'food_here': tuple(self.agent_pos) in self.food_positions,

            # Is there a wall in front of the agent?
            #
            # In this simplified environment,
            # Up is treated as "forward".
            'wall_ahead': self._wall_ahead()
        }

    def _wall_ahead(self):
        """
        Check whether the cell directly in front of
        the agent contains a wall or is outside the grid.
        """

        x, y = self.agent_pos

        # Up is considered forward
        next_pos = (
            x,
            min(self.height - 1, y + 1)
        )

        # At the top boundary, consider it a wall
        if y == self.height - 1:
            return True

        return next_pos in self.walls

    def execute_action(self, action: str):

        self.steps += 1

        new_pos = list(self.agent_pos)

        # -----------------------------
        # Move Up
        # -----------------------------
        if action == 'Up':
            new_pos[1] = min(
                self.height - 1,
                new_pos[1] + 1
            )

        # -----------------------------
        # Move Down
        # -----------------------------
        elif action == 'Down':
            new_pos[1] = max(
                0,
                new_pos[1] - 1
            )

        # -----------------------------
        # Move Left
        # -----------------------------
        elif action == 'Left':
            new_pos[0] = max(
                0,
                new_pos[0] - 1
            )

        # -----------------------------
        # Move Right
        # -----------------------------
        elif action == 'Right':
            new_pos[0] = min(
                self.width - 1,
                new_pos[0] + 1
            )

        # -----------------------------
        # Check wall collision
        # -----------------------------
        if tuple(new_pos) in self.walls:

            # Agent cannot move through wall
            self.score -= 5

        else:

            # Move agent
            self.agent_pos = new_pos

        # -----------------------------
        # Check food
        # -----------------------------

        current_position = tuple(self.agent_pos)

        if current_position in self.food_positions:

            self.food_positions.remove(current_position)

            # Reward
            self.score += 20

    def is_done(self):

        # Game ends when all food is collected
        # OR maximum number of steps is reached.
        return (
            len(self.food_positions) == 0
            or self.steps >= 20
        )