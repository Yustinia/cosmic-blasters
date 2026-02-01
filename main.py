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

        self.image = pygame.image.load(resource_path("assets/bg.png")).convert()
        self.y = 0
        self.scroll_speed = 1

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, (0, self.y))
        screen.blit(self.image, (0, self.y - self.height))

    def update(self):
        self.y += self.scroll_speed
        if self.y >= self.height:
            self.y = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, height: int) -> None:
        super().__init__()
        self.height = height
        self.speed = 10

        self.image = pygame.image.load(
            resource_path("assets/bullet.png")
        ).convert_alpha()
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

        self.image = pygame.image.load(
            resource_path("assets/enemy.png")
        ).convert_alpha()
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

        self.image = pygame.image.load(
            resource_path("assets/player.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def movement(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right <= self.width:
            self.rect.x += self.speed


class MainMenu:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.x = self.width // 2
        self.y = self.height // 2

        title_font = pygame.font.Font(None, 64)
        sub_font = pygame.font.Font(None, 24)
        WHITE = (255, 255, 255)
        self.title_surf = title_font.render("Cosmic Blasters", True, WHITE)
        self.title_rect = self.title_surf.get_rect(center=(self.x, self.y - 25))
        self.sub_surf = sub_font.render("Press SPACE to start", True, WHITE)
        self.sub_rect = self.sub_surf.get_rect(center=(self.x, self.y + 25))

        self.player = Player(self.width, self.height, self.width // 2, self.height - 60)
        self.speed = 5
        self.vd = -1

        self.sub_flicker = 0

    def draw(self, screen):
        self.sub_flicker += 1
        screen.blit(self.title_surf, self.title_rect)

        if (self.sub_flicker // 30) % 2 == 0:
            screen.blit(self.sub_surf, self.sub_rect)
        self.player.draw(screen)

    def update(self):
        self.player.rect.x += self.speed
        if self.player.rect.right >= self.width or self.player.rect.left <= 0:
            self.speed *= self.vd


class PlayingGame:
    def __init__(self, width: int, height: int, screen) -> None:
        self.width = width
        self.height = height
        self.screen = screen

        # instantiate objects
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
        self.shoot_sfx = pygame.mixer.Sound(resource_path("sounds/shoot.mp3"))
        self.explode = pygame.mixer.Sound(resource_path("sounds/explosion.mp3"))

    def event_handler(self, events):
        MAX_BULLET = 5

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if len(self.bullets) < MAX_BULLET:
                    bullet = Bullet(self.height)
                    bullet.rect.center = self.player.rect.center
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)
                    self.shoot_sfx.play()

    def update(self, keys) -> str | None:
        self.player.movement(keys)
        self.all_sprites.update()

        # bullet and enemy hit
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if hits:
            self.explode.play()

        # kill game player & enemy collision
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            status = "LOSE"
            return status

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
        self.all_sprites.draw(self.screen)


class GameManager:
    def __init__(self, width: int, height: int, state: str = "MAINMENU") -> None:
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        caption = pygame.display.set_caption("Cosmic Blasters")

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.state = "MAINMENU"  # MAINMENU, PLAYING

        self.environment = Environment(self.width, self.height)
        self.mainmenu = MainMenu(self.width, self.height)

    def draw(self):
        self.environment.draw(self.screen)
        match self.state:
            case "MAINMENU":
                self.mainmenu.draw(self.screen)
            case "PLAYING":
                self.playing.draw()

    def update(self):
        self.environment.update()
        match self.state:
            case "MAINMENU":
                self.mainmenu.update()
            case "PLAYING":
                keys = pygame.key.get_pressed()
                status = self.playing.update(keys)

                if status == "LOSE":
                    self.state = "MAINMENU"

    def event_handler(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.state == "MAINMENU":
                    self._start_game()

        match self.state:
            case "MAINMENU":
                pass
            case "PLAYING":
                self.playing.event_handler(events)

    def _start_game(self):
        self.playing = PlayingGame(self.width, self.height, self.screen)
        self.state = "PLAYING"

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
    pygame.mixer.music.load(resource_path("sounds/OST.mp3"))
    pygame.mixer.music.play(loops=-1)
    manager = GameManager(500, 600)
    manager.run()


if __name__ == "__main__":
    main()
