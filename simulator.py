from visual_grid_game import VisualGridHuntGame
from agent import SearchAgent


def run_simulation(agent, agent_name, width=10, height=10):
    """
    Run a search-agent simulation.

    The environment exposes its global state so that
    the SearchAgent can perform offline planning.
    """

    env = VisualGridHuntGame(
        width=width,
        height=height,
        num_food=5,
        num_opponents=0
    )

    print("\n========================================")
    print(f" Running {agent_name}")
    print("========================================")

    print(f"Grid Size: {width} x {height}")
    print(f"Starting Position: {env.agent_pos}")
    print(f"Initial Food: {env.food_positions}")
    print(f"Walls: {env.walls}")

    while not env.is_done():

        # --------------------------------------------------
        # Get global percept
        # --------------------------------------------------

        percept = env.get_percept()

        # --------------------------------------------------
        # Agent creates / follows plan
        # --------------------------------------------------

        action = agent.sense_and_act(percept)

        # --------------------------------------------------
        # Execute action
        # --------------------------------------------------

        env.execute_action(action)

        # --------------------------------------------------
        # Display result
        # --------------------------------------------------

        print(
            f"Step: {env.steps:2d} | "
            f"Algorithm: {agent.active_algo} | "
            f"Action: {action:5s} | "
            f"Position: {env.agent_pos} | "
            f"Score: {env.score:3d} | "
            f"Remaining Food: {len(env.food_positions)}"
        )

    print("\nGame Over!")
    print(f"Algorithm: {agent.active_algo}")
    print(f"Final Position: {env.agent_pos}")
    print(f"Final Score: {env.score}")
    print(f"Steps: {env.steps}")
    print(f"Food Remaining: {len(env.food_positions)}")
    print(f"Collision: {env.collision}")


def run_all_algorithms():

    # ==================================================
    # BFS
    # ==================================================

    bfs_agent = SearchAgent()

    bfs_agent.active_algo = 'BFS'

    run_simulation(
        bfs_agent,
        "Search Agent - BFS"
    )

    # ==================================================
    # DFS
    # ==================================================

    dfs_agent = SearchAgent()

    dfs_agent.active_algo = 'DFS'

    run_simulation(
        dfs_agent,
        "Search Agent - DFS"
    )

    # ==================================================
    # UCS
    # ==================================================

    ucs_agent = SearchAgent()

    ucs_agent.active_algo = 'UCS'

    run_simulation(
        ucs_agent,
        "Search Agent - UCS"
    )


if __name__ == "__main__":
    run_all_algorithms()