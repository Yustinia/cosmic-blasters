import pygame


class Environment:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.image = pygame.image.load("assets/bg.png")
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)


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

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        pass

    def draw(self):
        self.environment.draw(self.screen)

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
