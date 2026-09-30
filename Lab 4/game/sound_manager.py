import os
import pygame

class SoundManager:
    """Manages audio effects for the Snake game."""

    def __init__(self, sound_dir=None):
        self.enabled = False
        self.eat_sound = None
        self.game_over_sound = None

        if sound_dir is None:
            sound_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds")

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            # Audio device not available; run silently without crashing
            self.enabled = False
            return

        eat_path = os.path.join(sound_dir, "eat.wav")
        game_over_path = os.path.join(sound_dir, "game_over.wav")

        if os.path.exists(eat_path):
            try:
                self.eat_sound = pygame.mixer.Sound(eat_path)
                self.eat_sound.set_volume(0.6)
            except pygame.error:
                self.eat_sound = None

        if os.path.exists(game_over_path):
            try:
                self.game_over_sound = pygame.mixer.Sound(game_over_path)
                self.game_over_sound.set_volume(0.7)
            except pygame.error:
                self.game_over_sound = None

    def play_eat(self):
        """Play food consumption sound effect."""
        if self.enabled and self.eat_sound:
            try:
                self.eat_sound.play()
            except pygame.error:
                pass

    def play_game_over(self):
        """Play game-over sound effect."""
        if self.enabled and self.game_over_sound:
            try:
                self.game_over_sound.play()
            except pygame.error:
                pass
