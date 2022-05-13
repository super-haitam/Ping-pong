import pygame
import sys
sys.path.append("/game_touches_help")
from game_touches_help.get_game_touches_help_img import CreateImage, get_pygame_img
from player import Player
from ball import Ball
import random
pygame.font.init()
pygame.init()


WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping pong game")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
LIGHT_GREY = (60, 60, 60)
PSEUDO_WHITE = (random.randint(240, 250), random.randint(240, 250), random.randint(240, 250))
BLACK = (0, 0, 0)
DARK_RED = (235, 50, 25)
DARK_GREEN = (15, 195, 15)
DARK_BLUE = (30, 115, 180)
RANDOM_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Choice images
robot_img = pygame.transform.scale(pygame.image.load("assets/robot_icon.png"), (WIDTH/5, HEIGHT*(7/24)))
player_img = pygame.transform.scale(pygame.image.load("assets/player_icon.png"), (WIDTH/5, HEIGHT*(7/24)))

# Choice rects
robot_rect = robot_img.get_rect()
robot_rect.x, robot_rect.y = WIDTH*(5/6)-WIDTH/5, HEIGHT*(2/3)
player_rect = player_img.get_rect()
player_rect.x, player_rect.y = WIDTH/6, HEIGHT*(2/3)

# Mode choice images
unlimited_mode_img = pygame.transform.scale(pygame.image.load("assets/infinity_mode.png"), (WIDTH/5-10, HEIGHT*(7/24)-10))
limited_mode_img = pygame.transform.scale(pygame.image.load("assets/limited_mode.jpg"), (WIDTH/5-10, HEIGHT*(7/24)-10))

# Mode choice rects
unlimited_mode_rect = unlimited_mode_img.get_rect()
unlimited_mode_rect.x, unlimited_mode_rect.y = WIDTH*(5/6)-WIDTH/5+5, HEIGHT*(2/3)+5
limited_mode_rect = limited_mode_img.get_rect()
limited_mode_rect.x, limited_mode_rect.y = WIDTH/6+5, HEIGHT*(2/3)+5

# Control touches images, Changes made in 13/5/2022
player_ctrl_help_img = get_pygame_img(CreateImage(PSEUDO_WHITE, {"Control Player1": ["up", "down"]}))
robot_ctrl_help_img = get_pygame_img(CreateImage(PSEUDO_WHITE, {"Control Player2": ['w', 's']}))
w = WIDTH / 8
player_ctrl_help_img = pygame.transform.scale(
    player_ctrl_help_img, (w, (player_ctrl_help_img.get_height()*w)/player_ctrl_help_img.get_width()))
robot_ctrl_help_img = pygame.transform.scale(
    robot_ctrl_help_img, (w, (robot_ctrl_help_img.get_height()*w)/robot_ctrl_help_img.get_width()))


# Functions
def draw_screen():
    # Screen
    screen.fill(LIGHT_GREY)
    font = pygame.font.SysFont("comicsans", 30)

    # Draw a line in the middle of the screen
    pygame.draw.aaline(screen, PSEUDO_WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT))

    # Draw rects
    pygame.draw.rect(screen, DARK_BLUE, player_pad)
    pygame.draw.rect(screen, DARK_RED, opponent_pad)
    pygame.draw.ellipse(screen, PSEUDO_WHITE, ball_rect)

    # Make the countdown for another part of the game, means when the ball goes off the screen R or L
    if ball.countdown != 0:
        # Reset every paddle
        player_pad.centery = HEIGHT/2
        opponent_pad.centery = HEIGHT/2

        countdown_text = font.render(str(ball.countdown), True, PSEUDO_WHITE)
        screen.blit(countdown_text, ((WIDTH-countdown_text.get_width())/2, HEIGHT/2+10))
        pygame.display.flip()
        pygame.time.wait(1000)

        ball.countdown -= 1

    # Scores, font and text font
    score1 = opponent.score
    score2 = player.score
    text_font1 = font.render(f"score: {score1}", True, PSEUDO_WHITE)
    text_font2 = font.render(f"score: {score2}", True, PSEUDO_WHITE)

    # Blit scores
    screen.blit(text_font1, (10, 0))
    screen.blit(text_font2, (WIDTH-text_font2.get_width()-10, 0))

    # Flip
    pygame.display.flip()


