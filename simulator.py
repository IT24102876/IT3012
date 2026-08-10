from grid_game import GridHuntGame
from agent import SimpleReflexAgent, ModelBasedAgent


def run_simulation(agent, agent_name):

    env = GridHuntGame()

    print("\n====================================")
    print(f" Running {agent_name}")
    print("====================================")

    while not env.is_done():

        # Get partial percept
        percept = env.get_percept(agent)

        # Agent makes decision
        action = agent.sense_and_act(percept)

        # Environment executes action
        env.execute_action(action)

        print(
            f"Step: {env.steps:2d} | "
            f"Percept: {percept} | "
            f"Action: {action} | "
            f"Position: {env.agent_pos} | "
            f"Score: {env.score}"
        )

    print("\nGame Over!")
    print(f"Final Position: {env.agent_pos}")
    print(f"Final Score: {env.score}")
    print(f"Steps: {env.steps}")
    print(f"Food Remaining: {len(env.food_positions)}")


def main():

    # ------------------------------------
    # Test Simple Reflex Agent
    # ------------------------------------

    simple_agent = SimpleReflexAgent()

    run_simulation(
        simple_agent,
        "Simple Reflex Agent"
    )

    # ------------------------------------
    # Test Model-Based Agent
    # ------------------------------------

    model_agent = ModelBasedAgent()

    run_simulation(
        model_agent,
        "Model-Based Agent"
    )


if __name__ == "__main__":
    main()