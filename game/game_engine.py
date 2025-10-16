import pygame
import pygame
import os
import numpy as np
import wave
import struct
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

def generate_tone(filename, freq=440, duration=0.1, volume=0.5):
    """Generate a simple sine wave tone and save it as a .wav file."""
    framerate = 44100
    t = np.linspace(0, duration, int(framerate * duration))
    data = volume * np.sin(2 * np.pi * freq * t)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, framerate, 0, 'NONE', 'not compressed'))
        for s in data:
            wav_file.writeframes(struct.pack('h', int(s * 32767)))


class GameEngine:
    
    import pygame
import os
import numpy as np
import wave
import struct
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)


# =========================
# Helper: generate tone if file missing
# =========================
def generate_tone(filename, freq=440, duration=0.1, volume=0.5):
    """Generate a simple sine wave tone and save it as a .wav file."""
    framerate = 44100
    t = np.linspace(0, duration, int(framerate * duration))
    data = volume * np.sin(2 * np.pi * freq * t)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, framerate, 0, 'NONE', 'not compressed'))
        for s in data:
            wav_file.writeframes(struct.pack('h', int(s * 32767)))


# =========================
# Game Engine class
# =========================
class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.winning_score = 5

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # =========================
        # Step 3 — Sound setup here
        # =========================
        os.makedirs("assets", exist_ok=True)
        sound_files = {
            "paddle_hit.wav": 800,
            "wall_bounce.wav": 500,
            "score.wav": 200
        }

        for fname, freq in sound_files.items():
            fpath = os.path.join("assets", fname)
            if not os.path.exists(fpath):
                generate_tone(fpath, freq=freq, duration=0.08, volume=0.5)

        # Load sound effects
        self.sound_paddle = pygame.mixer.Sound("assets/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("assets/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("assets/score.wav")

        # Optional: set volumes
        self.sound_paddle.set_volume(0.6)
        self.sound_wall.set_volume(0.5)
        self.sound_score.set_volume(0.8)

    # ... (rest of your GameEngine methods: handle_input, update, render, etc.)


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move(self.player, self.ai, sound_wall=self.sound_wall, sound_paddle=self.sound_paddle)



        if self.ball.x <= 0:
            self.ai_score += 1
            self.sound_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.sound_score.play()
            self.ball.reset()


        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score:
            message = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            message = "AI Wins!"
        else:
            return False  # No winner yet

        # Show winner message
        font_large = pygame.font.SysFont("Arial", 60)
        text = font_large.render(message, True, WHITE)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 60))
        screen.blit(text, text_rect)

        # Show replay menu
        font_small = pygame.font.SysFont("Arial", 28)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit",
        ]
        for i, opt in enumerate(options):
            opt_text = font_small.render(opt, True, WHITE)
            screen.blit(opt_text, (self.width // 2 - 150, self.height // 2 + i * 40))
        pygame.display.flip()

        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 3
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.winning_score = 5
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.winning_score = 7
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            pygame.time.delay(100)

        # Reset for a new match
        self.reset_game()
        return False
    
    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
