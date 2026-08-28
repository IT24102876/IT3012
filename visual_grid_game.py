import random
import tkinter as tk


class VisualGridHuntGame:
    """
    A flexible Pacman-style grid environment.

    Supports:
        - Configurable grid size
        - Food
        - Opponents
        - Custom walls

    For Practical 03, the global environment state
    is exposed through get_percept().
    """

    def __init__(
        self,
        width=10,
        height=10,
        num_food=10,
        num_opponents=2,
        custom_walls=None
    ):

        self.width = width
        self.height = height

        # Agent starts at (0, 0)
        self.agent_pos = [0, 0]

        # --------------------------------------------------
        # Walls
        # --------------------------------------------------

        if custom_walls is not None:

            self.walls = set(
                custom_walls
            )

        else:

            self.walls = {
                (2, 2),
                (2, 3),
                (5, 5),
                (6, 5),
                (3, 7)
            }

        # --------------------------------------------------
        # Food
        # --------------------------------------------------

        self.food_positions = set()

        while len(self.food_positions) < num_food:

            fx = random.randint(
                0,
                self.width - 1
            )

            fy = random.randint(
                0,
                self.height - 1
            )

            pos_tuple = (
                fx,
                fy
            )

            # Avoid agent start and walls
            if (
                pos_tuple != (0, 0)
                and pos_tuple not in self.walls
            ):

                self.food_positions.add(
                    pos_tuple
                )

        # --------------------------------------------------
        # Opponents
        # --------------------------------------------------

        self.opponents = []

        while len(self.opponents) < num_opponents:

            ox = random.randint(
                0,
                self.width - 1
            )

            oy = random.randint(
                0,
                self.height - 1
            )

            op_pos = [
                ox,
                oy
            ]

            op_tuple = tuple(
                op_pos
            )

            if (
                op_tuple != (0, 0)
                and op_tuple not in self.walls
                and op_tuple not in self.food_positions
            ):

                self.opponents.append(
                    op_pos
                )

        # --------------------------------------------------
        # Game state
        # --------------------------------------------------

        self.score = 0

        self.steps = 0

        self.collision = False

    # ==================================================
    # PERCEPT
    # ==================================================

    def get_percept(self) -> dict:
        """
        Return the environment percept.

        Practical 03 requires exposing the global
        world model to the search agent.

        New keys:
            grid_size
            walls
            all_food
        """

        return {

            # Agent's current position
            'agent_pos':
                list(self.agent_pos),

            # Opponent positions
            'opponent_positions':
                [
                    list(op)
                    for op in self.opponents
                ],

            # Food at current location
            'smells_food':
                tuple(self.agent_pos)
                in self.food_positions,

            # Whether agent is on a wall
            'hit_wall':
                tuple(self.agent_pos)
                in self.walls,

            # Collision status
            'collision':
                self.collision,

            # Current score
            'score':
                self.score,

            # Number of remaining food
            'remaining_food':
                len(self.food_positions),

            # ==================================================
            # GLOBAL STATE FOR SEARCH AGENT
            # ==================================================

            # Grid dimensions
            'grid_size':
                (self.width, self.height),

            # Complete wall information
            'walls':
                list(self.walls),

            # Complete food information
            'all_food':
                list(self.food_positions)
        }

    # ==================================================
    # EXECUTE ACTION
    # ==================================================

    def execute_action(self, action: str):

        self.steps += 1

        new_pos = list(
            self.agent_pos
        )

        # --------------------------------------------------
        # Move Up
        # --------------------------------------------------

        if action == 'Up':

            new_pos[1] = min(
                self.height - 1,
                new_pos[1] + 1
            )

        # --------------------------------------------------
        # Move Down
        # --------------------------------------------------

        elif action == 'Down':

            new_pos[1] = max(
                0,
                new_pos[1] - 1
            )

        # --------------------------------------------------
        # Move Left
        # --------------------------------------------------

        elif action == 'Left':

            new_pos[0] = max(
                0,
                new_pos[0] - 1
            )

        # --------------------------------------------------
        # Move Right
        # --------------------------------------------------

        elif action == 'Right':

            new_pos[0] = min(
                self.width - 1,
                new_pos[0] + 1
            )

        # --------------------------------------------------
        # Check wall collision
        # --------------------------------------------------

        if tuple(new_pos) in self.walls:

            # Agent cannot move through wall
            self.score -= 5

        else:

            # Move agent
            self.agent_pos = new_pos

        # --------------------------------------------------
        # Check food
        # --------------------------------------------------

        tuple_pos = tuple(
            self.agent_pos
        )

        if tuple_pos in self.food_positions:

            self.food_positions.remove(
                tuple_pos
            )

            # Reward for collecting food
            self.score += 20

        # --------------------------------------------------
        # Move opponents
        # --------------------------------------------------

        for op in self.opponents:

            move = random.choice(
                [
                    'Up',
                    'Down',
                    'Left',
                    'Right',
                    'Stay'
                ]
            )

            if (
                move == 'Up'
                and op[1] < self.height - 1
            ):

                op[1] += 1

            elif (
                move == 'Down'
                and op[1] > 0
            ):

                op[1] -= 1

            elif (
                move == 'Left'
                and op[0] > 0
            ):

                op[0] -= 1

            elif (
                move == 'Right'
                and op[0] < self.width - 1
            ):

                op[0] += 1

            # --------------------------------------------------
            # Collision
            # --------------------------------------------------

            if op == self.agent_pos:

                self.score -= 50

                self.collision = True

    # ==================================================
    # GAME END
    # ==================================================

    def is_done(self) -> bool:

        return (
            len(self.food_positions) == 0
            or self.steps >= 60
            or self.collision
        )


