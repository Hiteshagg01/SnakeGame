import pygame
from pygame.math import Vector2
import random

# Game constants

CELL_SIZE = 20
CELL_NUMBER_X = 2 * 9
CELL_NUMBER_Y = 2 * 16

FPS = 60

SNAKE_SPEED = int(1000 / 12)
SNAKE_COLOR = (70, 175, 215)
FRUIT_COLOR = (215, 55, 70)
BACKGROUND_COLOR = (175, 215, 70)
GRASS_COLOR = (167, 209, 61)
FONT_COLOR = (56, 74, 12)


class SNAKE:
    def __init__(self, screen):
        self.screen = screen
        self.body = [Vector2(1, 1), Vector2(2, 1), Vector2(3, 1)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            head_relation = self.body[-1] - self.body[-2]
            tail_relation = self.body[0] - self.body[1]

            if index == len(self.body) - 1:
                if head_relation == Vector2(1, 0):
                    self.screen.blit(self.head_right, block_rect)

                if head_relation == Vector2(-1, 0):
                    self.screen.blit(self.head_left, block_rect)

                if head_relation == Vector2(0, 1):
                    self.screen.blit(self.head_down, block_rect)

                if head_relation == Vector2(0, -1):
                    self.screen.blit(self.head_up, block_rect)

            elif index == 0:
                if tail_relation == Vector2(1, 0):
                    self.screen.blit(self.tail_right, block_rect)

                if tail_relation == Vector2(-1, 0):
                    self.screen.blit(self.tail_left, block_rect)

                if tail_relation == Vector2(0, 1):
                    self.screen.blit(self.tail_down, block_rect)

                if tail_relation == Vector2(0, -1):
                    self.screen.blit(self.tail_up, block_rect)

            else:
                prev_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block

                if prev_block.x == next_block.x:
                    self.screen.blit(self.body_vertical, block_rect)

                elif prev_block.y == next_block.y:
                    self.screen.blit(self.body_horizontal, block_rect)

                else:
                    if (prev_block.x == -1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == -1):
                        self.screen.blit(self.body_bl, block_rect)

                    elif (prev_block.y == 1 and next_block.x == 1) or (prev_block.x == 1 and next_block.y == 1):
                        self.screen.blit(self.body_br, block_rect)

                    elif (prev_block.y == -1 and next_block.x == -1) or (prev_block.x == -1 and next_block.y == -1):
                        self.screen.blit(self.body_tl, block_rect)

                    elif (prev_block.x == 1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == 1):
                        self.screen.blit(self.body_tr, block_rect)

    def move_snake(self):
        if self.direction != Vector2(0, 0):
            if self.new_block:
                temp_body = self.body[:]
                temp_body.append(temp_body[-1] + self.direction)
                self.body = temp_body[:]
                self.new_block = False
            else:
                temp_body = self.body[1:]
                temp_body.append(temp_body[-1] + self.direction)
                self.body = temp_body[:]

    def turn_left(self):
        if self.direction != Vector2(1, 0):
            self.direction = Vector2(-1, 0)

    def turn_right(self):
        if self.direction != Vector2(-1, 0):
            self.direction = Vector2(1, 0)

    def turn_up(self):
        if self.direction != Vector2(0, 1):
            self.direction = Vector2(0, -1)

    def turn_down(self):
        if self.direction != Vector2(0, -1):
            self.direction = Vector2(0, 1)


class FRUIT:
    def __init__(self, screen):
        self.screen = screen
        self.pos = Vector2(-1, -1)
        self.respawn_fruit()

        self.apple = pygame.image.load('graphics/re_back_apple.png').convert_alpha()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.screen.blit(self.apple, fruit_rect)

    def respawn_fruit(self):
        self.pos = Vector2(random.randint(0, CELL_NUMBER_X - 1), random.randint(0, CELL_NUMBER_Y - 1))


class GAME:
    def __init__(self):
        self.playing = True
        self.pause = False
        self.fail = False

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER_X, CELL_SIZE * CELL_NUMBER_Y))
        pygame.display.set_caption("Snake Game")

        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, SNAKE_SPEED)

        self.snake = SNAKE(self.screen)
        self.fruit = FRUIT(self.screen)

    def set_background(self):
        self.screen.fill(BACKGROUND_COLOR)

        for row in range(CELL_NUMBER_Y):
            if row % 2 == 0:
                for col in range(CELL_NUMBER_X):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, GRASS_COLOR, grass_rect)
            else:
                for col in range(CELL_NUMBER_X):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, GRASS_COLOR, grass_rect)

    def display_score(self):
        score_font = pygame.font.Font("font/PoetsenOne-Regular.ttf", 14)
        score = str(len(self.snake.body) - 3)
        score_surf = score_font.render(score, True, FONT_COLOR)

        score_x = CELL_NUMBER_X * CELL_SIZE - 25
        score_y = 25

        score_rect = score_surf.get_rect(center=(score_x, score_y))
        apple_rect = self.fruit.apple.get_rect(midright=(score_rect.left, score_rect.centery))

        frame_w = apple_rect.width + score_rect.width + 6
        frame_h = apple_rect.height + 6
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top - 3, frame_w, frame_h)

        pygame.draw.rect(self.screen, BACKGROUND_COLOR, bg_rect)
        pygame.draw.rect(self.screen, FONT_COLOR, bg_rect, 2)
        self.screen.blit(score_surf, score_rect)
        self.screen.blit(self.fruit.apple, apple_rect)

    def game_over(self):
        game_over_font = pygame.font.Font("font/PoetsenOne-Regular.ttf", 40)
        game_over_surf = game_over_font.render('GAME OVER !!', True, (255, 60, 60))

        game_over_x = (CELL_NUMBER_X * CELL_SIZE / 2)
        game_over_y = (CELL_NUMBER_Y * CELL_SIZE / 2)

        game_over_rect = game_over_surf.get_rect(center=(game_over_x, game_over_y))

        frame_w = game_over_rect.width + 20
        frame_h = game_over_rect.height + 10
        frame = pygame.Rect(game_over_rect.left - 10, game_over_rect.top - 5, frame_w, frame_h)

        pygame.draw.rect(self.screen, FONT_COLOR, frame, 2)
        self.screen.blit(game_over_surf, game_over_rect)

    def game_pause(self):
        pause_font = pygame.font.Font("font/PoetsenOne-Regular.ttf", 40)
        pause_surf = pause_font.render('Paused', True, FONT_COLOR)

        pause_x = (CELL_NUMBER_X * CELL_SIZE / 2)
        pause_y = (CELL_NUMBER_Y * CELL_SIZE / 2)

        pause_rect = pause_surf.get_rect(center=(pause_x, pause_y))

        frame_w = pause_rect.width + 20
        frame_h = pause_rect.height + 10
        frame = pygame.Rect(pause_rect.left - 10, pause_rect.top - 5, frame_w, frame_h)

        pygame.draw.rect(self.screen, FONT_COLOR, frame, 2)
        self.screen.blit(pause_surf, pause_rect)

    def check_fruit_collision(self):
        if self.fruit.pos == self.snake.body[-1]:
            self.fruit.respawn_fruit()
            self.snake.new_block = True

            # Make sure fruit does not spawn on snake itself
            for block in self.snake.body[:-1]:
                if block == self.fruit.pos:
                    self.fruit.respawn_fruit()

    def check_wall_collision(self):
        if not (0 <= self.snake.body[-1].x < CELL_NUMBER_X and 0 <= self.snake.body[-1].y < CELL_NUMBER_Y):
            self.fail = True

    def check_self_collision(self):
        for block in self.snake.body[:-1]:
            if block == self.snake.body[-1]:
                self.fail = True

    def play(self):
        self.set_background()
        self.display_score()
        self.snake.draw_snake()
        self.fruit.draw_fruit()

        # Make sure fruit does not spawn on snake itself
        for block in self.snake.body[:-1]:
            if block == self.fruit.pos:
                self.fruit.respawn_fruit()

        if self.pause:
            self.game_pause()

        if self.fail:
            self.game_over()

        pygame.display.update()
        self.clock.tick(FPS)

    def start_game(self):
        while self.playing:

            self.play()

            for event in pygame.event.get():
                if event.type == self.SCREEN_UPDATE:
                    if not (self.pause or self.fail):
                        self.snake.move_snake()
                        self.check_fruit_collision()
                        self.check_wall_collision()
                        self.check_self_collision()

                if event.type == pygame.QUIT:
                    self.playing = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.pause = not self.pause

                    if event.key == pygame.K_SPACE:
                        if self.fail:
                            self.fail = False
                            self.snake.body = [Vector2(1, 1), Vector2(2, 1), Vector2(3, 1)]
                            self.snake.direction = Vector2(0, 0)

                    if not self.pause:
                        if event.key == pygame.K_w:
                            self.snake.turn_up()

                        elif event.key == pygame.K_a:
                            self.snake.turn_left()

                        elif event.key == pygame.K_s:
                            self.snake.turn_down()

                        elif event.key == pygame.K_d:
                            self.snake.turn_right()


if __name__ == "__main__":
    game = GAME()
    game.start_game()
