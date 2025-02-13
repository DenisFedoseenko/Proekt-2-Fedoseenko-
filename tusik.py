import pygame
import sys
import random
import logging

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 30
BRICK_COLOR = (9, 62, 94)
WHITE = (255, 255, 255)
FPS = 60
LEVELS = 3
BRICKS_PER_LEVEL = 10
BLUE = (9, 62, 94)
ORANGE = (255, 167, 86)
GREEN = (189, 236, 182)

# Загрузка изображений фона
start_background = pygame.image.load('start.png')
setting_background = pygame.image.load('setting.png')
level_one_background = pygame.image.load('one.png')
level_two_background = pygame.image.load('two.png')
level_three_background = pygame.image.load('three.png')
end_background = pygame.image.load('start2.png')  # Можно использовать тот же фон

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Мир столкновений")

# Установка начальной громкости
bg_volume = 0.5
sfx_volume = 0.5
pygame.mixer.music.set_volume(bg_volume)


# Функция для загрузки и воспроизведения музыки
def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)


# Функция для воспроизведения звуковых эффектов
def play_sound_effect(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.set_volume(sfx_volume)
    sound.play()


# Функция начальной заставки
def show_start_screen():
    play_music("x.mp3")  # Заставка
    font = pygame.font.Font(None, 74)
    text = font.render("Мир столкновений", True, ORANGE)
    start_button = font.render("Нажмите 'Пробел', чтобы начать", True, ORANGE)
    settings_button = font.render("Нажмите 'Tab', чтобы настройки", True, ORANGE)

    # Отображение фона
    screen.blit(start_background, (0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(start_button, (SCREEN_WIDTH // 2 - start_button.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(settings_button, (SCREEN_WIDTH // 2 - settings_button.get_width() // 2, SCREEN_HEIGHT // 2 + 70))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_TAB:  # Вход в меню настроек
                    settings_screen()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Функция экрана окончания игры
def show_end_screen(score):
    pygame.mixer.music.load("z.mp3")  # Конечный экран
    pygame.mixer.music.play(-1)

    font = pygame.font.Font(None, 74)
    text = font.render(f"Игра окончена! Счет: {score}", True, BLUE)
    restart_button = font.render("Играть снова - 'Пробел'", True, BLUE)
    exit_button = font.render("Выйти из игры - 'ESC'", True, BLUE)

    # Отображение фона
    screen.blit(end_background, (10, 10))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_button, (SCREEN_WIDTH // 2 - restart_button.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(exit_button, (SCREEN_WIDTH // 2 - exit_button.get_width() // 2, SCREEN_HEIGHT // 2 + 70))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:  # Выход из игры
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Функция для генерации кирпичей без наложений и касаний
def reset_bricks():
    bricks = []
    while len(bricks) < BRICKS_PER_LEVEL:
        brick_x = random.randint(0, SCREEN_WIDTH - BRICK_WIDTH)
        brick_y = random.randint(50, 200)
        new_brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)

        # Проверка на наложение и касание других кирпичей
        if not any(new_brick.colliderect(brick) for brick in bricks) and \
                not any(abs(brick.y - new_brick.y) < BRICK_HEIGHT and
                        (new_brick.x < brick.x + BRICK_WIDTH and new_brick.x + BRICK_WIDTH > brick.x) for brick in
                        bricks):
            bricks.append(new_brick)
    return bricks


# Функция для настроек
def settings_screen():
    global bg_volume, sfx_volume
    waiting = True
    font = pygame.font.Font(None, 48)

    while waiting:
        screen.fill(WHITE)
        title = font.render("Настройки громкости", True, GREEN)
        bg_label = font.render("Громкость музыки:", True, GREEN)
        sfx_label = font.render("Громкость эффектов:", True, GREEN)
        exit_button = font.render("Нажмите 'Shift', чтобы играть", True, GREEN)

        screen.blit(setting_background, (0, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        screen.blit(bg_label, (50, 150))
        screen.blit(sfx_label, (50, 250))
        screen.blit(exit_button, (50, 350))

        # Ползунки громкости
        pygame.draw.rect(screen, BLUE, (50, 200, 300, 20))
        pygame.draw.rect(screen, BLUE, (50, 300, 300, 20))
        pygame.draw.rect(screen, (255, 255, 255), (50 + int(bg_volume * 300), 200, 10, 20))  # Музыка
        pygame.draw.rect(screen, (255, 255, 255), (50 + int(sfx_volume * 300), 300, 10, 20))  # Эффекты

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # Выход из настроек по Shift
                    waiting = False  # Закрываем настройки и начинаем игру
                if event.key == pygame.K_UP:
                    bg_volume = min(bg_volume + 0.1, 1.0)
                    pygame.mixer.music.set_volume(bg_volume)
                if event.key == pygame.K_DOWN:
                    bg_volume = max(bg_volume - 0.1, 0.0)
                    pygame.mixer.music.set_volume(bg_volume)
                if event.key == pygame.K_RIGHT:
                    sfx_volume = min(sfx_volume + 0.1, 1.0)
                if event.key == pygame.K_LEFT:
                    sfx_volume = max(sfx_volume - 0.1, 0.0)

    game_loop()  # Начинаем игру с новыми настройками после выхода из меню


# Игровая логика с уровнями
def game_loop():
    pygame.mixer.music.load("u.mp3")
    pygame.mixer.music.play(-1)
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - 50
    ball_x = SCREEN_WIDTH // 2
    ball_y = paddle_y - BALL_RADIUS
    ball_vel_x = 4
    ball_vel_y = -4
    score = 0
    level = 1
    total_bricks = reset_bricks()

    while True:
        # Устанавливаем фон в зависимости от уровня
        if level == 1:
            screen.blit(level_one_background, (0, 0))
        elif level == 2:
            screen.blit(level_two_background, (0, 0))
        elif level == 3:
            screen.blit(level_three_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 10
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
            paddle_x += 10

        # Движение мяча
        ball_x += ball_vel_x
        ball_y += ball_vel_y

        # Отражение мяча от стен
        if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            ball_vel_x = -ball_vel_x
        if ball_y <= BALL_RADIUS:
            ball_vel_y = -ball_vel_y
        if ball_y >= SCREEN_HEIGHT:  # Если мяч упал
            play_sound_effect("cv.mp3")  # Проигрыш
            pygame.mixer.music.stop()  # Остановка музыки перед выходом на экран окончания
            show_end_screen(score)
            return

        # Проверка на столкновение с платформой
        if paddle_y <= ball_y + BALL_RADIUS <= paddle_y + PADDLE_HEIGHT:
            if paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH:
                ball_vel_y = -ball_vel_y
                score += 1  # Начальный бонус за касание платформы

        # Проверка на столкновение с кирпичами
        for brick in total_bricks[:]:
            if brick.collidepoint(ball_x, ball_y):
                ball_vel_y = -ball_vel_y
                total_bricks.remove(brick)
                score += 5  # Бонус за касание кирпича
                play_sound_effect('pm.mp3')  # Звук разбивания кирпича
                if not total_bricks:  # Если уровень пройден
                    level += 1
                    if level > LEVELS:
                        pygame.mixer.music.stop()  # Остановка музыки перед выходом на экран окончания
                        show_end_screen(score)
                        return
                    total_bricks = reset_bricks()
                break

        # Рисование объектов
        pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
        for brick in total_bricks:
            pygame.draw.rect(screen, BRICK_COLOR, brick)

        # Отображение счета и уровня
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {score}", True, WHITE)
        level_text = font.render(f"Уровень: {level}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50))
        screen.blit(level_text, (20, SCREEN_HEIGHT - 50))  # Позиция для отображения уровня

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


logging.basicConfig(filename='errors.log', level=logging.ERROR)


def log_excepthook(type, value, traceback):
    logging.error("Необработанное исключение:", exc_info=(type, value, traceback))


sys.excepthook = log_excepthook


# Главный цикл
def main():
    while True:
        show_start_screen()
        game_loop()


if __name__ == "__main__":
    main()
