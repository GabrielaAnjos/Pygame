import pygame, sys

class Ball:
    def __init__(self, screen, color, posX, posY, radius):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.show()

    def show(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    def start_moving(self):
        self.dx = 0.2
        self.dy = -0.2

    def move(self):
        self.posX += self.dx
        self.posY += self.dy

    def paddle_collision(self):
        self.dx = -self.dx

    def wall_collision(self):
        self.dy = -self.dy

    def restart_pos_ball(self):
        self.posX = WIDTH//2
        self.posY = HEIGHT//2
        self.dx = 0
        self.dy = 0
        self.show()

class Paddle:
    def __init__(self, screen, color, posX, posY, width, height):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.state = 'stopped'
        self.show()

    def show(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width, self.height))

    def move(self):
        if self.state == 'up':
            self.posY -= 0.5

        elif self.state == 'down':
            self.posY += 0.5

    def clamp(self):
        if self.posY <= 0:
            self.posY = 0

        if self.posY + self.height >= HEIGHT:
            self.posY = HEIGHT - self.height

    def restart_pos_paddle(self):
        self.posY = HEIGHT//2 - self.height//2
        self.state = 'Stopped'
        self.show()

class Score:
    def __init__(self, screen, points, posX, posY):
        self.screen = screen
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("monospace", 80, bold=True)
        self.label = self.font.render(self.points, 0, COLOR)
        self.show()

    def show(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

    def increase(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, COLOR)

    def restart_score(self):
        self.points = '0'
        self.label = self.font.render(self.points, 0, COLOR)

class Message:
    def __init__(self, screen, text, posX, posY):
        self.screen = screen
        self.text = text
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("monospace", 20, bold=False)
        self.label = self.font.render(self.text, 0, COLOR)
        self.show()

    def show(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

    def message(self):
        self.label = self.font.render(self.screen, 0, COLOR)

class CollisionManager:
    def between_ball_and_paddle1(self, ball, paddle1):
        if ball.posY + ball.radius > paddle1.posY and ball.posY - ball.radius < paddle1.posY + paddle1.height:
            if ball.posX - ball.radius <= paddle1.posX + paddle1.width:
                return True
        return False

    def between_ball_and_paddle2(self, ball, paddle2):
        if ball.posY + ball.radius > paddle2.posY and ball.posY - ball.radius < paddle2.posY + paddle2.height:
            if ball.posX + ball.radius >= paddle2.posX:
                return True
        return False

    def between_ball_and_walls(self, ball):
        # top collision
        if ball.posY - ball.radius <= 0:
            return True

        # botton collision
        if ball.posY + ball.radius >= HEIGHT:
            return True

        return False

    def check_goal_player1(self, ball):
        return ball.posX - ball.radius >= WIDTH

    def check_goal_player2(self, ball):
        return ball.posX + ball.radius <= 0

pygame.init()

WIDTH = 900
HEIGHT = 500
SCREENCOLOR = (102, 0, 51)
COLOR = (200, 200, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PING PONG')

def paint_back():
    screen.fill(SCREENCOLOR)
    pygame.draw.line(screen, COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

def restart():
    paint_back()
    score1.restart_score()
    score2.restart_score()
    ball.restart_pos_ball()
    paddle1.restart_pos_paddle()
    paddle2.restart_pos_paddle()

paint_back()

# OBJECTS
ball = Ball(screen, COLOR, WIDTH // 2, HEIGHT // 2, 12)
paddle1 = Paddle(screen, COLOR, 15, HEIGHT // 2 - 50, 20, 100)
paddle2 = Paddle(screen, COLOR, WIDTH - 20 - 15, HEIGHT // 2 - 50, 20, 100)
collision = CollisionManager()
score1 = Score(screen, '0', WIDTH//4, 15)
score2 = Score(screen, '0', WIDTH - WIDTH//4, 15)
text = Message(screen,'   P: Play  R: Restart' ,WIDTH//2, 415)
text1 = Message(screen, 'W: up & S: down', WIDTH//4, 450)
text2 = Message(screen, 'UP: up & DOWN: down', WIDTH - WIDTH//4, 450)

# VARIABLES
playing = False

# main loop
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                ball.start_moving()
                playing = True

            if event.key == pygame.K_r:
                restart()
                playing = False

            if event.key == pygame.K_w:
                paddle1.state = 'up'

            if event.key == pygame.K_s:
                paddle1.state = 'down'

            if event.key == pygame.K_UP:
                paddle2.state = 'up'

            if event.key == pygame.K_DOWN:
                paddle2.state = 'down'

        if event.type == pygame.KEYUP:
            paddle1.state = 'stopped'
            paddle2.state = 'stopped'

    if playing:
        paint_back()

        # ball movement
        ball.move()
        ball.show()

        # paddle 1
        paddle1.move()
        paddle1.clamp()
        paddle1.show()

        # paddle 2
        paddle2.move()
        paddle2.clamp()
        paddle2.show()

        # check for collisions
        if collision.between_ball_and_paddle1(ball, paddle1):
            ball.paddle_collision()

        if collision.between_ball_and_paddle2(ball, paddle2):
            ball.paddle_collision()

        if collision.between_ball_and_walls(ball):
            ball.wall_collision()

        if collision.check_goal_player1(ball):
            paint_back()
            score1.increase()
            ball.restart_pos_ball()
            paddle1.restart_pos_paddle()
            paddle2.restart_pos_paddle()
            playing = False

        if collision.check_goal_player2(ball):
            paint_back()
            score2.increase()
            ball.restart_pos_ball()
            paddle1.restart_pos_paddle()
            paddle2.restart_pos_paddle()
            playing = False

    score1.show()
    score2.show()

    pygame.display.update()