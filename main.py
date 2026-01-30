import pygame


class Environment:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.image = pygame.image.load("assets/bg.png")
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)


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
        self.collision_group = pygame.sprite.Group()
        self.collision_group.add(self.player)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.movement(keys)

    def draw(self):
        self.environment.draw(self.screen)
        self.collision_group.draw(self.screen)

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
