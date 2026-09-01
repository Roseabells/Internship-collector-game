import pygame
import random

# screen dimensions 
HEIGHT = 600
WIDTH = 800

# variables
coin_count = 0
high_score = 0
checkpoint = 0
coin_images = ['meta', 'apple', 'amazon', 'netflix', 'google']

speed = 5
speedup = 1.5
ball_speed_x = 4
ball_speed_y = 3

game_state = "title"

# actors
character = Actor('cat1.png')
character.pos = 400,500
coin = Actor('meta.png')
coin.pos = 400,300
ball = Actor('ball.png')
ball.pos = 200, 200

background = Actor('background1.png')
title = Actor('title.png')
tutorial = Actor('tutorial.png')
end1 = Actor('end1.png')
end2 = Actor('end2.png')

# checks game state
def draw():
    if game_state == "title":
        draw_title_screen()
    elif game_state == "tutorial":
        draw_tutorial_screen()
    elif game_state == "playing":
        draw_game_screen()
    elif game_state == "end1":
        draw_end1_screen()
    elif game_state == "end2":
        draw_end2_screen()

# game states
def draw_game_screen():
    background.draw()
    character.draw()
    coin.draw()
    ball.draw()
    screen.draw.text(f"Internships \nCollected = {coin_count}", pos=(10,10), color ="black")

def draw_title_screen():
    title.draw()

def draw_tutorial_screen():
    tutorial.draw()

def draw_end1_screen():
    end1.draw()
    screen.draw.text(f"Internships Collected = {coin_count}", pos=(400,150), fontsize=40)
    screen.draw.text(f"High Score = {high_score}", pos=(480,190), fontsize=40)

def draw_end2_screen():
    end2.draw()
    screen.draw.text(f"Internships Collected = {coin_count}", pos=(400,150), fontsize=40)
    screen.draw.text(f"High Score = {high_score}", pos=(480,190), fontsize=40)

# resets the game to be played again
def reset_game():
    global coin_count, ball_speed_x, ball_speed_y, checkpoint
    coin_count = 0
    checkpoint = 0
    ball_speed_x = 4
    ball_speed_y = 3
    ball.pos = 200, 200
    character.pos = 400, 500
    coin.pos = 400, 300

# randomizes the bounce of the ball
def randomize_bounce():
    global ball_speed_x, ball_speed_y
    ball_speed_x += random.uniform(-0.5, 0.5)
    ball_speed_y += random.uniform(-0.5, 0.5)

# keeps track of the state of the game based on the key pressed
def on_key_down(key):
    global game_state
    if game_state == "title":
        if key == keys.SPACE:
            game_state = "playing"
        elif key == keys.RETURN:
            game_state = "tutorial"
        elif key == keys.X:
            quit()
    elif key == keys.X:
        quit()

    elif game_state == "tutorial":
        if key == keys.SPACE:
            game_state = "playing"      
        elif key == keys.X:
            quit()

    elif game_state == "end1":
        if key == keys.SPACE:
            reset_game()
            game_state = "playing"      
        elif key == keys.X:
            quit()

    elif game_state == "end2":
            if key == keys.SPACE:
                reset_game()
                game_state = "playing"      
            elif key == keys.X:
                quit()

# core of the game, updates movement, speed, coin count, and game_state
def update():
    global coin_count, ball_speed_x, ball_speed_y, checkpoint, game_state, high_score

    if game_state != "playing":
        return

    # character movement
    if (keyboard.right):
        character.left = character.left+speed
    elif (keyboard.left):
        character.left = character.left-speed
    if (keyboard.up):
        character.top = character.top-speed
    elif (keyboard.down):
        character.top = character.top+speed

    # character boarders
    if character.left < 0:
        character.left = 0
    if character.right > WIDTH:
        character.right = WIDTH
    if character.top < 0:
        character.top = 0
    if character.bottom > HEIGHT:
        character.bottom = HEIGHT

    # checks for collison with coin
    if (coin.colliderect(character)):
        x = random.randrange(coin.width // 2, WIDTH - coin.width // 2)
        y = random.randrange (coin.height // 2, HEIGHT - coin.height // 2)
        coin.pos = x, y
        coin.image = random.choice(coin_images)
        coin_count = coin_count + 1

    # speeds up the ball for every 10 coins collected
    current_count = coin_count // 10
    if current_count > checkpoint:
        checkpoint = current_count
        ball_speed_x = ball_speed_x * speedup
        ball_speed_y = ball_speed_y * speedup

    # ball movement
    ball.x = ball.x + ball_speed_x
    ball.y = ball.y + ball_speed_y

    # bounce off left/right walls
    if ball.left < 0:
        ball.left = 0
        ball_speed_x = -ball_speed_x
    if ball.right > WIDTH:
        ball.right = WIDTH
        ball_speed_x = -ball_speed_x

    # bounce off top/bottom walls
    if ball.top < 0:
        ball.top = 0
        ball_speed_y = -ball_speed_y
        randomize_bounce()
    if ball.bottom > HEIGHT:
        ball.bottom = HEIGHT
        ball_speed_y = -ball_speed_y
        randomize_bounce()

    # checks for collison with ball
    if (ball.colliderect(character)):
        if coin_count <= 20:
            if high_score < coin_count:
                high_score = coin_count
            game_state = 'end1'
        else:
            if high_score < coin_count:
                high_score = coin_count
            game_state = 'end2'
