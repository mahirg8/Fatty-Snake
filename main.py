import pygame
import random
import os

pygame.mixer.init()

pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

screen_width = 800
screen_height = 600
# creating window
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fatty Snake by Mahir')
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# bg image
bgimg = pygame.image.load('data/bg.png')
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
gameover= pygame.image.load('data/gameover.png').convert_alpha()

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((250, 150, 210))
        text_screen("Welcome to FATTY SNAKE", black, 150, 230)
        text_screen("Press Space Bar To Play!", black, 170, 280)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('data/Caballero - Ofshane.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# game loop
def gameloop():
    # game specific var
    exit_game = False
    game_over = False
    snake_x = 20
    snake_y = 30
    vel_x = 2
    vel_y = 2
    snake_list = []
    snake_length = 1
    # check if highscore file exist
    if (not os.path.exists('data\highscore')):
        with open('data\highscore', 'w') as f:
            f.write('0')
    with open('data\highscore', 'r') as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_vel = 6
    snake_size = 17
    fps = 60

    while not exit_game:
        if game_over:
            with open('data\highscore', 'w') as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(gameover, (100,120))
            text_screen('Press Enter To Continue', red, 200, 450)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        vel_x = init_vel
                        vel_y = 0

                    if event.key == pygame.K_LEFT:
                        vel_x = -init_vel
                        vel_y = 0

                    if event.key == pygame.K_DOWN:
                        vel_y = init_vel
                        vel_x = 0

                    if event.key == pygame.K_UP:
                        vel_y = - init_vel
                        vel_x = 0

                    # cheat codes
                    if event.key == pygame.K_q:
                        score += 10

                    if event.key == pygame.K_SPACE:
                        init_vel -= 1

            snake_x = snake_x + vel_x
            snake_y = snake_y + vel_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snake_length += 4
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen('Score: ' + str(score) + '  HighScore: ' + str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('data/gameover.mp3.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('data/gameover.mp3.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    quit()


welcome()

gameloop()
