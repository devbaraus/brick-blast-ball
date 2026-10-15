"""Execute com python main.py. Os assets são relativos a este arquivo."""
import argparse
import json
import math
import os
from pathlib import Path

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from engine import Game, WIDTH, HEIGHT, TOP, FLOOR, CELL, RADIUS

ROOT = Path(__file__).resolve().parent


def save_path():
    base = Path(os.environ.get('APPDATA') or os.environ.get('XDG_DATA_HOME') or Path.home() / '.local' / 'share')
    return base / 'brick-blocks-python' / 'record.json'


def read_record():
    try:
        return max(0, int(json.loads(save_path().read_text())['record']))
    except (OSError, ValueError, KeyError, TypeError):
        return 0


class App:
    def __init__(self, muted=False):
        pygame.init()
        self.window = pygame.display.set_mode((640, 800), pygame.RESIZABLE)
        pygame.display.set_caption('Retro Brick Blast — Python')
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.fonts = {size: pygame.font.Font(None, size) for size in (20, 24, 30, 36, 44, 56)}
        self.backgrounds = []
        for i in range(10):
            path = next(ROOT.glob(f'back{i}.*'), None)
            if path:
                self.backgrounds.append(pygame.transform.scale(pygame.image.load(path).convert(), (WIDTH, FLOOR - TOP)))
        self.square = self.sprite('square.png', (CELL, CELL), 205)
        self.ball = self.sprite('ball.png', (RADIUS * 2, RADIUS * 2))
        self.pickup = self.sprite('gBall.png', (CELL, CELL), 210)
        self.game = Game()
        self.record = read_record()
        self.saved_record = self.record
        self.paused = False
        self.muted = muted
        self.track = -1
        self.play_music()

    def sprite(self, name, size, alpha=255):
        sprite = pygame.transform.smoothscale(pygame.image.load(ROOT / name).convert_alpha(), size)
        sprite.set_alpha(alpha)
        return sprite

    def play_music(self):
        track = ((self.game.round - 1) // 5) % 5
        if pygame.mixer.get_init():
            try:
                if self.track != track:
                    pygame.mixer.music.load(str(ROOT / f'song{track + 1}.ogg'))
                    pygame.mixer.music.play(-1)
                    self.track = track
                pygame.mixer.music.set_volume(0 if self.muted else 0.3)
            except pygame.error:
                pass

    def text(self, text, size, pos, color='white', centered=False):
        image = self.fonts[size].render(str(text), True, color)
        rect = image.get_rect(center=pos) if centered else image.get_rect(topleft=pos)
        self.canvas.blit(image, rect)

    def viewport(self):
        w, h = self.window.get_size()
        scale = min(w / WIDTH, h / HEIGHT)
        size = (max(1, int(WIDTH * scale)), max(1, int(HEIGHT * scale)))
        return size, ((w - size[0]) // 2, (h - size[1]) // 2)

    def pointer(self):
        size, offset = self.viewport()
        x, y = pygame.mouse.get_pos()
        return (x - offset[0]) * WIDTH / size[0], (y - offset[1]) * HEIGHT / size[1]

    def persist(self):
        if self.record <= self.saved_record:
            return
        try:
            path = save_path()
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_suffix('.tmp')
            temporary.write_text(json.dumps({'record': self.record}))
            temporary.replace(path)
            self.saved_record = self.record
        except OSError:
            pass

    def draw(self):
        g = self.game
        self.canvas.fill('#242424')
        if self.backgrounds:
            self.canvas.blit(self.backgrounds[((g.round - 1) // 5) % len(self.backgrounds)], (0, TOP))
        pygame.draw.line(self.canvas, '#8a829a', (0, FLOOR), (WIDTH, FLOOR))
        for b in g.blocks:
            self.canvas.blit(self.square, (b.x, b.y))
            pygame.draw.rect(self.canvas, '#777383', (b.x + 2, b.y + 2, CELL - 4, CELL - 4), 3, border_radius=2)
            self.text(b.hp, 30, (b.x + CELL / 2, b.y + CELL / 2), 'black', True)
        for p in g.pickups:
            self.canvas.blit(self.pickup, (p.x - CELL / 2, p.y - CELL / 2))
        if g.state == 'aim':
            direction = g.direction(*self.pointer())
            if direction and not self.paused:
                # Reflect a dotted guide against side walls and ceiling.
                x, y = g.origin, FLOOR - RADIUS
                dx, dy = direction
                for _ in range(40):
                    x, y = x + dx * 12, y + dy * 12
                    if x < RADIUS or x > WIDTH - RADIUS:
                        x = max(RADIUS, min(WIDTH - RADIUS, x))
                        dx *= -1
                    if y < TOP + RADIUS:
                        break
                    pygame.draw.circle(self.canvas, '#fa5353', (round(x), round(y)), 2)
            self.canvas.blit(self.ball, (g.origin - RADIUS, FLOOR - RADIUS * 2))
            self.text(f'×{g.count}', 24, (min(WIDTH - 60, g.origin + 20), FLOOR - 24))
        for b in g.balls:
            self.canvas.blit(self.ball, (b.x - RADIUS, b.y - RADIUS))
        if g.landing is not None and g.state == 'flight':
            self.canvas.blit(self.ball, (g.landing - RADIUS, FLOOR - RADIUS * 2))
        pygame.draw.rect(self.canvas, '#242424', (0, 0, WIDTH, TOP))
        self.text(f'Hi-Score: {self.record}', 24, (20, 10))
        self.text(f'Score: {g.round}', 24, (20, 32))
        self.text(f'Round {g.round}', 44, (WIDTH / 2, 30), centered=True)
        self.text(f'Bolas: {g.count + g.collected}', 24, (WIDTH - 125, 20))
        direction = g.direction(*self.pointer())
        angle = round(math.degrees(math.atan2(-direction[1], abs(direction[0])))) if direction else 0
        self.text(f'{angle}°', 24, (30, 874))
        self.text('P pausa   M música   R reinicia   Espaço acelera   B recolhe', 20, (120, 875))
        if self.paused or g.state == 'over':
            shade = pygame.Surface((WIDTH, FLOOR - TOP), pygame.SRCALPHA)
            shade.fill((0, 0, 0, 185))
            self.canvas.blit(shade, (0, TOP))
            self.text('PAUSADO' if self.paused else 'FIM DE JOGO', 56, (WIDTH / 2, 390), centered=True)
            self.text('P para continuar' if self.paused else f'Você chegou à rodada {g.round}', 30, (WIDTH / 2, 445), centered=True)
            self.text('R para reiniciar • Esc para sair', 24, (WIDTH / 2, 490), centered=True)
        size, offset = self.viewport()
        self.window.fill('black')
        self.window.blit(pygame.transform.smoothscale(self.canvas, size), offset)
        pygame.display.flip()

    def run(self, frames=0, screenshot=None):
        running, elapsed_frames = True, 0
        while running:
            dt = min(self.clock.tick(60) / 1000, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_p and self.game.state != 'over':
                        self.paused = not self.paused
                    elif event.key == pygame.K_m:
                        self.muted = not self.muted
                        self.play_music()
                    elif event.key == pygame.K_r:
                        self.persist()
                        self.game = Game()
                        self.paused = False
                    elif event.key == pygame.K_b and not self.paused:
                        self.game.recall()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.paused:
                    self.game.shoot(*self.pointer())
            if not self.paused:
                speed = 4 if pygame.key.get_pressed()[pygame.K_SPACE] else 1
                self.game.update(dt * speed)
            self.record = max(self.record, self.game.round)
            if self.game.state in ('aim', 'over'):
                self.persist()
            self.play_music()
            self.draw()
            elapsed_frames += 1
            if frames and elapsed_frames >= frames:
                running = False
        if screenshot:
            pygame.image.save(self.canvas, screenshot)
        self.persist()
        pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Brick Blocks em Python / Pygame')
    parser.add_argument('--mute', action='store_true', help='Inicia sem música')
    parser.add_argument('--frames', type=int, default=0, help='Encerra após N quadros (verificação)')
    parser.add_argument('--screenshot', help='Salva o último quadro em PNG')
    args = parser.parse_args()
    App(args.mute).run(args.frames, args.screenshot)
