import pygame
from game.encapsulation.render import Render
from game.encapsulation.event import EventType, Key, Event

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
    def __init__(self, screen_width: int, screen_height: int, tile_size: int = 0, caption: str = None):
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fullscreen = False

        pygame.init()
        if caption:
            pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

    def clear(self):
        """Clear screen by filling it with a black color"""
        self.screen.fill((0, 0, 0))

    def get_width(self) -> int:
        return self.screen_width

    def get_height(self) -> int:
        return self.screen_height

    def resize(self, new_width: int, new_height: int, tile_size: int = None):
        """Resize current window size"""

        if (self.screen_width == new_width
            and self.screen_height == new_height
            and (tile_size is None or self.tile_size == tile_size)):
            return

        self.screen_width = new_width
        self.screen_height = new_height
        
        if tile_size:
            self.tile_size = tile_size

        flags = 0
        if self.fullscreen:
            flags = pygame.FULLSCREEN | pygame.SCALED

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            flags
        )
 
    def toggle_fullscreen(self):
        """Toggle full screen / window"""
        self.fullscreen = not self.fullscreen
        size = (self.screen_width, self.screen_height)
 
        if self.fullscreen:
            try:
                self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED)
            except pygame.error:
                self.fullscreen = False
                pygame.display.quit()
                pygame.display.init()
                self.screen = pygame.display.set_mode(size)
        else:
            self.screen = pygame.display.set_mode(size)

    def update(self):
        """Update the screen"""
        pygame.display.flip()

    def tick(self, fps: int = 60) -> float:
        """Update deltatime in seconds"""
        return self.clock.tick(fps) / 1000.0

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
                if pg_event.button != 1:
                    continue
                mouse_pos = pygame.mouse.get_pos()
                
            events.append(Event(neutral_type, key=neutral_key, mouse_pos=mouse_pos))
            
        return events

    def quit(self):
        """Quit pygame"""
        self.running = False
        pygame.quit()

    def get_mouse_pos(self) -> tuple[int, int]:
        """Return the current mouse position"""
        return pygame.mouse.get_pos()

