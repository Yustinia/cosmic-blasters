import pygame


class Environment:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.image = pygame.image.load("assets/bg.png")
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, height: int) -> None:
        super().__init__()
        self.height = height
        self.speed = 10

        self.image = pygame.image.load("assets/test.png")
        self.rect = self.image.get_rect()

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, x: int, y: int, speed: int = 7) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed

        self.image = pygame.image.load("assets/player.png")
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
        self.player = Player(self.width, self.height, self.width // 2, self.height - 80)

        # collision group for player & bullet
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.bullets = pygame.sprite.Group()

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

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.movement(keys)
        self.all_sprites.update()

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
    game = Game(500, 600)
    game.run()


if __name__ == "__main__":
    main()
