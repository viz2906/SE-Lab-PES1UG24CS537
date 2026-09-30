# Lab 4: Vibe Coding — Prompt History & Development Log

**Student Name:** Vishnu Anand M  
**SRN / USN:** PES1UG24CS537  
**Assigned Repository:** [SETAPESU26/45_snake](https://github.com/SETAPESU26/45_snake)  
**Personal Repository:** [viz2906/SE-Lab-PES1UG24CS537](https://github.com/viz2906/SE-Lab-PES1UG24CS537)  
**Assignment Duration:** 60 minutes  
**AI Assistant (Vibe Coding Tool):** Gemini / Claude Pair Programmer  

---

## Overview

The objective of this lab is to use AI-assisted ("Vibe Coding") pair programming to diagnose, repair, and extend a partially working Pygame Snake implementation. Each feature must be designed, refined, and delivered iteratively within three to four prompting attempts, accompanied by separate Git commits and gameplay video demonstrations.

---

## Task 1: Refine Collision Detection

### Problem Analysis
- In `game/snake.py`, `set_direction(dx, dy)` directly replaced `self.direction` without checking whether `(dx, dy)` was the exact opposite of the current movement vector (`-cur_dx, -cur_dy`).
- If the snake was moving Right and the player tapped Left, the head immediately collided with `body[1]`, resulting in an instant, unfair death.
- Additionally, if a player tapped two keys quickly before the next movement tick (e.g., UP then LEFT while moving RIGHT), the snake could step backwards into itself.

### Vibe Coding Prompt (Attempt 1 of 4)
> *"I am working on the Pygame Snake starter in `game/snake.py`. Right now, tapping the opposite direction key (e.g. Left while moving Right) causes instant self-collision because the snake reverses straight into its neck segment. Also, rapid consecutive key presses within a single frame can cause unfair reversals. Please refine collision detection and direction handling so that 180-degree reversals are safely ignored when the snake has length > 1, and buffer the direction updates so moves remain fair and responsive."*

### AI Response & Solution Implemented
1. Added `self.next_direction` and `self.last_move_direction` in `Snake.__init__`.
2. Updated `set_direction(dx, dy)` to validate against `self.last_move_direction`:
   ```python
   cur_dx, cur_dy = self.last_move_direction
   if len(self.body) > 1 and (dx == -cur_dx and dy == -cur_dy):
       return False
   if (dx, dy) == (cur_dx, cur_dy):
       return False
   self.next_direction = (dx, dy)
   self.direction = (dx, dy)
   return True
   ```
3. In `move()`, synced `self.direction = self.next_direction` and recorded `self.last_move_direction = self.direction`.
4. Verified that wall and self collision checks execute cleanly on every grid advance.

### Outcome & Verification
- Unit test verified that pressing `(-1, 0)` while moving `(1, 0)` returns `False` and leaves the snake trajectory intact.
- **Git Commit:** `5c648c6 Task 1: Refine collision detection and prevent instant 180-degree self-collision`

---

## Task 2: Implement Game Over Condition

### Problem Analysis
- The starter code simply printed `"Game over! Final score: X"` to the standard console and halted game updates, leaving the display frozen without any graphical feedback or restart mechanism.

### Vibe Coding Prompt (Attempt 1 of 4)
> *"In `game/game_engine.py`, the game over condition only logs the score to the terminal. Please implement an in-game Game Over screen that renders a semi-transparent dark backdrop overlay, displays 'GAME OVER' prominently in bold red text, shows the player's final score and session high score, and gracefully waits for player input instead of abruptly exiting."*

### AI Response & Solution Implemented
1. Added session high score tracking (`self.high_score = 0`) updated whenever the score increases or the game terminates.
2. Initialized styled typography (`title_font`, `font`, `subtitle_font`).
3. In `render()`, created an alpha-blended surface overlay (`DARK_OVERLAY = (15, 15, 20, 220)`) and centered modal dialog card.
4. Rendered title `"GAME OVER"`, `"Final Score: {score}"`, `"Best Score: {high_score}"`, and quit prompt.
5. In `handle_keydown()`, captured `Q` and `ESCAPE` keys to exit gracefully without crashing.

### Outcome & Verification
- Visual render confirmed centered alignment, clear contrast, and stable framerate.
- **Git Commit:** `e46a728 Task 2: Implement Game Over screen with score display and input wait`

---

## Task 3: Add Replay Option with Difficulty Selection

### Problem Analysis
- Once the game ended, players had no option to restart without relaunching the entire Python process.
- The game lacked speed / difficulty customization.

### Vibe Coding Prompt (Attempt 1 of 4)
> *"Extend the Game Over screen in `game/game_engine.py` to support full replay capabilities with three distinct difficulty levels: Easy (6 moves/s), Medium (10 moves/s), and Hard (16 moves/s). Allow the player to restart by pressing keys 1, 2, or 3, or restart with the current difficulty by pressing R / Space. Add a reset method that re-centers the snake, respawns food, and resets game states cleanly."*

### AI Response & Solution Implemented
1. Defined difficulty presets dictionary:
   ```python
   DIFFICULTIES = {
       "Easy": 6,
       "Medium": 10,
       "Hard": 16,
   }
   ```
2. Added `restart(self, difficulty=None)` to reset snake, food, score, frame counters, and apply the chosen speed.
3. Updated `handle_keydown()` during `self.game_over`:
   - `[1] / [E]`: Easy speed
   - `[2] / [M]`: Medium speed
   - `[3] / [H]`: Hard speed
   - `[R] / [SPACE]`: Restart current difficulty
   - `[Q] / [ESC]`: Exit
4. Added active difficulty HUD indicator in the top-right corner during gameplay.

### Outcome & Verification
- Tested state resetting and speed adjustments across all three presets.
- **Git Commit:** `9e239b3 Task 3: Add replay option with difficulty selection (Easy, Medium, Hard)`

---

## Task 4: Add Sound Feedback

### Problem Analysis
- The starter game had no audio feedback.
- To prevent external file dependency errors and ensure portability across all evaluation machines, audio assets should be self-contained and loaded safely with graceful fallback if audio devices are unconfigured.

### Vibe Coding Prompt (Attempt 1 of 4)
> *"Add sound effects for eating food and for the game over event. Create a modular `SoundManager` class in `game/sound_manager.py` that handles `pygame.mixer` initialization safely. Synthesize clean 16-bit WAV audio files for `eat.wav` (pleasant ascending chime) and `game_over.wav` (descending defeat tone) and trigger them at the appropriate game events."*

### AI Response & Solution Implemented
1. Generated `sounds/eat.wav`: 44.1 kHz 16-bit PCM dual-tone chime (587 Hz to 880 Hz with exponential decay).
2. Generated `sounds/game_over.wav`: 44.1 kHz 16-bit PCM descending sweep (380 Hz down to 110 Hz with retro harmonic blend).
3. Created `SoundManager` with exception guarding:
   - Initializes mixer only if available.
   - Provides `play_eat()` and `play_game_over()`.
4. Connected triggers in `GameEngine.update()`:
   - When food is eaten -> `self.sound_manager.play_eat()`
   - When collision occurs -> `self.sound_manager.play_game_over()`

### Outcome & Verification
- Confirmed audio playback on both food consumption and game over events.
- **Git Commit:** `b8a8cff Task 4: Add sound effects for food consumption and game over events`

---

## Git Commit History

| Commit Hash | Message | Scope |
|-------------|---------|-------|
| `114601f` | Initial Snake starter | Upstream template |
| `5c648c6` | Task 1: Refine collision detection and prevent instant 180-degree self-collision | `game/snake.py` |
| `e46a728` | Task 2: Implement Game Over screen with score display and input wait | `game/game_engine.py` |
| `9e239b3` | Task 3: Add replay option with difficulty selection (Easy, Medium, Hard) | `game/game_engine.py` |
| `b8a8cff` | Task 4: Add sound effects for food consumption and game over events | `game/sound_manager.py`, `sounds/`, `game/game_engine.py` |

---

## Deliverables Summary

1. **Before Gameplay Video (`videos/before_gameplay.mp4`):** Demonstrates the original broken behavior (instant unfair 180° death upon pressing opposite direction key and lack of in-game Game Over screen).
2. **After Gameplay Video (`videos/after_gameplay.mp4`):** Demonstrates guarded direction inputs, score HUD, food eating with audio, Game Over dialog card, and difficulty selection replay.
3. **Updated Modular Codebase:** Clean OOP structure with `main.py`, `game/`, `sounds/`, and `requirements.txt`.
4. **Vibe Coding Prompt Log:** Documented rationale, prompts, and verification steps (all tasks completed in 1 prompt iteration each).
