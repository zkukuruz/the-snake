import pygame
from random import choice, randint


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32
)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=(0, 0), body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает игровой объект."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Создаёт яблоко и задаёт его начальные параметры."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Размещает яблоко в случайной клетке поля."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(
            self.position, (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Создаёт змейку с начальными параметрами."""
        super().__init__()
        self.positions = [
            (
                GRID_WIDTH // 2 * GRID_SIZE,
                GRID_HEIGHT // 2 * GRID_SIZE
            )
        ]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.length = 1

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну клетку."""
        head = self.get_head_position()
        new_head = (
            (
                head[0] + self.direction[0] * GRID_SIZE
            ) % SCREEN_WIDTH,
            (
                head[1] + self.direction[1] * GRID_SIZE
            ) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.positions = [
            (
                GRID_WIDTH // 2 * GRID_SIZE,
                GRID_HEIGHT // 2 * GRID_SIZE
            )
        ]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает тело и голову змейки."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                position, (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки:
        head_rect = pygame.Rect(
            self.positions[0], (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента:
        if self.last:
            last_rect = pygame.Rect(
                self.last, (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                screen, BOARD_BACKGROUND_COLOR, last_rect
            )


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш управления."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                and game_object.direction != DOWN
            ):
                game_object.next_direction = UP
            elif (
                event.key == pygame.K_DOWN
                and game_object.direction != UP
            ):
                game_object.next_direction = DOWN
            elif (
                event.key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                event.key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pygame.init()

    # Создание объектов игры:
    snake = Snake()
    apple = Apple()

    # Устанавливаем цвет змейки:
    snake.body_color = SNAKE_COLOR

    # Основной игровой цикл:
    while True:
        clock.tick(SPEED)

        # Обрабатываем нажатия клавиш:
        handle_keys(snake)

        # Обновляем направление змейки:
        snake.update_direction()

        # Двигаем змейку:
        snake.move()

        # Если змейка съела яблоко:
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверяем столкновение с собственным телом:
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Заливаем экран цветом фона:
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Рисуем яблоко и змейку:
        apple.draw()
        snake.draw()

        # Обновляем экран:
        pygame.display.update()


if __name__ == '__main__':
    main()
