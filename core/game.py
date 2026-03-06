import sys
import pygame
from core.settings import *
from utils.colors import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.key.set_repeat(200, 50)
        
        # Initialize the board
        from core.board import Board
        self.board = Board()
        
        # Initialize score manager
        from systems.score_manager import ScoreManager
        self.score_manager = ScoreManager()
        
        # Initialize piece factory and current piece
        from pieces.factory import PieceFactory
        self.factory = PieceFactory()
        self.current_piece = self._spawn_piece()
        self.next_piece = self._spawn_piece()
        self.hold_piece = None
        self.can_hold = True
        
        # Gravity and Level settings
        self.level = 0
        self.fall_time = 0
        self.fall_speed = 500  # Fall every 500 ms
        
        # Game Over state
        self.game_over = False
        self.font = pygame.font.SysFont('arial', 48, bold=True)

    def _spawn_piece(self):
        start_x = BOARD_WIDTH // 2 - 2
        start_y = 0
        return self.factory.create_random_piece(start_x, start_y)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                elif self.current_piece:
                    if event.key == pygame.K_LEFT:
                        if self._is_valid_move(self.current_piece, dx=-1, dy=0):
                            self.current_piece.move_left()
                    elif event.key == pygame.K_RIGHT:
                        if self._is_valid_move(self.current_piece, dx=1, dy=0):
                            self.current_piece.move_right()
                    elif event.key == pygame.K_DOWN:
                        if self._is_valid_move(self.current_piece, dx=0, dy=1):
                            self.current_piece.move_down()
                            # Reset fall time so it doesn't double-drop immediately
                            self.fall_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_UP:
                        # Rotate clockwise
                        self.current_piece.rotate()
                        # If rotation causes a collision, undo it
                        if not self._is_valid_move(self.current_piece, dx=0, dy=0):
                            self.current_piece.rotate_counter_clockwise()
                    elif event.key == pygame.K_SPACE:
                        # Hard Drop
                        while self._is_valid_move(self.current_piece, dx=0, dy=1):
                            self.current_piece.move_down()
                        self._lock_and_spawn_piece()
                    elif event.key == pygame.K_c:
                        # Hold Piece mechanics
                        if self.can_hold:
                            if self.hold_piece is None:
                                self.hold_piece = self.current_piece
                                self.current_piece = self.next_piece
                                self.next_piece = self._spawn_piece()
                            else:
                                self.hold_piece, self.current_piece = self.current_piece, self.hold_piece
                            
                            # Reset piece back to the top-center
                            self.current_piece._x = BOARD_WIDTH // 2 - 2
                            self.current_piece._y = 0
                            
                            self.can_hold = False
                            self.fall_time = pygame.time.get_ticks()

    def reset_game(self):
        """Reset the game state to start a new game."""
        # Reset the board
        from core.board import Board
        self.board = Board()
        
        # Reset the score manager
        from systems.score_manager import ScoreManager
        self.score_manager = ScoreManager()
        
        # Reset the piece and game state
        self.current_piece = self._spawn_piece()
        self.next_piece = self._spawn_piece()
        self.hold_piece = None
        self.can_hold = True
        self.game_over = False
        self.level = 0
        self.fall_time = pygame.time.get_ticks()
        self.fall_speed = 500

    def update(self):
        if self.game_over:
            return
            
        current_time = pygame.time.get_ticks()
        
        if self.current_piece:
            # Gravity: piece naturally falls down
            if current_time - self.fall_time > self.fall_speed:
                self.fall_time = current_time
                if self._is_valid_move(self.current_piece, dx=0, dy=1):
                    self.current_piece.move_down()
                else:
                    self._lock_and_spawn_piece()

    def _lock_and_spawn_piece(self):
        """Locks current piece, clears rows, updates score/level/speed, and spawns the next piece."""
        self._lock_piece(self.current_piece)
        lines_cleared = self.board.clear_full_rows()
        
        if lines_cleared > 0:
            self.score_manager.add_score(lines_cleared)
            self.level = self.score_manager.get_score() // 500
            self.fall_speed = max(100, 500 - self.level * 50)
            
        self.current_piece = self.next_piece
        self.next_piece = self._spawn_piece()
        self.can_hold = True
        self.fall_time = pygame.time.get_ticks()
        
        if not self._is_valid_move(self.current_piece, dx=0, dy=0):
            self.game_over = True


    def _is_valid_move(self, piece, dx, dy):
        """Check if the piece can be moved by dx, dy without collision."""
        for r, row in enumerate(piece.shape):
            for c, val in enumerate(row):
                if val != 0:
                    new_x = piece.x + c + dx
                    new_y = piece.y + r + dy
                    
                    # Boundary check
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                        return False
                    
                    # Collision check (only check if piece is inside the board on Y axis)
                    if new_y >= 0:
                        if self.board.get_cell(new_y, new_x) != 0:
                            return False
        return True

    def _lock_piece(self, piece):
        """Lock the piece into the board grid."""
        for r, row in enumerate(piece.shape):
            for c, val in enumerate(row):
                if val != 0:
                    y = piece.y + r
                    x = piece.x + c
                    
                    # Only lock blocks that are actually on the board
                    if y >= 0:
                        self.board.set_cell(y, x, piece.color)

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw the game board
        self.board.draw(self.screen)
        
        # Draw the current piece
        if self.current_piece:
            for r, row in enumerate(self.current_piece.shape):
                for c, val in enumerate(row):
                    if val != 0:
                        px = BOARD_X + (self.current_piece.x + c) * CELL_SIZE
                        py = BOARD_Y + (self.current_piece.y + r) * CELL_SIZE
                        block_rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, self.current_piece.color, block_rect)
                        pygame.draw.rect(self.screen, BLACK, block_rect, 1)        
        
        # Draw the next piece preview
        if self.next_piece:
            preview_font = pygame.font.SysFont('arial', 24)
            preview_text = preview_font.render("NEXT:", True, WHITE)
            # Position it to the right of the board
            preview_x = BOARD_X + (BOARD_WIDTH * CELL_SIZE) + 30
            preview_y = BOARD_Y
            self.screen.blit(preview_text, (preview_x, preview_y))
            
            for r, row in enumerate(self.next_piece.shape):
                for c, val in enumerate(row):
                    if val != 0:
                        px = preview_x + c * CELL_SIZE
                        py = preview_y + 40 + r * CELL_SIZE
                        block_rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, self.next_piece.color, block_rect)
                        pygame.draw.rect(self.screen, BLACK, block_rect, 1)        
        
        # Draw the hold piece preview
        hold_font = pygame.font.SysFont('arial', 24)
        hold_text = hold_font.render("HOLD:", True, WHITE)
        # Position it to the left of the board
        hold_x = BOARD_X - 120
        hold_y = BOARD_Y
        self.screen.blit(hold_text, (hold_x, hold_y))
        
        if self.hold_piece:
            for r, row in enumerate(self.hold_piece.shape):
                for c, val in enumerate(row):
                    if val != 0:
                        px = hold_x + c * CELL_SIZE
                        py = hold_y + 40 + r * CELL_SIZE
                        block_rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, self.hold_piece.color, block_rect)
                        pygame.draw.rect(self.screen, BLACK, block_rect, 1)
        
        # Draw the score and level in the top-left corner (with a bit of margin)
        self.score_manager.draw(self.screen, 20, 20, self.level)
        
        if self.game_over:
            text = self.font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            self.screen.blit(text, text_rect)
            
            # Restart instruction
            restart_font = pygame.font.SysFont('arial', 24)
            restart_text = restart_font.render("Press R to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
