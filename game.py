import pygame
import sys
from constants import WIDTH, HEIGHT, CELL_SIZE, FPS, BLACK, WHITE, GREEN, DARK_GREEN, RED, GRAY
from snake import Snake
import random

class Game:
    def __init__(self):
        pygame.init()
        self.snake = Snake()
        self.is_over = False
        self.score = 0
        self.food_pos = None
        self.difficulty = None
        self.walls = []
        self.direction = 'd'  # Initial direction is right
        self.screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
        self.clock = pygame.time.Clock()

    def start_screen(self):
        waiting = True
        font = pygame.font.SysFont(None, 48)  # None = default font, 48 = size
        text_surface = font.render("Welcome to Snake!", True, WHITE)
        self.screen.fill(BLACK)
        self.screen.blit(text_surface, (50, (HEIGHT * CELL_SIZE) // 2))  # blit = draw surface onto surface
        pygame.display.flip()
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def difficulty_screen(self):
        waiting = True
        font = pygame.font.SysFont(None, 48)  # None = default font, 48 = size
        line1 = font.render("Choose a difficulty:", True, WHITE)
        line2 = font.render("1 - Easy: walls only", True, WHITE)
        line3 = font.render("2 - Normal: walls + self collision", True, WHITE)
        line4 = font.render("3 - Hard: normal + barriers", True, WHITE)
        self.screen.fill(BLACK)
        self.screen.blit(line1, (50, 150))
        self.screen.blit(line2, (50, 220))
        self.screen.blit(line3, (50, 290))  # blit = draw surface onto surface
        self.screen.blit(line4, (50, 360))
        pygame.display.flip()
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.difficulty = 'easy'
                        waiting = False
                    elif event.key == pygame.K_2:
                        self.difficulty = 'normal'
                        waiting = False
                    elif event.key == pygame.K_3:
                        self.difficulty = 'hard'
                        waiting = False

    def generate_food(self):
        while True:
            food_pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if food_pos not in self.snake.segments:
                return food_pos
            
    def generate_walls(self):
        while True:
            wall_pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if wall_pos not in self.snake.segments and wall_pos not in self.walls and wall_pos != self.food_pos:
                self.walls.append(wall_pos)
                return
    
    def run(self):
        self.start_screen()
        self.difficulty_screen()
        self.food_pos = self.generate_food()
    
        while not self.is_over: #loop
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
    
        self.show_game_over()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.direction != 's':
                    self.direction = 'w'
                elif event.key == pygame.K_s and self.direction != 'w':
                    self.direction = 's'
                elif event.key == pygame.K_a and self.direction != 'd':
                    self.direction = 'a'
                elif event.key == pygame.K_d and self.direction != 'a':
                    self.direction = 'd'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.snake.move(self.direction)
        if self.check_collision():
            self.is_over = True
        if self.check_food():
            self.snake.grow()
            self.score += 1
            self.food_pos = self.generate_food()
            if self.difficulty == 'hard':
                self.generate_walls()

    def check_collision(self):
        head_x, head_y = self.snake.head_position()
        # out of bounds
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True
        # Check self collision
        if self.difficulty in ['normal', 'hard'] and (head_x, head_y) in self.snake.segments[1:]:
            return True
        # Check barrier collision
        if self.difficulty == 'hard' and (head_x, head_y) in self.walls:
            return True
        return False
    
    def check_food(self):
        return self.snake.head_position() == self.food_pos
    
    def draw(self):
        self.screen.fill(BLACK)
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) == self.food_pos:
                    COLOR = RED
                elif (x, y) in self.walls:
                    COLOR = GRAY
                elif (x, y) == self.snake.head_position():
                    COLOR = DARK_GREEN
                elif (x, y) in self.snake.segments:
                    COLOR = GREEN
                else:
                    COLOR = BLACK
                pygame.draw.rect(self.screen, COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text_surface, (5, 5))  # blit = draw surface onto surface
        pygame.display.flip()


    def show_game_over(self):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(None, 48)  # None = default font, 48 = size
        text_surface = font.render(f"Game Over! Score: {self.score}", True, WHITE)
        self.screen.blit(text_surface, (WIDTH * CELL_SIZE // 2 - text_surface.get_width() // 2, HEIGHT * CELL_SIZE // 2 - text_surface.get_height() // 2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
