import pygame
import random
pygame.init()

# Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
BALL_SIZE = 20 
PADDLE_SPEED = 10
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BRICK_WIDTH = 50
BRICK_HEIGHT = 20
BRICK_ROWS = 3
BRICK_COLS = 7
BRICK_PADDING = 10
BRICK_OFFSET_TOP = 50
BRICK_OFFSET_LEFT = 60
COLORS = ['#6f4e37', '#89664e', '#a47f66', '#c0997f', '#dcba99', '#ff8b00', '#f9cfb4', '#ffecd0', '#fb5aaa', '#fba0b5', '#fec5ea']

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HIT & RUN")

# Load images
ball_image = pygame.image.load("img/ball.png")
paddle_image = pygame.image.load("img/paddle.png")
brick_image = pygame.image.load("img/brick.png")

PADDLE_WIDTH, PADDLE_HEIGHT = paddle_image.get_size() 

# Game variables
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25]
ball_vel = [random.choice([-4, 4]), -4]
paddle_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 5]
bricks = []
score = 0
lives = 3
current_color_index = 0
paused = False
life_lost = False  
game_won = False  
game_over = False  

# Font
font = pygame.font.Font(None, 36)

# Create bricks
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
        brick_y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

def handle_input():
    mouse_x, _ = pygame.mouse.get_pos()
    paddle_pos[0] = mouse_x

    # Ensure the paddle stays within the screen boundaries
    if paddle_pos[0] < PADDLE_WIDTH // 2:
        paddle_pos[0] = PADDLE_WIDTH // 2
    if paddle_pos[0] > SCREEN_WIDTH - PADDLE_WIDTH // 2:
        paddle_pos[0] = SCREEN_WIDTH - PADDLE_WIDTH // 2

def draw():
    screen.fill(pygame.Color(COLORS[current_color_index]))
    screen.blit(ball_image, (ball_pos[0] - BALL_SIZE // 2, ball_pos[1] - BALL_SIZE // 2))
    screen.blit(paddle_image, (paddle_pos[0] - PADDLE_WIDTH // 2, paddle_pos[1] - PADDLE_HEIGHT // 2))
    for brick in bricks:
        screen.blit(brick_image, (brick.x, brick.y))
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
    if paused:
        if life_lost and lives > 0:
            pause_text = font.render("You lost a life! Click to continue", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))
        elif game_over:
            game_over_text = font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    if game_won:
        win_text = font.render("You won the game, Congratulations!", True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))

def change_background_color():
    global current_color_index
    current_color_index = (current_color_index + 1) % len(COLORS)

def reset_ball():
    global ball_pos, ball_vel
    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25]
    ball_vel = [random.choice([-4, 4]), -4]

def show_start_screen():
    screen.fill(BLACK)
    title_text = font.render("Pygame Brick Breaker", True, WHITE)
    start_text = font.render("Click to Start", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 50))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2 + 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def main():
    global ball_pos, ball_vel, paddle_pos, score, lives, bricks, paused, life_lost, game_won, game_over

    clock = pygame.time.Clock()
    running = True

    show_start_screen()  # Show the start screen before starting the game

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if paused and event.type == pygame.MOUSEBUTTONDOWN:
                paused = False
                life_lost = False
                reset_ball()

        if not paused and not game_won and not game_over:
            handle_input()

            # Update ball position
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]

            # Ball collision with walls
            if ball_pos[1] <= BALL_SIZE // 2:
                ball_vel[1] = -ball_vel[1]
            if ball_pos[0] <= BALL_SIZE // 2 or ball_pos[0] >= SCREEN_WIDTH - BALL_SIZE // 2:
                ball_vel[0] = -ball_vel[0]

            # Ball collision with paddle
            paddle_rect = paddle_image.get_rect(center=(paddle_pos[0], paddle_pos[1]))
            if paddle_rect.collidepoint(ball_pos[0], ball_pos[1] + BALL_SIZE // 2):
                ball_vel[1] = -ball_vel[1]
                change_background_color()

            # Ball collision with bricks
            for brick in bricks[:]:
                if brick.collidepoint(ball_pos[0], ball_pos[1] - BALL_SIZE // 2):
                    bricks.remove(brick)
                    ball_vel[1] = -ball_vel[1]
                    score += 10
                    change_background_color()
                    break

           
            if not bricks:
                game_won = True
                paused = True

            # Ball leaves screen
            if ball_pos[1] >= SCREEN_HEIGHT:
                lives -= 1
                paused = True
                life_lost = True  
                #print("You lost a life")
                if lives == 0:
                    game_over = True
                    paused = True

        draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()