def create_rects():
    paddle1 = pygame.Rect([0, HEIGHT/2-50, 10, 100])
    paddle2 = pygame.Rect([WIDTH-10, HEIGHT/2-50, 10, 100])
    circle = pygame.Rect([WIDTH/2-10, HEIGHT/2-10, 20, 20])

    return paddle1, paddle2, circle


def draw_choice():
    screen.fill(PSEUDO_WHITE)

    # Welcome text
    font = pygame.font.SysFont("comicsans", 80)
    welcome_txt = font.render("WELCOME TO", True, BLACK)
    ping_pong_txt = font.render("PING PONG", True, RANDOM_COLOR)
    game_txt = font.render("GAME", True, BLACK)

    # Draw welcome text
    screen.blit(welcome_txt, ((WIDTH-welcome_txt.get_width())/2, 0))
    screen.blit(ping_pong_txt, ((WIDTH-ping_pong_txt.get_width())/2, HEIGHT/6))
    screen.blit(game_txt, ((WIDTH-game_txt.get_width())/2, HEIGHT/3))

    # Rect images
    choice1_rect = pygame.Rect([WIDTH/6, HEIGHT*(2/3), WIDTH/5, HEIGHT*(7/24)])
    choice2_rect = pygame.Rect([WIDTH*(5/6)-WIDTH/5, HEIGHT*(2/3), WIDTH/5, HEIGHT*(7/24)])

    # Draw rects
    pygame.draw.rect(screen, BLACK, choice1_rect, width=1)
    pygame.draw.rect(screen, BLACK, choice2_rect, width=1)

    # Draw images
    screen.blit(player_img, (player_rect.x, player_rect.y))
    screen.blit(robot_img, (robot_rect.x, robot_rect.y))

    pygame.display.flip()


def is_mouse_in_rect(mousex, mousey, rect):
    if (rect.x < mousex < mousex+rect.w) and (rect.y < mousey < mousey+rect.h):
        return True
    else:
        return False


def display_choice_limit():
    screen.fill(PSEUDO_WHITE)

    # Create the text
    font = pygame.font.SysFont('comicsans', 80)
    choosethe_txt = font.render('Choose the', True, BLACK)
    gamemode_txt = font.render('game mode', True, BLACK)

    # Rect images
    choice1_rect = pygame.Rect([WIDTH / 6, HEIGHT * (2 / 3), WIDTH / 5, HEIGHT * (7 / 24)])
    choice2_rect = pygame.Rect(
        [WIDTH * (5 / 6) - WIDTH / 5, HEIGHT * (2 / 3), WIDTH / 5, HEIGHT * (7 / 24)])

    # Display the text
    screen.blit(choosethe_txt, ((WIDTH - choosethe_txt.get_width()) / 2, HEIGHT / 15))
    screen.blit(gamemode_txt, ((WIDTH - gamemode_txt.get_width()) / 2, HEIGHT / 4))

    # Draw the rectangles
    pygame.draw.rect(screen, BLACK, choice1_rect, width=1)
    pygame.draw.rect(screen, BLACK, choice2_rect, width=1)

    # Blit the mode choice images
    screen.blit(unlimited_mode_img, (unlimited_mode_rect.x, unlimited_mode_rect.y))
    screen.blit(limited_mode_img, (limited_mode_rect.x, limited_mode_rect.y))

    # Blit ctrl touches
    screen.blit(player_ctrl_help_img, (WIDTH*(1-1/6), HEIGHT/4))
    if bool_player:
        screen.blit(robot_ctrl_help_img, (WIDTH/14, HEIGHT/4))

    # Flip
    pygame.display.flip()


