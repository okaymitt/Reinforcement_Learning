import unittest
import grid_world
import sarsa

gridworld = grid_world.Gridworld(move='cross', modus='RL')



class Test_Sarsa(unittest.TestCase):
    def test_state_size(self):
        RL = sarsa.Sarsa(gridworld)
        self.assertEqual(RL.state_size, RL.observation_size[0]*RL.observation_size[1])
    
    def test_qvalue_size(self):
        RL = sarsa.Sarsa(gridworld)
        self.assertEqual(RL.q_value.shape, (RL.state_size, RL.action_size))


if __name__ == '__main__':
    unittest.main()