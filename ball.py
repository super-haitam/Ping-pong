import random

# Variables
WIDTH, HEIGHT = 800, 500


# Ball Class
class Ball:
    def __init__(self, rect, player1, player2, speed=5):
        # Random where the ball will go in the first time !!! Actually better to random the direction for better game
        rand_x = random.choice([-1, 1])
        rand_y = random.choice([-1, 1])

        self.speed = speed
        self.speed_x, self.speed_y = self.speed * rand_x, self.speed * rand_y
        self.rect = rect

        # Self form of the Instances
        self.player1 = player1
        self.player2 = player2

        # Paddles
        self.pad1 = self.player1.paddle
        self.pad2 = self.player2.paddle

        self.countdown = 3

    def bounce(self, axis: str):
        if axis == 'x':
            self.speed_x *= -1
        elif axis == 'y':
            self.speed_y *= -1

    def is_collided(self, pad):
        if (pad.x <= self.rect.center[0] <= pad.x + pad.w) and (pad.y <= self.rect.center[1] <= pad.y + pad.h):
            return True
        else:
            return False

    def reset_pos(self):
        self.rect.x = (WIDTH-self.rect.w)/2
        self.rect.y = (HEIGHT-self.rect.h)/2

        # Random where the ball will go in the first time !!! Actually better to random the direction for better game
        rand_x = random.choice([-1, 1])
        rand_y = random.choice([-1, 1])

        self.speed_x, self.speed_y = self.speed * rand_x, self.speed * rand_y

    def ball_off(self):
        if self.rect.centerx < 0:
            self.player1.score += 1
            self.reset_pos()
        if WIDTH < self.rect.centerx:
            self.player2.score += 1
            self.reset_pos()

        self.countdown = 3

    def move(self):
        if self.countdown == 0:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # Bounce when collision with up and down borders
            if not 0 <= self.rect.centery <= HEIGHT:
                self.bounce('y')

            # Bounce when collision with either pad1 or pad2
            if self.is_collided(self.pad1) or self.is_collided(self.pad2):
                self.bounce('x')

            # Check when the ball goes off right and left borders, to count the points and make countdown == True
            if not 0 <= self.rect.centerx <= WIDTH:
                self.ball_off()
