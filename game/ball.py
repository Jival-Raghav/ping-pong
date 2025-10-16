import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, player, ai, sound_wall=None, sound_paddle=None):
        old_vx = self.velocity_x
        old_vy = self.velocity_y

        # Move ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if sound_wall:
                sound_wall.play()

        # Paddle collision
        ball_rect = self.rect()
        if ball_rect.colliderect(player.rect()) or ball_rect.colliderect(ai.rect()):
            self.velocity_x *= -1
            if sound_paddle:
                sound_paddle.play()

            # Prevent sticking
            if self.velocity_x > 0:
                self.x = player.x + player.width
            else:
                self.x = ai.x - self.width

    def check_collision(self, player, ai):
        if self.rect().colliderect(player.rect()) or self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