def show_winner(winner: str):
    screen.fill(PSEUDO_WHITE)

    # Define a color for the winner txt
    if winner == "player1":
        winner_color = DARK_BLUE
    elif winner == "player2":
        winner_color = DARK_RED

    # Create the font & the texts
    font = pygame.font.SysFont('comicsans', 80)
    thewinner_txt = font.render("The winner", True, BLACK)
    is_txt = font.render("is", True, BLACK)
    winner_txt = font.render(winner.capitalize(), True, winner_color)

    # Blit the texts
    screen.blit(thewinner_txt, ((WIDTH-thewinner_txt.get_width())/2, HEIGHT/6))
    screen.blit(is_txt, ((WIDTH-is_txt.get_width())/2, HEIGHT/3))
    screen.blit(winner_txt, ((WIDTH-winner_txt.get_width())/2, HEIGHT/2))

    # Flip
    pygame.display.flip()

    pygame.time.wait(3000)


def check_victory(amount, player1, player2) -> str:
    if player1.score >= amount:
        return "player1"
    elif player2.score >= amount:
        return "player2"


# Having the created rects
opponent_pad, player_pad, ball_rect = create_rects()

# Instances
player = Player(player_pad)
opponent = Player(opponent_pad, vel=4)
ball = Ball(ball_rect, player, opponent)

# Main loop
run = True
is_started = False
is_choosing_limit = False

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not is_started and is_choosing_limit:
                # What mode did the player choose to play
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if is_mouse_in_rect(mouse_x, mouse_y, limited_mode_rect):
                    limited_mode = True
                    is_choosing_limit = False
                    is_started = True
                if is_mouse_in_rect(mouse_x, mouse_y, unlimited_mode_rect):
                    limited_mode = False
                    is_choosing_limit = False
                    is_started = True

            if not is_started and not is_choosing_limit:
                # What opponent did the player choose to play with
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if is_mouse_in_rect(mouse_x, mouse_y, robot_rect):
                    bool_player, bool_pc = False, True
                    is_choosing_limit = True
                elif is_mouse_in_rect(mouse_x, mouse_y, player_rect):
                    bool_player, bool_pc = True, False
                    is_choosing_limit = True

            if not is_started and is_choosing_limit:
                display_choice_limit()

    if is_started and not is_choosing_limit:
        draw_screen()
        ball.move()

        # Look for any win
        if limited_mode:
            winner = check_victory(7, player, opponent)
            if isinstance(winner, str):
                if winner == "player1":
                    show_winner(winner)
                    is_started = False
                elif winner == "player2":
                    show_winner(winner)
                    is_started = False

        # Handle player and opponent movement
        player.handle_movement("up", "down")
        if bool_player:
            opponent.handle_movement('w', 's')
            opponent.vel = player.vel
        elif bool_pc:
            # Here will be the code to handle pc's movement, when the ball moves
            if opponent_pad.centery > ball_rect.centery:
                opponent.move_up()
            if opponent_pad.centery < ball_rect.centery:
                opponent.move_down()

    elif not is_started and not is_choosing_limit:
        player.score = opponent.score = 0
        draw_choice()


# AAH! FINALLY DONE, I don't know how much time I spent doing this project... Probably more than 5, or does it seem
# to me? Anyway, I finally did it and I'm pretty proud of it!

# IDEA FROM THE YT CHANNEL: "Clear Code"..
# ACTUALLY NOT ONLY THE IDEA ,I ALSO DIDN'T KNOW HOW TO BOUNCE THE BALL [FOOLISH ME :) ]

# Made by Haitam Laghmam, a beginner programmer that codes to fight depression caused by his catastrophic grades ;)
# I burst out of laughter when reading this 2 days before my birthday, Happy Birthday to me .. both me & you then. lol
# Last touches: 4/2/2022 at 15:30
