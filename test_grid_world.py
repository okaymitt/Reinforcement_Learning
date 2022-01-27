import unittest
import grid_world

class Test_Gridworld(unittest.TestCase):
    def test_grid_world(self):
        environment = grid_world.Gridworld()
        result = (environment.pos_x, environment.pos_y)
        expected_result = (0, 3)
        self.assertEqual(result, expected_result)

    def test_move(self):
        environment = grid_world.Gridworld()

        direction = (0, 1)
        environment.move(direction)

        result = (environment.pos_x, environment.pos_y)
        expected_result = (3, 1)
        self.assertEqual(result, expected_result)

        direction = (0, -1)
        environment.move(direction)

        result = (environment.pos_x, environment.pos_y)
        expected_result = (3, 0)
        self.assertEqual(result, expected_result)

        direction = (1, 0)
        environment.move(direction)

        result = (environment.pos_x, environment.pos_y)
        expected_result = (4, 0)
        self.assertEqual(result, expected_result)


        direction = (-1, 0)
        environment.move(direction)

        result = (environment.pos_x, environment.pos_y)
        expected_result = (3, 0)
        self.assertEqual(result, expected_result)        





if __name__ == '__main__':
    unittest.main()