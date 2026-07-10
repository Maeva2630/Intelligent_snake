"""Rect class to encapsulate the concept og pygame rects"""
class Rect:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

    def collidepoint(self, x: int, y: int) -> bool:
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
