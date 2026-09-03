class GridHuntGame:
    """
    Partially Observable Grid Environment.

    Used for the Simple Reflex Agent
    and Model-Based Agent.
    """

    def __init__(
        self,
        width=4,
        height=4
    ):

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

    def get_percept(
        self,
        agent=None
    ):

        return {

            'food_here':
                tuple(self.agent_pos)
                in self.food_positions,

            'wall_ahead':
                self._wall_ahead(),

            'agent_pos':
                list(self.agent_pos)
        }

    def _wall_ahead(self):

        x, y = self.agent_pos

        # Top boundary
        if y == self.height - 1:
            return True

        next_pos = (
            x,
            y + 1
        )

        return next_pos in self.walls

    def execute_action(
        self,
        action: str
    ):

        self.steps += 1

        new_pos = list(
            self.agent_pos
        )

        # Up
        if action == 'Up':

            new_pos[1] = min(
                self.height - 1,
                new_pos[1] + 1
            )

        # Down
        elif action == 'Down':

            new_pos[1] = max(
                0,
                new_pos[1] - 1
            )

        # Left
        elif action == 'Left':

            new_pos[0] = max(
                0,
                new_pos[0] - 1
            )

        # Right
        elif action == 'Right':

            new_pos[0] = min(
                self.width - 1,
                new_pos[0] + 1
            )

        # Stay
        elif action == 'Stay':

            pass

        # --------------------------------------------------
        # Wall collision
        # --------------------------------------------------

        if tuple(new_pos) in self.walls:

            self.score -= 5

        else:

            self.agent_pos = new_pos

        # --------------------------------------------------
        # Food
        # --------------------------------------------------

        current_position = tuple(
            self.agent_pos
        )

        if current_position in self.food_positions:

            self.food_positions.remove(
                current_position
            )

            self.score += 20

    def is_done(self):

        return (
            len(self.food_positions) == 0
            or self.steps >= 20
        )