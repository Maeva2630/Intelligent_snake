import pygame
from game.encaspulation.render import Render
from game.encaspulation.event import EventType, Key, Event

EVENT_MAP = {
    pygame.QUIT: EventType.QUIT,
    pygame.KEYDOWN: EventType.KEY_DOWN,
    pygame.MOUSEBUTTONDOWN: EventType.MOUSE_CLICK
}

KEY_MAP = {
    pygame.K_ESCAPE: Key.ESCAPE,
    pygame.K_SPACE: Key.SPACE,
    pygame.K_UP: Key.UP,
    pygame.K_DOWN: Key.DOWN,
    pygame.K_LEFT: Key.LEFT,
    pygame.K_RIGHT: Key.RIGHT
}

class Window:
    def __init__(self, screen_width: int, screen_height: int, tile_size: int):
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

    def clear(self):
        """Clear screen by filling it with a black color"""
        self.screen.fill((0, 0, 0))

    def update(self):
        """Update the screen"""
        pygame.display.flip()


    def tick(self, fps: int = 60) -> float:
        """Update deltatime in seconds"""
        return self.clock.tick(fps) / 1000.0


    def get_events(self) -> list:
        """Return pygame events"""
        return pygame.event.get()

    def get_events(self) -> list[Event]:
        events = []
        
        for pg_event in pygame.event.get():
            if pg_event.type not in EVENT_MAP:
                continue
                
            neutral_type = EVENT_MAP[pg_event.type]
            neutral_key = None
            mouse_pos = None
            
            if pg_event.type == pygame.KEYDOWN:
                neutral_key = KEY_MAP.get(pg_event.key)
                if neutral_key is None:
                    continue
                    
            elif pg_event.type == pygame.MOUSEBUTTONDOWN:
                if pg_event.button != pygame.event.button.LEFT:
                    continue
                mouse_pos = pygame.mouse.get_pos()
                
            events.append(Event(neutral_type, key=neutral_key, mouse_pos=mouse_pos))
            
        return events

    def quit(self):
        """Quit pygame"""
        self.running = False
        pygame.quit()
