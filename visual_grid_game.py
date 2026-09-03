import random
import tkinter as tk

from agent import SearchAgent


class VisualGridHuntGame:
    """
    Visual Grid Hunt Environment.

    Practical 03 version.

    The environment exposes:
        - agent_pos
        - grid_size
        - walls
        - all_food

    This allows the SearchAgent to perform
    BFS, DFS and UCS planning.
    """

    def __init__(
        self,
        width=10,
        height=10,
        num_food=8,
        num_opponents=0,
        custom_walls=None
    ):

        self.width = width
        self.height = height

        # --------------------------------------------------
        # Agent
        # --------------------------------------------------

        self.agent_pos = [
            0,
            0
        ]

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

        while len(
            self.food_positions
        ) < num_food:

            fx = random.randint(
                0,
                self.width - 1
            )

            fy = random.randint(
                0,
                self.height - 1
            )

            food = (
                fx,
                fy
            )

            if (
                food != (0, 0)
                and food not in self.walls
            ):

                self.food_positions.add(
                    food
                )

        # --------------------------------------------------
        # Opponents
        # --------------------------------------------------

        self.opponents = []

        while len(
            self.opponents
        ) < num_opponents:

            ox = random.randint(
                0,
                self.width - 1
            )

            oy = random.randint(
                0,
                self.height - 1
            )

            opponent = [
                ox,
                oy
            ]

            opponent_tuple = tuple(
                opponent
            )

            if (
                opponent_tuple != (0, 0)
                and opponent_tuple not in self.walls
                and opponent_tuple not in self.food_positions
            ):

                self.opponents.append(
                    opponent
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
        Return the global percept.

        Practical 03 requires:
            grid_size
            walls
            all_food
        """

        return {

            # Current agent position
            'agent_pos':
                list(
                    self.agent_pos
                ),

            # Opponents
            'opponent_positions':
                [
                    list(op)
                    for op in self.opponents
                ],

            # Food at current location
            'smells_food':
                tuple(
                    self.agent_pos
                ) in self.food_positions,

            # Wall information
            'hit_wall':
                tuple(
                    self.agent_pos
                ) in self.walls,

            # Collision
            'collision':
                self.collision,

            # Score
            'score':
                self.score,

            # Remaining food
            'remaining_food':
                len(
                    self.food_positions
                ),

            # ==================================================
            # PRACTICAL 03 GLOBAL STATE
            # ==================================================

            'grid_size':
                (
                    self.width,
                    self.height
                ),

            'walls':
                list(
                    self.walls
                ),

            'all_food':
                list(
                    self.food_positions
                )
        }

    # ==================================================
    # EXECUTE ACTION
    # ==================================================

    def execute_action(
        self,
        action: str
    ):

        self.steps += 1

        new_pos = list(
            self.agent_pos
        )

        # --------------------------------------------------
        # Up
        # --------------------------------------------------

        if action == 'Up':

            new_pos[1] = min(
                self.height - 1,
                new_pos[1] + 1
            )

        # --------------------------------------------------
        # Down
        # --------------------------------------------------

        elif action == 'Down':

            new_pos[1] = max(
                0,
                new_pos[1] - 1
            )

        # --------------------------------------------------
        # Left
        # --------------------------------------------------

        elif action == 'Left':

            new_pos[0] = max(
                0,
                new_pos[0] - 1
            )

        # --------------------------------------------------
        # Right
        # --------------------------------------------------

        elif action == 'Right':

            new_pos[0] = min(
                self.width - 1,
                new_pos[0] + 1
            )

        # --------------------------------------------------
        # Stay
        # --------------------------------------------------

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
        # Eat food
        # --------------------------------------------------

        current_position = tuple(
            self.agent_pos
        )

        if (
            current_position
            in self.food_positions
        ):

            self.food_positions.remove(
                current_position
            )

            # Food reward
            self.score += 20

        # --------------------------------------------------
        # Opponents
        # --------------------------------------------------

        for opponent in self.opponents:

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
                and opponent[1]
                < self.height - 1
            ):

                opponent[1] += 1

            elif (
                move == 'Down'
                and opponent[1] > 0
            ):

                opponent[1] -= 1

            elif (
                move == 'Left'
                and opponent[0] > 0
            ):

                opponent[0] -= 1

            elif (
                move == 'Right'
                and opponent[0]
                < self.width - 1
            ):

                opponent[0] += 1

            # Collision
            if opponent == self.agent_pos:

                self.score -= 50

                self.collision = True

    # ==================================================
    # GAME END
    # ==================================================

    def is_done(self) -> bool:

        return (
            len(
                self.food_positions
            ) == 0

            or self.steps >= 100

            or self.collision
        )


class GridGameGUI:
    """
    Tkinter GUI for Practical 03.

    Allows the user to choose:

        BFS
        DFS
        UCS

    and watch the SearchAgent
    navigate the environment.
    """

    def __init__(
        self,
        root,
        width=10,
        height=10,
        num_food=8,
        num_opponents=0,
        walls=None
    ):

        self.root = root

        self.root.title(
            "IT3012 - Practical 05 - Search Agent"
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
        # Search Agent
        # --------------------------------------------------

        self.agent = SearchAgent()

        self.agent.active_algo = 'BFS'

        # --------------------------------------------------
        # Canvas
        # --------------------------------------------------

        max_canvas_dim = 600

        self.cell_size = max(
            30,
            min(
                max_canvas_dim // self.env.width,
                max_canvas_dim // self.env.height
            )
        )

        canvas_width = (
            self.env.width
            * self.cell_size
        )

        canvas_height = (
            self.env.height
            * self.cell_size
        )

        self.canvas = tk.Canvas(
            root,
            width=canvas_width,
            height=canvas_height,
            bg="white"
        )

        self.canvas.pack(
            padx=10,
            pady=10
        )

        # --------------------------------------------------
        # Algorithm label
        # --------------------------------------------------

        self.algorithm_label = tk.Label(
            root,
            text="Algorithm: BFS",
            font=(
                "Arial",
                15,
                "bold"
            )
        )

        self.algorithm_label.pack(
            pady=5
        )

        # --------------------------------------------------
        # Status label
        # --------------------------------------------------

        self.status_label = tk.Label(
            root,
            text=(
                "Choose an algorithm "
                "and press Start Simulation"
            ),
            font=(
                "Arial",
                11
            )
        )

        self.status_label.pack(
            pady=5
        )

        # --------------------------------------------------
        # Button frame
        # --------------------------------------------------

        button_frame = tk.Frame(
            root
        )

        button_frame.pack(
            pady=5
        )

        # --------------------------------------------------
        # BFS button
        # --------------------------------------------------

        self.bfs_button = tk.Button(
            button_frame,
            text="BFS",
            width=10,
            command=lambda:
                self.select_algorithm('BFS')
        )

        self.bfs_button.grid(
            row=0,
            column=0,
            padx=5
        )

        # --------------------------------------------------
        # DFS button
        # --------------------------------------------------

        self.dfs_button = tk.Button(
            button_frame,
            text="DFS",
            width=10,
            command=lambda:
                self.select_algorithm('DFS')
        )

        self.dfs_button.grid(
            row=0,
            column=1,
            padx=5
        )

        # --------------------------------------------------
        # UCS button
        # --------------------------------------------------

        self.ucs_button = tk.Button(
            button_frame,
            text="UCS",
            width=10,
            command=lambda:
                self.select_algorithm('UCS')
        )

        self.ucs_button.grid(
            row=0,
            column=2,
            padx=5
        )

        # --------------------------------------------------
        # Start button
        # --------------------------------------------------

        self.start_button = tk.Button(
            root,
            text="Start Simulation",
            width=20,
            command=self.start_simulation
        )

        self.start_button.pack(
            pady=8
        )

        # --------------------------------------------------
        # Initial drawing
        # --------------------------------------------------

        self.draw_grid()

    # ==================================================
    # SELECT ALGORITHM
    # ==================================================

    def select_algorithm(
        self,
        algorithm
    ):

        # Don't allow changing while running
        if str(
            self.start_button['state']
        ) == 'disabled':

            return

        self.agent.active_algo = algorithm

        self.algorithm_label.config(
            text=f"Algorithm: {algorithm}"
        )

        self.status_label.config(
            text=(
                f"{algorithm} selected. "
                "Press Start Simulation."
            )
        )

    # ==================================================
    # RESET ENVIRONMENT
    # ==================================================

    def reset_environment(self):

        # Create a fresh environment
        self.env = VisualGridHuntGame(
            width=10,
            height=10,
            num_food=8,
            num_opponents=0
        )

        # Create fresh agent
        self.agent = SearchAgent()

        # Keep selected algorithm
        self.agent.active_algo = (
            self.algorithm_label['text']
            .replace(
                "Algorithm: ",
                ""
            )
        )

        self.draw_grid()

    # ==================================================
    # START SIMULATION
    # ==================================================

    def start_simulation(self):

        # Disable controls
        self.start_button.config(
            state="disabled"
        )

        self.bfs_button.config(
            state="disabled"
        )

        self.dfs_button.config(
            state="disabled"
        )

        self.ucs_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="Simulation running..."
        )

        self.run_step()

    # ==================================================
    # RUN ONE STEP
    # ==================================================

    def run_step(self):

        # Check if game finished
        if self.env.is_done():

            self.show_game_over()

            return

        # --------------------------------------------------
        # Get global percept
        # --------------------------------------------------

        percept = (
            self.env.get_percept()
        )

        # --------------------------------------------------
        # Search agent chooses action
        # --------------------------------------------------

        action = (
            self.agent.sense_and_act(
                percept
            )
        )

        # --------------------------------------------------
        # Environment executes action
        # --------------------------------------------------

        self.env.execute_action(
            action
        )

        # --------------------------------------------------
        # Redraw GUI
        # --------------------------------------------------

        self.draw_grid()

        # --------------------------------------------------
        # Update information
        # --------------------------------------------------

        self.status_label.config(
            text=(
                f"Algorithm: "
                f"{self.agent.active_algo} | "
                f"Action: {action} | "
                f"Score: {self.env.score} | "
                f"Steps: {self.env.steps} | "
                f"Food Remaining: "
                f"{len(self.env.food_positions)}"
            )
        )

        # --------------------------------------------------
        # Schedule next step
        # --------------------------------------------------

        self.root.after(
            400,
            self.run_step
        )

    # ==================================================
    # GAME OVER
    # ==================================================

    def show_game_over(self):

        if self.env.collision:

            message = (
                "Collision! Game Over!"
            )

        elif len(
            self.env.food_positions
        ) == 0:

            message = (
                "All food collected!"
            )

        else:

            message = (
                "Maximum steps reached!"
            )

        self.status_label.config(
            text=(
                f"{message}   |   "
                f"Final Score: "
                f"{self.env.score}   |   "
                f"Steps: {self.env.steps}"
            )
        )

        # Enable controls
        self.start_button.config(
            state="normal"
        )

        self.bfs_button.config(
            state="normal"
        )

        self.dfs_button.config(
            state="normal"
        )

        self.ucs_button.config(
            state="normal"
        )

    # ==================================================
    # DRAW GRID
    # ==================================================

    def draw_grid(self):

        self.canvas.delete(
            "all"
        )

        # --------------------------------------------------
        # Draw grid cells
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

                # Wall
                if (
                    x,
                    y
                ) in self.env.walls:

                    cell_color = "#64748b"

                # Normal cell
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

                # Wall label
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
                            9,
                            "bold"
                        )
                    )

        # --------------------------------------------------
        # Draw food
        # --------------------------------------------------

        for fx, fy in (
            self.env.food_positions
        ):

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

        for ox, oy in (
            self.env.opponents
        ):

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

        ax, ay = (
            self.env.agent_pos
        )

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
# MAIN
# ==================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = GridGameGUI(
        root,
        width=10,
        height=10,
        num_food=8,
        num_opponents=0
    )

    root.mainloop()