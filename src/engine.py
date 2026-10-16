"""Regras e física do Brick Blocks, independentes da interface gráfica."""

import math
import random
from dataclasses import dataclass

WIDTH, HEIGHT = 720, 900
TOP, FLOOR, CELL, RADIUS = 60, 860, 80, 9
SPEED, INTERVAL = 620, 0.085


@dataclass
class Block:
    x: float
    y: float
    hp: int


@dataclass
class Pickup:
    x: float
    y: float


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float


class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.round = 1
        self.count = 1
        self.origin = WIDTH / 2
        self.blocks = []
        self.pickups = []
        self.balls = []
        self.pending = 0
        self.collected = 0
        self.landing = None
        self.timer = 0
        self.hits = 0
        self.state = "aim"
        self.add_row()

    def add_row(self):
        cells = list(range(9))
        self.rng.shuffle(cells)
        for col in cells[: self.rng.randint(3, 6)]:
            self.blocks.append(Block(col * CELL, TOP + CELL, self.round))
        col = cells[-1]
        self.pickups.append(Pickup(col * CELL + CELL / 2, TOP + CELL * 1.5))

    def direction(self, x, y):
        dx, dy = x - self.origin, y - (FLOOR - RADIUS)
        if dy >= -12:
            return None
        angle = max(
            math.radians(8), min(math.pi - math.radians(8), math.atan2(-dy, dx))
        )
        return math.cos(angle), -math.sin(angle)

    def shoot(self, x, y):
        direction = self.direction(x, y)
        if self.state != "aim" or direction is None:
            return False
        self.velocity = (direction[0] * SPEED, direction[1] * SPEED)
        self.pending = self.count
        self.timer = 0
        self.landing = None
        self.state = "flight"
        return True

    def finish_round(self):
        self.origin = self.landing if self.landing is not None else self.origin
        self.balls.clear()
        self.pending = 0
        self.count += self.collected
        self.collected = 0
        for block in self.blocks:
            block.y += CELL
        for item in self.pickups:
            item.y += CELL
        self.pickups = [p for p in self.pickups if p.y + CELL / 2 < FLOOR]
        if any(b.y + CELL >= FLOOR for b in self.blocks):
            self.state = "over"
            return
        self.round += 1
        self.add_row()
        self.state = "aim"

    def recall(self):
        if self.state == "flight":
            self.finish_round()

    def update(self, dt):
        if self.state != "flight":
            return
        # Small fixed upper bound prevents tunnelling even during fast-forward.
        remaining = max(0, dt)
        while remaining > 1e-9 and self.state == "flight":
            step = min(remaining, 1 / 240)
            remaining -= step
            self.timer -= step
            if self.pending and self.timer <= 0:
                self.balls.append(Ball(self.origin, FLOOR - RADIUS, *self.velocity))
                self.pending -= 1
                self.timer += INTERVAL
            for ball in self.balls[:]:
                ball.x += ball.vx * step
                ball.y += ball.vy * step
                if ball.x < RADIUS:
                    ball.x, ball.vx = RADIUS, abs(ball.vx)
                elif ball.x > WIDTH - RADIUS:
                    ball.x, ball.vx = WIDTH - RADIUS, -abs(ball.vx)
                if ball.y < TOP + RADIUS:
                    ball.y, ball.vy = TOP + RADIUS, abs(ball.vy)
                for p in self.pickups[:]:
                    if math.hypot(ball.x - p.x, ball.y - p.y) < RADIUS + 25:
                        self.pickups.remove(p)
                        self.collected += 1
                for b in self.blocks[:]:
                    if self.collide(ball, b):
                        b.hp -= 1
                        self.hits += 1
                        if b.hp <= 0:
                            self.blocks.remove(b)
                        break
                if ball.y >= FLOOR - RADIUS and ball.vy > 0:
                    if self.landing is None:
                        self.landing = max(RADIUS, min(WIDTH - RADIUS, ball.x))
                    self.balls.remove(ball)
            if not self.pending and not self.balls:
                self.finish_round()

    @staticmethod
    def collide(ball, block):
        # Circle against rectangle, including the true corner normal.
        left, top = block.x + 2, block.y + 2
        right, bottom = block.x + CELL - 2, block.y + CELL - 2
        nx = ball.x - max(left, min(right, ball.x))
        ny = ball.y - max(top, min(bottom, ball.y))
        distance = math.hypot(nx, ny)
        if distance >= RADIUS:
            return False
        if distance == 0:
            sides = [
                (ball.x - left, -1, 0),
                (right - ball.x, 1, 0),
                (ball.y - top, 0, -1),
                (bottom - ball.y, 0, 1),
            ]
            depth, nx, ny = min(sides)
            penetration = RADIUS + depth
        else:
            nx, ny = nx / distance, ny / distance
            penetration = RADIUS - distance
        ball.x += nx * (penetration + 0.01)
        ball.y += ny * (penetration + 0.01)
        dot = ball.vx * nx + ball.vy * ny
        if dot >= 0:
            return False
        ball.vx -= 2 * dot * nx
        ball.vy -= 2 * dot * ny
        return True
