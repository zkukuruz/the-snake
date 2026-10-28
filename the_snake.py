import sys
from random import choice

import pygame as pg

# Константы игры
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
INITIAL_POSITION = (
    GRID_WIDTH // 2 * GRID_SIZE,
    GRID_HEIGHT // 2 * GRID_SIZE,
)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_BACKGROUND_COLOR = BLACK
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10

TURNS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT),
}

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(
        self, position=INITIAL_POSITION, body_color=None
    ):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color=None):
        """Отрисовывает одну ячейку игрового поля."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(
            screen,
            self.body_color if color is None else color,
            rect,
        )
        if color is None or color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовывает игровой объект."""
        raise NotImplementedError(
            f'Метод draw не переопределён в классе '
            f'{self.__class__.__name__}'
        )


class Apple(GameObject):
    """Класс яблока."""

    def __init__(
        self, body_color=APPLE_COLOR, occupied_positions=None
    ):
        super().__init__(
            position=(0, 0),
            body_color=body_color,
        )
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions=None):
        """Размещает яблоко в случайной свободной клетке."""
        occupied_positions = occupied_positions or []
        free_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE)
            not in occupied_positions
        ]
        if free_positions:
            self.position = choice(free_positions)

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(
        self, position=INITIAL_POSITION, body_color=SNAKE_COLOR
    ):
        super().__init__(position, body_color)
        self.reset()

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну клетку."""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE)
            % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE)
            % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.last = None

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает голову и обновляет хвост змейки."""
        self.draw_cell(self.get_head_position())

        if self.last is not None:
            self.draw_cell(
                self.last, color=BOARD_BACKGROUND_COLOR
            )


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш управления."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        elif event.type == pg.KEYDOWN and event.key in TURNS:
            new_direction, opposite = TURNS[event.key]
            if game_object.direction != opposite:
                game_object.next_direction = new_direction


def main():
    """Запускает основной игровой цикл."""
    pg.init()

    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head = snake.get_head_position()

        if head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif head in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
