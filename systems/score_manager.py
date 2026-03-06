import pygame
from utils.colors import WHITE

class ScoreManager:
    """
    Manages the player's score and handles rendering the score on the screen.
    """
    def __init__(self):
        self._score = 0
        # Typical Tetris scoring multipliers based on number of lines cleared at once
        self.points_per_lines = {
            1: 100,
            2: 300,
            3: 500,
            4: 800  # "Tetris"
        }
        
        # Initialize basic font for drawing
        # Size 36, default system font
        self.font = pygame.font.Font(None, 36)

    def add_score(self, lines_cleared):
        """
        Increases the score based on the number of lines cleared.
        """
        if lines_cleared > 0:
            # If standard scoring isn't found (e.g., > 4), default to 100 * lines
            points = self.points_per_lines.get(lines_cleared, lines_cleared * 100)
            self._score += points

    def get_score(self):
        return self._score

    def draw(self, screen, x, y, level=0):
        """
        Renders the current score and level onto the provided Pygame screen at (x, y).
        """
        score_surface = self.font.render(f"Score: {self._score}", True, WHITE)
        screen.blit(score_surface, (x, y))
        
        level_surface = self.font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_surface, (x, y + 40))
