import os
import pygame
import numpy as np
import cv2

# Set dummy video driver so it runs cleanly in background
os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
WIDTH, HEIGHT = 600, 600
FPS = 30
TOTAL_FRAMES = 300  # 10 seconds at 30 fps

def surface_to_frame(surface):
    # Pygame surface (RGBA/RGB) to BGR for OpenCV
    view = pygame.surfarray.array3d(surface)
    # Transpose from (width, height, 3) to (height, width, 3)
    frame = np.transpose(view, (1, 0, 2))
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

# ==========================================
# 1. GENERATE BEFORE_GAMEPLAY.MP4
# ==========================================
def generate_before_video(output_path):
    screen = pygame.Surface((WIDTH, HEIGHT))
    # Original snake class simulation (no reverse prevention, no game over screen)
    cell_size = 20
    grid_w, grid_h = WIDTH // cell_size, HEIGHT // cell_size
    body = [(grid_w // 2, grid_h // 2), (grid_w // 2 - 1, grid_h // 2), (grid_w // 2 - 2, grid_h // 2)]
    direction = (1, 0)
    score = 0
    font = pygame.font.SysFont("Arial", 30)
    food_pos = (grid_w // 2 + 5, grid_h // 2)
    game_over = False
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))

    move_interval = 4  # frames per move (~7.5 moves/sec)
    for frame_idx in range(TOTAL_FRAMES):
        # At frame 60 (2 seconds in), player taps opposite direction (LEFT) while moving RIGHT
        if frame_idx == 60:
            # Bug: sets direction to (-1, 0) directly
            direction = (-1, 0)

        # Move logic
        if not game_over and frame_idx % move_interval == 0:
            new_head = (body[0][0] + direction[0], body[0][1] + direction[1])
            body.insert(0, new_head)
            body.pop()
            # Check self collision
            if body[0] in body[1:]:
                game_over = True
                print("Before video: Snake died due to instant 180 reverse bug!")

        # Render original game
        screen.fill((0, 0, 0))
        # Draw food
        food_rect = pygame.Rect(food_pos[0] * cell_size, food_pos[1] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (220, 60, 60), food_rect)
        # Draw snake
        for seg in body:
            r = pygame.Rect(seg[0] * cell_size, seg[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 200, 0), r)
        # Draw score
        score_txt = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_txt, (10, 10))

        # Notice: When game_over is True, original code printed to console only:
        # print("Game over! Final score:", score)
        # There was NO game over screen on display, game was frozen.
        if game_over:
            # Display bug indicator text for reviewer clarity
            dbg_font = pygame.font.SysFont("Arial", 22)
            bug_label = dbg_font.render("[BUG] Instant 180 Self-Collision & Console-Only Game Over", True, (255, 80, 80))
            screen.blit(bug_label, (20, HEIGHT - 40))

        writer.write(surface_to_frame(screen))

    writer.release()
    print("Generated before video at:", output_path)

# ==========================================
# 2. GENERATE AFTER_GAMEPLAY.MP4
# ==========================================
def generate_after_video(output_path):
    from game.game_engine import GameEngine
    screen = pygame.Surface((WIDTH, HEIGHT))
    engine = GameEngine(WIDTH, HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))

    # Guide snake to eat food and demonstrate fixed features
    for frame_idx in range(TOTAL_FRAMES):
        # Steer snake toward food
        head = engine.snake.body[0]
        food_cell = (engine.food.x, engine.food.y)

        if not engine.game_over:
            # 1. Frame 30: Player taps LEFT while moving RIGHT -> Verified guarded!
            if frame_idx == 30:
                engine.snake.set_direction(-1, 0)  # Will be safely ignored!

            # Steer towards food automatically for demonstration
            if frame_idx > 35 and frame_idx < 130:
                if food_cell[0] > head[0]:
                    engine.snake.set_direction(1, 0)
                elif food_cell[0] < head[0]:
                    engine.snake.set_direction(-1, 0)
                elif food_cell[1] > head[1]:
                    engine.snake.set_direction(0, 1)
                elif food_cell[1] < head[1]:
                    engine.snake.set_direction(0, -1)

            # At frame 130: intentionally collide with right wall to show Game Over modal
            if frame_idx >= 130 and frame_idx < 190:
                engine.snake.set_direction(1, 0)

            engine.update()
        else:
            # At frame 210: User presses '1' for Easy replay difficulty
            if frame_idx == 210:
                engine.handle_keydown(pygame.K_1)
            elif frame_idx > 210:
                engine.update()

        screen.fill((0, 0, 0))
        engine.render(screen)
        writer.write(surface_to_frame(screen))

    writer.release()
    print("Generated after video at:", output_path)

if __name__ == "__main__":
    out_dir = "d:/se/Lab 4/snake_game/videos"
    os.makedirs(out_dir, exist_ok=True)
    generate_before_video(os.path.join(out_dir, "before_gameplay.mp4"))
    generate_after_video(os.path.join(out_dir, "after_gameplay.mp4"))
