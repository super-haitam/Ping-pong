import pygame

# Vars
WIDTH, HEIGHT = 800, 500


# Player class
class Player:
    def __init__(self, paddle, vel=8, score=0):
        self.paddle = paddle
        self.vel = vel
        self.score = score

    def move_up(self):
        if self.paddle.y >= 0:
            self.paddle.y -= self.vel

    def move_down(self):
        if self.paddle.y <= HEIGHT-self.paddle.h:
            self.paddle.y += self.vel

    def handle_movement(self, key_up: str, key_down: str):
        pressed = pygame.key.get_pressed()

        # Dictionary
        keys_dict = {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "w": pygame.K_w,
            "s": pygame.K_s
        }
        pg_key_up = keys_dict[key_up]
        pg_key_down = keys_dict[key_down]

        if pressed[pg_key_up]:
            self.move_up()
        elif pressed[pg_key_down]:
            self.move_down()
