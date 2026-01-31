import pygame
import random
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Environment:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.image = pygame.image.load(resource_path("assets/bg.png"))
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, height: int) -> None:
        super().__init__()
        self.height = height
        self.speed = 10

        self.image = pygame.image.load(resource_path("assets/bullet.png"))
        self.rect = self.image.get_rect()

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y -= self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, x: int) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.speed = random.randint(3, 10)
        self.x = x
        self.y = -100

        self.image = pygame.image.load(resource_path("assets/enemy.png"))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, x: int, y: int, speed: int = 5) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed

        self.image = pygame.image.load(resource_path("assets/player.png"))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def movement(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right <= self.width:
            self.rect.x += self.speed


class Game:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        caption = pygame.display.set_caption("Alien Shooter")

        self.clock = pygame.time.Clock()
        self.is_running = True

        # instantiate objects
        self.environment = Environment(self.width, self.height)
        self.player = Player(self.width, self.height, self.width // 2, self.height - 60)

        # collision group for player & bullet
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.MAX_ENEMIES = 2
        for _ in range(self.MAX_ENEMIES):
            enemy = Enemy(self.width, self.height, random.randint(50, self.width - 50))
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # lazer sound
        self.shoot_sfx = pygame.mixer.Sound("sounds/shoot.mp3")
        self.explode = pygame.mixer.Sound("sounds/explosion.mp3")

    def event_handler(self):
        MAX_BULLET = 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(self.bullets) < MAX_BULLET:
                        bullet = Bullet(self.height)
                        bullet.rect.center = self.player.rect.center
                        self.bullets.add(bullet)
                        self.all_sprites.add(bullet)
                        self.shoot_sfx.play()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.movement(keys)
        self.all_sprites.update()

        # bullet and enemy hit
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if hits:
            self.explode.play()

        # kill game player & enemy collision
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.is_running = False

        # respawn new enemy
        while len(self.enemies) < self.MAX_ENEMIES:
            enemy = Enemy(self.width, self.height, random.randint(50, self.width - 50))
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # kill enemy off screen
        for enemy in self.enemies:
            if enemy.rect.top >= self.height:
                enemy.kill()
                self.MAX_ENEMIES += 1

        # kill bullet off screen
        for bullet in self.bullets:
            if bullet.rect.bottom < 0:
                bullet.kill()

    def draw(self):
        self.environment.draw(self.screen)
        self.all_sprites.draw(self.screen)

    def run(self):
        while self.is_running:
            self.event_handler()
            self.update()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()
        pygame.quit()


def main() -> None:
    pygame.init()
    game = Game(500, 600)
    game.run()


if __name__ == "__main__":
    main()
