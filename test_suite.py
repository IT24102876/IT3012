import unittest

from agent import (
    SimpleReflexAgent,
    ModelBasedAgent,
    SearchAgent
)


class TestPractical1And2_ReflexAgents(
    unittest.TestCase
):

    def setUp(self):

        self.simple_agent = (
            SimpleReflexAgent()
        )

        self.model_agent = (
            ModelBasedAgent()
        )

    def test_simple_reflex_logic(self):

        # Food present
        percept_food = {
            'wall_ahead': False,
            'food_here': True
        }

        action = (
            self.simple_agent.sense_and_act(
                percept_food
            )
        )

        self.assertIsNotNone(
            action
        )

        # Wall ahead
        percept_wall = {
            'wall_ahead': True,
            'food_here': False
        }

        action_wall = (
            self.simple_agent.sense_and_act(
                percept_wall
            )
        )

        self.assertIn(
            action_wall,
            [
                'Left',
                'Right',
                'Down',
                'Up'
            ]
        )

    def test_model_based_memory(self):

        percept = {
            'wall_ahead': True,
            'food_here': False
        }

        action_1 = (
            self.model_agent.sense_and_act(
                percept
            )
        )

        action_2 = (
            self.model_agent.sense_and_act(
                percept
            )
        )

        self.assertNotEqual(
            action_1,
            action_2
        )


class TestPractical3_SearchAgent(
    unittest.TestCase
):

    def setUp(self):

        self.search_agent = SearchAgent()

    # ==================================================
    # BFS TEST
    # ==================================================

    def test_bfs_shortest_path(self):

        grid_size = (
            4,
            4
        )

        start_pos = (
            0,
            0
        )

        goal_pos = (
            3,
            3
        )

        walls = [
            (1, 0),
            (2, 0),
            (0, 2),
            (1, 2),
            (2, 2)
        ]

        path = (
            self.search_agent.bfs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )
        )

        self.assertIsNotNone(
            path
        )

        self.assertIsInstance(
            path,
            list
        )

        self.assertEqual(
            len(path),
            6
        )

    # ==================================================
    # BFS UNREACHABLE TEST
    # ==================================================

    def test_bfs_unreachable_goal(self):

        grid_size = (
            3,
            3
        )

        start_pos = (
            0,
            0
        )

        goal_pos = (
            2,
            2
        )

        walls = [
            (1, 2),
            (2, 1),
            (1, 1)
        ]

        path = (
            self.search_agent.bfs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )
        )

        is_empty_or_none = (
            path is None
            or len(path) == 0
        )

        self.assertTrue(
            is_empty_or_none
        )

    # ==================================================
    # DFS TEST
    # ==================================================

    def test_dfs_search(self):

        grid_size = (
            4,
            4
        )

        start_pos = (
            0,
            0
        )

        goal_pos = (
            3,
            3
        )

        walls = [
            (1, 0),
            (2, 0),
            (0, 2),
            (1, 2),
            (2, 2)
        ]

        path = (
            self.search_agent.dfs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )
        )

        self.assertIsNotNone(
            path
        )

        self.assertIsInstance(
            path,
            list
        )

    # ==================================================
    # UCS TEST
    # ==================================================

    def test_ucs_search(self):

        grid_size = (
            4,
            4
        )

        start_pos = (
            0,
            0
        )

        goal_pos = (
            3,
            3
        )

        walls = [
            (1, 0),
            (2, 0),
            (0, 2),
            (1, 2),
            (2, 2)
        ]

        path = (
            self.search_agent.ucs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )
        )

        self.assertIsNotNone(
            path
        )

        self.assertIsInstance(
            path,
            list
        )

        self.assertEqual(
            len(path),
            6
        )


if __name__ == '__main__':

    print(
        "=== IT3012: Intelligent Agents "
        "- Autograder Test Suite ===\n"
    )

    unittest.main(
        verbosity=2
    )