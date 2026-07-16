""" Render screen"""
from game.encapsulation.render import Render

class Screen:
    def __init__(self, render: Render, game: "Game"):
        self.render = render
        self.game = game

    def _render_end_screen(self):
        grid_center_x = (self.game.grid.width * self.game.tile_size) // 2
        grid_center_y = (self.game.grid.height * self.game.tile_size) // 2
        self.render.draw_dim_overlay((0, 0, 0), alpha=150)
        
        if self.game.winner is not None:
            self.render.draw_text("VICTORY", grid_center_x, grid_center_y - 30, 60, self.game.winner.color, align="center")
            self.render.draw_text(f"AI {self.game.winner.id} Wins!", grid_center_x, grid_center_y + 20, 24, self.game.winner.color, align="center")
        else:
            self.render.draw_text("GAME OVER", grid_center_x, grid_center_y - 30, 60, (230, 50, 50), align="center")
            self.render.draw_text("No Winner", grid_center_x, grid_center_y + 20, 24, (255, 255, 255), align="center")
        
        self.render.draw_text("Press ESC or click 'Back to menu'", grid_center_x, grid_center_y + 60, 20, (180, 180, 180), align="center")
