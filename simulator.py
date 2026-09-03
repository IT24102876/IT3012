from visual_grid_game import VisualGridHuntGame
from agent import SearchAgent


def run_simulation(
    algorithm,
    width=10,
    height=10,
    num_food=5
):
    """
    Run one search algorithm in the terminal.
    """

    agent = SearchAgent()

    agent.active_algo = algorithm

    env = VisualGridHuntGame(
        width=width,
        height=height,
        num_food=num_food,
        num_opponents=0
    )

    print()
    print("=" * 50)
    print(
        f"Running Search Agent - {algorithm}"
    )
    print("=" * 50)

    print(
        f"Grid Size: "
        f"{width} x {height}"
    )

    print(
        f"Starting Position: "
        f"{env.agent_pos}"
    )

    print(
        f"Initial Food: "
        f"{env.food_positions}"
    )

    print(
        f"Walls: "
        f"{env.walls}"
    )

    while not env.is_done():

        # Get global percept
        percept = env.get_percept()

        # Agent chooses action
        action = agent.sense_and_act(
            percept
        )

        # Execute action
        env.execute_action(
            action
        )

        print(
            f"Step: {env.steps:2d} | "
            f"Algorithm: {algorithm:3s} | "
            f"Action: {action:5s} | "
            f"Position: {env.agent_pos} | "
            f"Score: {env.score:3d} | "
            f"Food Remaining: "
            f"{len(env.food_positions)}"
        )

    print()
    print("Game Over!")
    print(
        f"Algorithm: {algorithm}"
    )
    print(
        f"Final Position: "
        f"{env.agent_pos}"
    )
    print(
        f"Final Score: "
        f"{env.score}"
    )
    print(
        f"Total Steps: "
        f"{env.steps}"
    )
    print(
        f"Food Remaining: "
        f"{len(env.food_positions)}"
    )


def run_all_algorithms():

    # BFS
    run_simulation(
        'BFS'
    )

    # DFS
    run_simulation(
        'DFS'
    )

    # UCS
    run_simulation(
        'UCS'
    )


if __name__ == "__main__":

    run_all_algorithms()