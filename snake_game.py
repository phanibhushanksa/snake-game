import pygame
import random
import sys
from enum import Enum
from collections import namedtuple

# Initialize Pygame
pygame.init()

# Colors
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    BLUE1 = (0, 0, 255)
    BLUE2 = (0, 100, 255)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 100, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)

# Direction enum
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Point named tuple
Point = namedtuple('Point', 'x, y')

class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.block_size = 20
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        
        # Initialize game state
        self.direction = Direction.RIGHT
        self.head = Point(self.width//2, self.height//2)
        self.snake = [self.head, 
                     Point(self.head.x-self.block_size, self.head.y),
                     Point(self.head.x-(2*self.block_size), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.game_over = False
        self.paused = False
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def _place_food(self):
        x = random.randint(0, (self.width-self.block_size)//self.block_size)*self.block_size
        y = random.randint(0, (self.height-self.block_size)//self.block_size)*self.block_size
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self):
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                if not self.paused and not self.game_over:
                    if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                    elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.direction = Direction.DOWN
        
        if self.paused or self.game_over:
            return
            
        # 2. Move
        self._move(self.direction)
        self.snake.insert(0, self.head)
        
        # 3. Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            self.game_over = True
            return game_over, self.score
            
        # 4. Place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(10)
        
        # 6. Return game over and score
        return game_over, self.score
    
    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.width - self.block_size or pt.x < 0 or pt.y > self.height - self.block_size or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(Colors.BLACK)
        
        # Draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, Colors.BLUE1, pygame.Rect(pt.x, pt.y, self.block_size, self.block_size))
            pygame.draw.rect(self.display, Colors.BLUE2, pygame.Rect(pt.x+4, pt.y+4, self.block_size-8, self.block_size-8))
        
        # Draw head
        pygame.draw.rect(self.display, Colors.DARK_GREEN, pygame.Rect(self.head.x, self.head.y, self.block_size, self.block_size))
        pygame.draw.rect(self.display, Colors.GREEN, pygame.Rect(self.head.x+4, self.head.y+4, self.block_size-8, self.block_size-8))
        
        # Draw food
        pygame.draw.rect(self.display, Colors.RED, pygame.Rect(self.food.x, self.food.y, self.block_size, self.block_size))
        
        # Draw score
        text = self.font.render(f'Score: {self.score}', True, Colors.WHITE)
        self.display.blit(text, [0, 0])
        
        # Draw instructions
        instructions = [
            "Arrow Keys: Move",
            "Space: Pause",
            "R: Restart (when game over)",
            "ESC: Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, Colors.LIGHT_GRAY)
            self.display.blit(text, [self.width - 200, 10 + i * 20])
        
        # Draw pause or game over message
        if self.paused:
            text = self.font.render('PAUSED', True, Colors.WHITE)
            text_rect = text.get_rect(center=(self.width//2, self.height//2))
            self.display.blit(text, text_rect)
        elif self.game_over:
            text = self.font.render('GAME OVER!', True, Colors.RED)
            text_rect = text.get_rect(center=(self.width//2, self.height//2 - 30))
            self.display.blit(text, text_rect)
            
            restart_text = self.small_font.render('Press R to restart', True, Colors.WHITE)
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 10))
            self.display.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += self.block_size
        elif direction == Direction.LEFT:
            x -= self.block_size
        elif direction == Direction.DOWN:
            y += self.block_size
        elif direction == Direction.UP:
            y -= self.block_size
        self.head = Point(x, y)
    
    def reset_game(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.width//2, self.height//2)
        self.snake = [self.head, 
                     Point(self.head.x-self.block_size, self.head.y),
                     Point(self.head.x-(2*self.block_size), self.head.y)]
        self.score = 0
        self._place_food()
        self.game_over = False
        self.paused = False

def main():
    game = SnakeGame()
    
    # Game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            break
    
    print(f'Final Score: {score}')
    pygame.quit()

if __name__ == '__main__':
    main() 