class GridGameGUI:
    """
    Tkinter GUI wrapper.

    Used to visually demonstrate the grid environment.
    """

    def __init__(
        self,
        root,
        width=10,
        height=10,
        num_food=12,
        num_opponents=2,
        walls=None
    ):

        self.root = root

        self.root.title(
            "IT3012 - Scalable Multi-Agent Grid Hunt"
        )

        # --------------------------------------------------
        # Environment
        # --------------------------------------------------

        self.env = VisualGridHuntGame(
            width=width,
            height=height,
            num_food=num_food,
            num_opponents=num_opponents,
            custom_walls=walls
        )

        # --------------------------------------------------
        # Canvas size
        # --------------------------------------------------

        max_canvas_dim = 600

        self.cell_size = max(
            20,
            min(
                max_canvas_dim // self.env.width,
                max_canvas_dim // self.env.height
            )
        )

        canvas_w = (
            self.env.width
            * self.cell_size
        )

        canvas_h = (
            self.env.height
            * self.cell_size
        )

        # --------------------------------------------------
        # Canvas
        # --------------------------------------------------

        self.canvas = tk.Canvas(
            root,
            width=canvas_w,
            height=canvas_h,
            bg="white"
        )

        self.canvas.pack()

        # --------------------------------------------------
        # Label
        # --------------------------------------------------

        self.label = tk.Label(
            root,
            text="Score: 0 | Steps: 0",
            font=("Arial", 14)
        )

        self.label.pack(
            pady=10
        )

        # --------------------------------------------------
        # Button
        # --------------------------------------------------

        self.btn = tk.Button(
            root,
            text="Start Simulation",
            command=self.run_loop,
            font=("Arial", 12),
            bg="#000066",
            fg="white"
        )

        self.btn.pack(
            pady=5
        )

        self.draw_grid()

    # ==================================================
    # DRAW GRID
    # ==================================================

    def draw_grid(self):

        self.canvas.delete("all")

        # --------------------------------------------------
        # Draw cells
        # --------------------------------------------------

        for x in range(
            self.env.width
        ):

            for y in range(
                self.env.height
            ):

                x1 = (
                    x
                    * self.cell_size
                )

                y1 = (
                    self.env.height
                    - 1
                    - y
                ) * self.cell_size

                x2 = (
                    x1
                    + self.cell_size
                )

                y2 = (
                    y1
                    + self.cell_size
                )

                # Wall or normal cell
                if (
                    x,
                    y
                ) in self.env.walls:

                    cell_color = "#64748b"

                else:

                    cell_color = "#f1f5f9"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=cell_color,
                    outline="#cbd5e1"
                )

                # Display W for walls
                if (
                    self.cell_size >= 40
                    and (x, y)
                    in self.env.walls
                ):

                    self.canvas.create_text(
                        x1
                        + self.cell_size / 2,
                        y1
                        + self.cell_size / 2,
                        text="W",
                        fill="white",
                        font=(
                            "Arial",
                            8,
                            "bold"
                        )
                    )

        # --------------------------------------------------
        # Draw food
        # --------------------------------------------------

        for fx, fy in self.env.food_positions:

            offset = (
                self.cell_size
                * 0.25
            )

            x1 = (
                fx
                * self.cell_size
                + offset
            )

            y1 = (
                self.env.height
                - 1
                - fy
            ) * self.cell_size + offset

            self.canvas.create_oval(
                x1,
                y1,
                x1
                + self.cell_size * 0.5,
                y1
                + self.cell_size * 0.5,
                fill="#f59e0b",
                outline="#d97706"
            )

        # --------------------------------------------------
        # Draw opponents
        # --------------------------------------------------

        for ox, oy in self.env.opponents:

            offset = (
                self.cell_size
                * 0.2
            )

            x1 = (
                ox
                * self.cell_size
                + offset
            )

            y1 = (
                self.env.height
                - 1
                - oy
            ) * self.cell_size + offset

            self.canvas.create_rectangle(
                x1,
                y1,
                x1
                + self.cell_size * 0.6,
                y1
                + self.cell_size * 0.6,
                fill="#990000",
                outline="#7a0000"
            )

        # --------------------------------------------------
        # Draw agent
        # --------------------------------------------------

        ax, ay = self.env.agent_pos

        offset = (
            self.cell_size
            * 0.15
        )

        x1 = (
            ax
            * self.cell_size
            + offset
        )

        y1 = (
            self.env.height
            - 1
            - ay
        ) * self.cell_size + offset

        self.canvas.create_oval(
            x1,
            y1,
            x1
            + self.cell_size * 0.7,
            y1
            + self.cell_size * 0.7,
            fill="#000066",
            outline="#1e3a8a"
        )

    # ==================================================
    # RUN LOOP
    # ==================================================

    def run_loop(self):

        self.btn.config(
            state="disabled"
        )

        def step():

            if not self.env.is_done():

                # Random action for GUI demonstration
                action = random.choice(
                    [
                        'Up',
                        'Down',
                        'Left',
                        'Right'
                    ]
                )

                self.env.execute_action(
                    action
                )

                self.draw_grid()

                self.label.config(
                    text=(
                        f"Score: {self.env.score} | "
                        f"Steps: {self.env.steps} | "
                        f"Action: {action}"
                    )
                )

                self.root.after(
                    250,
                    step
                )

            else:

                if self.env.collision:

                    end_text = (
                        "Collision! Game Over! "
                        f"Final Score: {self.env.score}"
                    )

                else:

                    end_text = (
                        "Finished! "
                        f"Final Score: {self.env.score}"
                    )

                self.label.config(
                    text=end_text
                )

                self.btn.config(
                    state="normal"
                )

        step()


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = GridGameGUI(
        root,
        width=12,
        height=12,
        num_food=15,
        num_opponents=0
    )

    root.mainloop()