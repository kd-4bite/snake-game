import pygame
import random
import os

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 1080, 720
GRID_SIZE = 65
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_SPEED = 6

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Sound Effects")
clock = pygame.time.Clock()

# Load custom food image
def load_food_image():
    try:
        food_img = pygame.image.load('Screenshot 2025-05-02 085709.png')
        food_img = pygame.transform.scale(food_img, (GRID_SIZE, GRID_SIZE))
        return food_img
    except:
        print("Custom food image not found. Using default red square.")
        return None

# Load sound effects
def load_sounds():
    sounds = {}
    try:
        sounds["eat"] = pygame.mixer.Sound('gopgopgop-[AudioTrimmer.com] (1).wav')
    except:
        print("Custom eat sound not found. Using default beep.")
        sound = pygame.mixer.Sound(buffer=bytes([127] * 8000))  # Simple beep
        sounds["eat"] = sound
    
    try:
        sounds["game_over"] = pygame.mixer.Sound('aah-aah-chud-gai-chud-gai-made-with-Voicemod-[AudioTrimmer.com] (1).mp3')
    except:
        print("Custom game over sound not found. Using default sound.")
        sound = pygame.mixer.Sound(buffer=bytes([127, 0] * 4000))  # Different beep
        sounds["game_over"] = sound
    
    return sounds

food_image = load_food_image()
sounds = load_sounds()

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x) % GRID_WIDTH
        new_y = (head_y + dir_y) % GRID_HEIGHT
        
        if (new_x, new_y) in self.positions[1:]:
            sounds["game_over"].play()  # Play game over sound
            return False
            
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()
        return True
    
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        self.score = 0
    
    def render(self, surface):
        for p in self.positions:
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        if food_image:
            surface.blit(food_image, rect)
        else:
            pygame.draw.rect(surface, RED, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BLACK, rect, 1)

def show_game_over(surface, score):
    font = pygame.font.SysFont('arial', 48)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    restart = font.render("Press R to restart", True, WHITE)
    surface.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 80))
    surface.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))

def main():
    snake = Snake()
    food = Food()
    running = True
    game_over = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if not game_over:
            if not snake.update():
                game_over = True
            
            # Check if snake eats food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                sounds["eat"].play()  # Play eating sound
                food.randomize_position()
                while food.position in snake.positions:
                    food.randomize_position()
        
        # Drawing
        screen.fill(BLACK)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        
        # Display score
        font = pygame.font.SysFont('arial', 28)
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (30, 30))
        
        if game_over:
            show_game_over(screen, snake.score)
        
        pygame.display.update()
        clock.tick(SNAKE_SPEED)
    
    pygame.quit()

if __name__ == "__main__":
    main()