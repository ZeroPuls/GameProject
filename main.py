import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Цвета
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Загрузка изображений
player_img = pygame.image.load('images/images1.png')
meteor_img = pygame.image.load('images/imagesmeteor.png')
background = pygame.image.load('images/background.png')


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (40, 40))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed


# Класс астероида
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(meteor_img, (30, 30))
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), -20))
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Класс снаряда
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -5

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# Группы спрайтов
player = Player()
all_sprites = pygame.sprite.Group(player)
meteors = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Основной цикл игры
clock = pygame.time.Clock()
running = True
score = 0
meteor_timer = 0

while running:
    clock.tick(60)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Генерация астероидов
    meteor_timer += 1
    if meteor_timer > 30:
        meteor = Meteor()
        all_sprites.add(meteor)
        meteors.add(meteor)
        meteor_timer = 0

    # Обновление спрайтов
    all_sprites.update()

    # Проверка столкновений
    for bullet in bullets:
        hit_meteors = pygame.sprite.spritecollide(bullet, meteors, True)
        if hit_meteors:
            bullet.kill()
            score += 10

    if pygame.sprite.spritecollide(player, meteors, True):
        player.lives -= 1
        if player.lives == 0:
            running = False

    # Отрисовка
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
