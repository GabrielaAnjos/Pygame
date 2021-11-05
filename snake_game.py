import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

crash_sound = pygame.mixer.Sound('smw_coin.wav')
crash_sound.set_volume(0.6)

width = 640
height = 480

x_snake = int((width / 2 - 20))
y_snake = int(height / 2)

velocity = 6
x_control = velocity
y_control = 0

x_apple = randint(40, 600)
y_apple = randint(50, 430)
points = 0
letter1 = pygame.font.SysFont('gabriola', 40, True, False)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Draw the snake's body
list_snake = []
initial_length = 5;
dead = False

def increase_snake(list_snake):
    for XandY in list_snake:
        pygame.draw.rect(screen, (173,216,230), (XandY[0], XandY[1], 20, 20))

def restart_game():
    global points, initial_length, x_snake, y_snake, \
        list_snake, list_head, x_apple, y_apple, dead
    points = 0
    initial_length = 5
    x_snake = int((width / 2 - 20))
    y_snake = int(height / 2)
    list_snake = []
    list_head = []
    x_apple = randint(40, 600)
    y_apple = randint(50, 430)
    dead = False

while True:
    clock.tick(70)
    screen.fill((25,25,112))
    message = f'Points: {points}'
    formatted_text = letter1.render(message, False, (173,216,230))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if x_control == velocity:
                    pass
                else:
                    x_control = -velocity
                    y_control = 0
            if event.key == K_RIGHT:
                if x_control == -velocity:
                    pass
                else:
                    x_control = velocity
                    y_control = 0
            if event.key == K_UP:
                if y_control == velocity:
                    pass
                else:
                    x_control = 0
                    y_control = -velocity
            if event.key == K_DOWN:
                if y_control == -velocity:
                    pass
                else:
                    x_control = 0
                    y_control = velocity

    x_snake += x_control
    y_snake += y_control

    snake = pygame.draw.rect(screen, (173,216,230), (x_snake, y_snake, 20, 20))
    apple = pygame.draw.rect(screen, (255, 0, 0), (x_apple, y_apple, 20, 20))

    # collisions
    if snake.colliderect(apple):
        x_apple = randint(40, 600)
        y_apple = randint(50, 430)
        points += 1
        crash_sound.play()
        initial_length += 1;

    # store current position
    list_head = []
    list_head.append(x_snake)
    list_head.append(y_snake)

    # Store old positions
    list_snake.append(list_head)

    # game over
    if list_snake.count(list_head) > 1:
        letter2 = pygame.font.SysFont('arial', 25, True, True)
        message = 'Game Over! Press R to play again'
        formatted_text = letter2.render(message, True, (173,216,230))
        rect_text = formatted_text.get_rect()

        dead = True
        while dead:
            screen.fill((25,25,112))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        restart_game()
            rect_text.center = (width // 2, height // 2)
            screen.blit(formatted_text, rect_text)
            pygame.display.update()

    if x_snake > width:
        x_snake = 0
    if x_snake < 0:
        x_snake = width
    if y_snake < 0:
        y_snake = height
    if y_snake > height:
        y_snake = 0

    if len(list_snake) > initial_length:
        del list_snake[0]

    increase_snake(list_snake)

    screen.blit(formatted_text, (450, 40))
    pygame.display.update()

    '''
    Link to crash_sound:
    .wav: https://themushroomkingdom.net/media/smw/wav
    '''



