import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
LIGHTBLUE = (173, 216, 230)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

def main_menu():
    while True:
        screen.fill(LIGHTBLUE)
        
        # Title text
        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("Welcome to the Snake Game!", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)
        
        # Instructions text
        instruct_font = pygame.font.Font(None, 30)
        instruct_text = instruct_font.render("Press SPACE to Play or Press Q to Quit", True, WHITE)
        instruct_rect = instruct_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(instruct_text, instruct_rect)
        
        pygame.display.update()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_q:
                    return False

# Quit function
def quit_game():
    pygame.quit()
    sys.exit()

class SnakeGame:
    def __init__(self):
        # Initialize game parameters
        self.snake = [(300, 300)]
        self.food = self.generate_food()
        self.direction = "Right"
        self.score = 0
        self.paused = False
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((600, 600))
        self.font = pygame.font.Font(None, 36)
        
        # Start the game loop
        self.move_snake()
    
    def generate_food(self):
        x = random.randint(0, 29) * 20
        y = random.randint(0, 29) * 20
        return (x, y)
    
    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.screen, (143, 0, 255), (segment[0], segment[1], 20, 20))
    
    def draw_food(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.food[0], self.food[1], 20, 20))
    
    def change_direction(self, event):
        if event.key == pygame.K_UP and self.direction != "Down":
            self.direction = "Up"
        elif event.key == pygame.K_DOWN and self.direction != "Up":
            self.direction = "Down"
        elif event.key == pygame.K_LEFT and self.direction != "Right":
            self.direction = "Left"
        elif event.key == pygame.K_RIGHT and self.direction != "Left":
            self.direction = "Right"
        elif event.key == pygame.K_p:
            self.toggle_pause()
            if self.paused:
                self.show_pause_sign()
            else:
                self.screen.fill(LIGHTBLUE)
        elif event.key == pygame.K_r:
            self.restart_game()
    
    def restart_game(self):
        self.snake = [(300, 300)]
        self.food = self.generate_food()
        self.direction = "Right"
        self.score = 0
        self.paused = False
    
    def move_snake(self):
        while True:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.KEYDOWN:
                    self.change_direction(event)

            if not self.paused:
                head = list(self.snake[0])

                if self.direction == "Up":
                    head[1] -= 20
                elif self.direction == "Down":
                    head[1] += 20
                elif self.direction == "Left":
                    head[0] -= 20
                elif self.direction == "Right":
                    head[0] += 20

                if head == list(self.food):
                    self.snake.insert(0, head)
                    self.score += 1
                    self.food = self.generate_food()
                else:
                    self.snake.pop()
                    self.snake.insert(0, head)

                if self.check_collision():
                    self.game_over()

                self.screen.fill(LIGHTBLUE)
                self.draw_snake()
                self.draw_food()
                self.draw_score() 
                pygame.display.update()

    def toggle_pause(self):
        self.paused = not self.paused
    
    def show_pause_sign(self):
        pause_text = self.font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        pygame.display.update()

    def check_collision(self):
        head = self.snake[0]
        
        if head[0] < 0 or head[0] >= 600 or head[1] < 0 or head[1] >= 600:
            return True
        
        for segment in self.snake[1:]:
            if head == segment:
                return True

    def game_over(self):
        gameover = pygame.font.Font(None, 50)
        game_over_text = gameover.render(f"Game Over! Your score is: {self.score}", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        game_over_image = pygame.image.load("bg.png")
        image_rect = game_over_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 175))
        self.screen.blit(game_over_image, image_rect)

        text1 =  pygame.font.Font(None, 24)
        text = text1.render("Press SPACE to Play Again and Press Q to Quit", True, (128, 128, 128))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25))
        self.screen.blit(text, rect)

        pygame.display.update()

        # Wait for any key press to start a new game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
                        waiting = False
                    elif event.key == pygame.K_q:
                        quit_game()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(score_text, score_rect)

def main():
    while True:
        if not main_menu():
            break
        game = SnakeGame()
        game.move_snake()

if __name__ == "__main__":
    main()
