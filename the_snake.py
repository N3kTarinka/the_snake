from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
POSITION_GAME = (0, 0)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pygame.time.Clock()

# Заголовок окна:
pygame.display.set_caption('Игра Змейка')


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=POSITION_GAME, body_color=APPLE_COLOR):
        """Создание объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта."""
        pygame.draw.rect(surface, self.body_color, pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE))


class Apple(GameObject):
    """Класс для объекта яблока."""

    def __init__(self, body_color=APPLE_COLOR, snake_positions=POSITION_GAME):
        super().__init__(body_color)
        self.randomize_position(snake_positions)

    def randomize_position(self, occupied_positions):
        available_positions = [(x, y) for x in range
                               (GRID_WIDTH) for y in range(GRID_HEIGHT)
                               if (x, y) not in occupied_positions]
        if available_positions:
            self.position = choice(available_positions)


class Snake(GameObject):
    """Класс для объекта змеи."""

    def __init__(self):
        # Инициализация цвета тела змеи и сброс параметров
        self.body_color = SNAKE_COLOR
        self.reset()

    def draw(self, surface):
        # Отрисовка змеи на поверхности
        block_size = GRID_SIZE
        for pos in self.positions:
            pygame.draw.rect(surface, self.body_color, pygame.Rect(
                pos[0] * block_size, pos[1] * block_size,
                block_size, block_size))

    def get_head_position(self):
        # Получение позиции головы змеи
        return self.positions[0]

    def move(self, grow=False):
        # Движение змеи
        head_x, head_y = self.get_head_position()
        new_head = ((head_x + self.direction[0]) % GRID_WIDTH,
                    (head_y + self.direction[1]) % GRID_HEIGHT)

        self.positions.insert(0, new_head)

        if not grow:
            self.positions.pop()

    def reset(self):
        # Сброс параметров змеи
        self.position = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [self.position]

    def update_direction(self, new_direction):
        # Обновление направления движения змеи
        self.direction = new_direction


def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов Snake и Apple:
    snake = Snake()
    apple = Apple(APPLE_COLOR, snake.positions)

    while True:
        clock.tick(SPEED)  # Ограничение скорости игры
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана

        # Отрисовка змеи и яблока на экране
        snake.draw(screen)
        apple.draw(screen)

        # Обработка нажатий клавиш
        handle_keys(snake)

        # Проверка столкновения змеи с яблоком
        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.move(grow=True)
        else:
            snake.move()

        # Проверка столкновения змеи с самой собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        # Обновление экрана
        pygame.display.update()


if __name__ == "__main__":
    main()
