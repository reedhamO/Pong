import pygame
import sys
import random


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_three = timer_font.render("3", False, red)
        screen.blit(number_three, (screen_width/2 - 20, 10))

    if 700 < current_time - score_time < 1400:
        number_two = timer_font.render("2", False, red)
        screen.blit(number_two, (screen_width/2 - 20, 10))

    if 1400 < current_time - score_time < 2100:
        number_one = timer_font.render("1", False, red)
        screen.blit(number_one, (screen_width/2 - 15, 10))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 3.5 * random.choice((1, -1))
        ball_speed_y = 3.5 * random.choice((1, -1))
        score_time = None


def player_animation():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


# General Setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15/2, screen_height/2 - 15/2, 15, 15)
player = pygame.Rect(screen_width - 10, screen_height/2 - 35, 5, 70)
opponent = pygame.Rect(5, screen_height/2 - 35, 5, 70)

# Colours
bg_color = pygame.Color('#2d2d2d')
light_grey = (241, 241, 241)
blue = (52, 132, 240)
red = (219, 68, 55)
green = pygame.Color('#65ED99')

# Game Variables
ball_speed_x = 3.5 * random.choice((1, -1))
ball_speed_y = 3.5 * random.choice((1, -1))
player_speed = 0
opponent_speed = 3.5

# Text Variables (Score)
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("Montserrat-Medium.ttf", 18)
timer_font = pygame.font.Font("Montserrat-Bold.ttf", 70)

# Score Timer
score_time = True

# Sound
# collision_sound = pygame.mixer.Sound('pong.ogg')

while True:
    # Handling Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 3.5
            if event.key == pygame.K_UP:
                player_speed -= 3.5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 3.5
            if event.key == pygame.K_UP:
                player_speed += 3.5

    ball_animation()
    player.y += player_speed
    player_animation()
    opponent_animation()
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, red, opponent)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height,))
    pygame.draw.ellipse(screen, blue, ball)

    player_text = game_font.render(f"{player_score}", False, green)
    screen.blit(player_text, (screen_width/2 + 10, 235))

    opponent_text = game_font.render(f"{opponent_score}", False, green)
    screen.blit(opponent_text, (screen_width/2 - 20, 235))

    if score_time:
        ball_restart()

    # Updating the window
    pygame.display.flip()
    clock.tick(60)
