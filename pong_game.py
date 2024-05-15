import sys
import pygame
import random


def random_color():
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    return color


def ball_animation():
    global ball_speed_x, ball_speed_y, ball_color, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Vertical bounce / y axis
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Player score
    if ball.right <= 0:
        ball_reset()
        player_score += 1

    # Opponent score
    if ball.left >= screen_width:
        ball_reset()
        opponent_score += 1

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
            ball_color = random_color()
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
            ball_color = random_color()
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_x *= -1
            ball_color = random_color()

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
            ball_color = random_color()
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
            ball_color = random_color()
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_x *= -1
            ball_color = random_color()


def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    if opponent.centery < ball.centery:
        opponent.y += opponent_speed
    if opponent.centery > ball.centery:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_reset():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_y *= random.choice((-1, 1))
    ball_speed_x *= random.choice((-1, 1))


def pause():
    loop = 1
    pause_text = game_font.render("PAUSED", False, white)
    screen.blit(pause_text, (498, 275))
    continue_text = game_font.render("press SPACE to continue", False, white)
    screen.blit(continue_text, (250, 425))

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    loop = 0
        pygame.display.update()


def game_status():
    global player_score, opponent_score
    win = False

    if player_score >= win_score:
        win = True
        win_text = "You win!"
    elif opponent_score >= win_score:
        win = True
        win_text = "You loose"

    if win:
        text = game_font.render(win_text, False, white)
        screen.blit(text, (498, 275))
        pygame.display.update()
        pygame.time.delay(3000)
        ball_reset()
        player_score = 0
        opponent_score = 0


# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the Main Window
screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game Rectangles (x, y, width, height)
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 15, 140)
opponent = pygame.Rect(5, screen_height/2 - 70, 15, 140)

# Game variables
ball_speed_x = 7 * random.choice((-1, 1))
ball_speed_y = 6 * random.choice((-1, 1))
player_speed = 0
opponent_speed = 7

win_score = 5

# Text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 70)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

ball_color = white
bg_color = black

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause()
            if event.key == pygame.K_DOWN:
                player_speed += 6
            if event.key == pygame.K_UP:
                player_speed -= 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 6
            if event.key == pygame.K_UP:
                player_speed += 6

    # Game Logic
    ball_animation()
    player_animation()
    opponent_animation()
    game_status()

    # Display
    screen.fill(bg_color)
    pygame.draw.rect(screen, blue, player)
    pygame.draw.rect(screen, red, opponent)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, white, (screen_width/2, 0), (screen_width/2, screen_height))

    player_text = game_font.render(f"{player_score}", False, blue)
    screen.blit(player_text, (660, 15))

    opponent_text = game_font.render(f"{opponent_score}", False, red)
    screen.blit(opponent_text, (585, 15))

    # Updating the window
    pygame.display.flip()
    clock.tick(60)  # FPS
