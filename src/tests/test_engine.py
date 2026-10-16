import math
import unittest

from engine import FLOOR, Ball, Block, Game, Pickup


class PhysicsTests(unittest.TestCase):
    def test_cannot_launch_down_or_during_flight(self):
        g = Game(1)
        self.assertFalse(g.shoot(g.origin, FLOOR))
        self.assertTrue(g.shoot(g.origin, 100))
        self.assertFalse(g.shoot(100, 100))

    def test_side_and_corner_reflection_preserve_speed(self):
        for ball in [Ball(94, 140, 100, 0), Ball(96, 96, 100, 100)]:
            speed = math.hypot(ball.vx, ball.vy)
            self.assertTrue(Game.collide(ball, Block(100, 100, 2)))
            self.assertLess(ball.vx, 0)
            self.assertAlmostEqual(speed, math.hypot(ball.vx, ball.vy))

    def test_block_takes_one_hit_and_ball_returns(self):
        g = Game(2)
        g.blocks = [Block(320, 140, 1)]
        g.pickups = []
        g.shoot(360, 60)
        for _ in range(2000):
            g.update(1 / 120)
            if g.state != "flight":
                break
        self.assertEqual(g.hits, 1)
        self.assertEqual(g.round, 2)
        self.assertEqual(g.state, "aim")
        self.assertAlmostEqual(g.origin, 360)

    def test_pickup_counts_once_for_entire_volley(self):
        g = Game(3)
        g.count = 3
        g.blocks = []
        g.pickups = [Pickup(360, 400)]
        g.shoot(360, 60)
        for _ in range(2000):
            g.update(1 / 120)
            if g.state != "flight":
                break
        self.assertEqual(g.count, 4)
        self.assertEqual(g.round, 2)
        self.assertEqual(g.pending, 0)
        self.assertFalse(g.balls)

    def test_loss_when_blocks_reach_floor(self):
        g = Game(4)
        g.blocks = [Block(0, FLOOR - 160, 10)]
        g.finish_round()
        self.assertEqual(g.state, "over")

    def test_fast_forward_still_hits_block(self):
        g = Game(5)
        g.blocks = [Block(320, 140, 10)]
        g.pickups = []
        g.shoot(360, 60)
        g.update(2)
        self.assertEqual(g.hits, 1)
        self.assertEqual(g.blocks[0].hp, 9)

    def test_round_spawns_separate_pickup_and_valid_blocks(self):
        g = Game(6)
        for _ in range(30):
            g.blocks.clear()
            g.pickups.clear()
            g.finish_round()
            self.assertTrue(all(b.hp == g.round for b in g.blocks))
            self.assertFalse(any(b.x < g.pickups[0].x < b.x + 80 for b in g.blocks))


if __name__ == "__main__":
    unittest.main()
