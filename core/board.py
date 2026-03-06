import pygame
from core.settings import *
from utils.colors import *

class Board:
    def __init__(self):
        # Encapsulation: Use private variable for the grid
        # 0 means empty, other values can represent colors or block types
        self.__grid = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE)

    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, DARK_GRAY, self.rect)
        
        # Draw grid lines and blocks
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                x = BOARD_X + col * CELL_SIZE
                y = BOARD_Y + row * CELL_SIZE
                
                # Draw the block if it exists (not 0)
                if self.__grid[row][col] != 0:
                    # Retrieve color from grid or use WHITE as fallback
                    color = self.__grid[row][col] if isinstance(self.__grid[row][col], tuple) else WHITE
                    block_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, color, block_rect)
                    # Optional: draw an inner border to make blocks look better
                    pygame.draw.rect(screen, BLACK, block_rect, 1)
                
                # Draw faint grid lines
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRAY, cell_rect, 1)

    # Encapsulation methods (Getters/Setters)
    def get_grid(self):
        return self.__grid
        
    def get_cell(self, row, col):
        if 0 <= row < BOARD_HEIGHT and 0 <= col < BOARD_WIDTH:
            return self.__grid[row][col]
        return None
        
    def set_cell(self, row, col, value):
        if 0 <= row < BOARD_HEIGHT and 0 <= col < BOARD_WIDTH:
            self.__grid[row][col] = value
            return True
        return False
        
    def clear_full_rows(self):
        """
        Checks for any full rows, clears them, and shifts blocks above down.
        Returns the number of rows cleared (for scoring).
        """
        # Create a new blank grid
        new_grid = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        new_row_idx = BOARD_HEIGHT - 1
        lines_cleared = 0
        
        # Iterate from bottom to top
        for row in range(BOARD_HEIGHT - 1, -1, -1):
            # If the row is NOT full, copy it to the new grid at new_row_idx
            if not all(self.__grid[row][col] != 0 for col in range(BOARD_WIDTH)):
                new_grid[new_row_idx] = self.__grid[row]
                new_row_idx -= 1
            else:
                lines_cleared += 1
                
        self.__grid = new_grid
        return lines_cleared
