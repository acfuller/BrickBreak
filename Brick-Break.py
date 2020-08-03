# Brick Break - A wonderful game
# Plan to make base game, then add an AI to play it
# Also seperately plan to make this an idle game as well (for fun)

x = 100
y = 30
import pygame
import neat
import time
import os
import random

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

pygame.font.init()

# Setting the size of the game window
WIN_WIDTH = 1200
WIN_HEIGTH = 700

# Pictures for game assets
TILE_IMGS = [pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "blue_tile.png")), 0, 0.35), pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "green_tile.png")), 0, 0.35), pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "red_tile.png")), 0, 0.35), pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "purple_tile.png")), 0, 0.35), pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "yellow_tile.png")), 0, 0.35)]
TILE_IMG = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "blue_tile.png")), 0, 0.15)
BALL_IMG = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "ball.png")), 0, 0.15)
PADDLE_IMG = pygame.transform.rotozoom(pygame.image.load(os.path.join("imgs", "paddle.png")), 0, 0.15)
BG_IMG = pygame.image.load(os.path.join("imgs", "bg.png"))

STAT_FONT = pygame.font.SysFont("comicsans", 35)


class Ball:
    IMG = BALL_IMG
    X_VEL = 4
    Y_VEL = 4

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attack = 1
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        self.x += self.X_VEL
        self.y += self.Y_VEL

        if self.x > 1182 or self.x < 0:
            self.X_VEL = self.X_VEL * -1
        elif self.y < 0:
            self.Y_VEL = self.Y_VEL * -1
        elif self.y > 682:
            run = False
            pygame.quit()
            quit()

    def collide(self, paddle, tile):
        ball_mask = pygame.mask.from_surface(self.IMG)
        paddle_mask = paddle.get_mask()
        tile_mask = tile.get_mask()

        paddle_offset = (paddle.x - self.x, paddle.y - round(self.y))
        tile_offset = (tile.x - self.x, tile.y - round(self.y))

        p_point = ball_mask.overlap(paddle_mask, paddle_offset)
        t_point = ball_mask.overlap(tile_mask, tile_offset)

        if p_point:
            return 1
        if t_point:
            return 2

        return False



    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Paddle:
    VEL = 6
    WIDTH = PADDLE_IMG.get_width()
    IMG = PADDLE_IMG

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.VEL

        if keys[pygame.K_RIGHT] and self.x < 1182 - self.WIDTH:
            self.x += self.VEL

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

    def get_mask(self):
            return pygame.mask.from_surface(self.IMG)


class Tile:
    IMGS = TILE_IMGS
    WIDTH = TILE_IMG.get_width()
    HEIGHT = TILE_IMG.get_height()


    def __init__(self, x, y):
        self.x = x
        self.y = x
        self.density = 11
        self.img = self.IMGS[0]

    def draw(self, win):

        if self.density < 10:
            self.img = self.IMGS[0]
        elif self.density < 20:
            self.img = self.IMGS[1]
        elif self.density < 30:
            self.img = self.IMGS[2]
        elif self.density < 40:
            self.img = self.IMGS[3]
        else:
            self.img = self.IMGS[4]


        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
            return pygame.mask.from_surface(self.img)





def draw_window(win, score, ball, round, paddle, tiles):
    win.blit(BG_IMG, (0,0))

    text = STAT_FONT.render("Score: " + str(score), 1,(255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Round: " + str(round), 1,(255,255,255))
    win.blit(text, (10, 10))


    for tile in tiles:
        tile.draw(win)

    paddle.draw(win)
    ball.draw(win)
    pygame.display.update()


def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGTH))
    clock = pygame.time.Clock()
    score = 0
    round = 1
    ball = Ball(900, 100)
    paddle = Paddle(600, 665)
    tiles = [Tile(100, 100)]
    WIDTH = TILE_IMG.get_width()
    HEIGHT = TILE_IMG.get_height()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()




        for tile in tiles:
            if ball.collide(paddle, tile) == 1:
                ball.Y_VEL = ball.Y_VEL * -1
            elif ball.collide(paddle, tile) == 2:
                ball.Y_VEL = ball.Y_VEL * -1
                score += 1

            if len(tiles) < 10:
                for i in range(10):
                    tiles.append(Tile(450 + WIDTH, 100))



        paddle.move()
        ball.move()
        draw_window(win, score, ball, round, paddle, tiles)

main()
