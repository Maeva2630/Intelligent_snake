import pygame

class Game:
    def __init__(self):
        self.tile_size = 20
        self.screen_width = 32
        self.screen_height = 24
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width * self.tile_size, self.screen_height * self.tile_size))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
            self.screen.fill((0,0,0))

            for x in range(self.screen_width):
                for y in range(self.screen_height):
                    pygame.draw.rect(self.screen, (255, 255, 255), (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size), 1)
        
            pygame.display.flip()

            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def _handle_input(self):
        pass

    def _update(self):
        pass

    def _render(self):
        pass

if __name__ == "__main__":
    game = Game()
    game.run()
