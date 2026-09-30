import pygame
from .snake import Snake
from .food import Food
from .sound_manager import SoundManager

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
GRAY = (180, 180, 180)
GOLD = (255, 215, 0)
CYAN = (0, 210, 230)
DARK_OVERLAY = (15, 15, 20, 220)

DIFFICULTIES = {
    "Easy": 6,
    "Medium": 10,
    "Hard": 16,
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.difficulty = "Medium"
        self.moves_per_second = DIFFICULTIES[self.difficulty]

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)
        self.sound_manager = SoundManager()

        self.score = 0
        self.high_score = 0
        self.font = pygame.font.SysFont("Arial", 26)
        self.title_font = pygame.font.SysFont("Arial", 44, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial", 17)

        self._frame_counter = 0
        self.game_over = False

    def restart(self, difficulty=None):
        """Restart the game session with optional difficulty selection."""
        if difficulty in DIFFICULTIES:
            self.difficulty = difficulty
            self.moves_per_second = DIFFICULTIES[difficulty]

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food.respawn(self.snake.body)
        self.score = 0
        self._frame_counter = 0
        self.game_over = False

    def handle_keydown(self, key):
        if self.game_over:
            # Replay difficulty selections
            if key in (pygame.K_1, pygame.K_e):
                self.restart("Easy")
            elif key in (pygame.K_2, pygame.K_m):
                self.restart("Medium")
            elif key in (pygame.K_3, pygame.K_h):
                self.restart("Hard")
            elif key in (pygame.K_r, pygame.K_SPACE):
                self.restart(self.difficulty)
            elif key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        # Direction changes are applied immediately on key press.
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        if self.snake.collides_with_wall(self.grid_width, self.grid_height) or self.snake.collides_with_self():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            self.sound_manager.play_game_over()
            return

        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.sound_manager.play_eat()
            self.food.respawn(self.snake.body)

    def render(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        # Draw HUD: Score and Difficulty
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (15, 12))

        diff_text = self.subtitle_font.render(f"Difficulty: {self.difficulty} ({self.moves_per_second}/s)", True, CYAN)
        screen.blit(diff_text, (self.width - diff_text.get_width() - 15, 15))

        # Render Game Over modal with replay options
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill(DARK_OVERLAY)
            screen.blit(overlay, (0, 0))

            box_w, box_h = 460, 310
            box_x = (self.width - box_w) // 2
            box_y = (self.height - box_h) // 2
            pygame.draw.rect(screen, (24, 28, 38), (box_x, box_y, box_w, box_h), border_radius=12)
            pygame.draw.rect(screen, RED, (box_x, box_y, box_w, box_h), width=2, border_radius=12)

            # Title
            title_text = self.title_font.render("GAME OVER", True, RED)
            screen.blit(title_text, title_text.get_rect(center=(self.width // 2, box_y + 40)))

            # Score & Best
            score_line = self.font.render(f"Final Score: {self.score}   |   Best: {self.high_score}", True, WHITE)
            screen.blit(score_line, score_line.get_rect(center=(self.width // 2, box_y + 90)))

            # Difficulty Replay Options
            replay_hdr = self.subtitle_font.render("Select Difficulty to Play Again:", True, GOLD)
            screen.blit(replay_hdr, replay_hdr.get_rect(center=(self.width // 2, box_y + 145)))

            opt_line = self.font.render("[1] Easy    [2] Medium    [3] Hard", True, CYAN)
            screen.blit(opt_line, opt_line.get_rect(center=(self.width // 2, box_y + 185)))

            # Quick replay & exit prompts
            quick_text = self.subtitle_font.render(f"Press [R / Space] to Restart ({self.difficulty})", True, WHITE)
            screen.blit(quick_text, quick_text.get_rect(center=(self.width // 2, box_y + 230)))

            exit_text = self.small_font.render("Press [Q / ESC] to Quit", True, GRAY)
            screen.blit(exit_text, exit_text.get_rect(center=(self.width // 2, box_y + 270)))
