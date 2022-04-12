# Hier werden Bibliotheken importiert die für uns jedoch erstmal nicht relevant sind
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

# Schriftart
pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# Nummernvergabe für Richtungen
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
# Tupel für Punkt und Achsen
Point = namedtuple('Point', 'x, y')

# Farbschema
WHITE = (255, 255, 255)
# Rot für das Futter
RED = (200,0,0)
# Blau 1 ist die "Schlangenhülle"
BLUE1 = (0, 0, 255)
# Blau 2 ist die innere Farbe der Schlange
BLUE2 = (0, 100, 255)
# Black ist die Farbe des Hintergrunds
BLACK = (0,0,0)

# Größe von den Blöcken - Schlange und Futter
BLOCK_SIZE = 20
# Geschwindigkeit der Schlange im Spiel
SPEED = 120

# Spielklasse
class SnakeGameAI:
    # Fenster
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display # Display wird initialisiert
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # Speichern vom vorherigen Spielstand
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    # Platzierung von dem Futter - Random
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    # Durchläufe
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input # Beenden bei Userinput
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move # Bewegung
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over # Überprüfung ob das Spiel vorbei ist
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move # Neues Futter platzieren, wenn noch nicht getroffen
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock # Update von der Ansicht und Uhr
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score # Rückgabe des Status "Spiel beendet" und Belohnung oder Bestrafung an KI verteilen
        return reward, game_over, self.score

    # Kollisionen abstecken
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary # Trifft die Seitenwände
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself # Trifft sich selbst
        if pt in self.snake[1:]:
            return True

        return False

    # Anzeige updaten
    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    # Einzelne Bewegungen
    def _move(self, action):
        # [straight, right, left] - [geradeaus, rechts, links]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)