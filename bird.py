# Bird Class of Flappy Bird

import pygame
import math


class Bird(pygame.sprite.Sprite):
    def __init__(self, surface, background):
        """
        :param surface: surface of the window
        :param background: background rect
        """
        super().__init__()      # sprite initialisation
        # loading images
        self.surface = surface
        self.group_images = [pygame.image.load("./Assets/images/bird_1.png").convert_alpha(),
                             pygame.image.load("./Assets/images/bird_2.png").convert_alpha(),
                             pygame.image.load("./Assets/images/bird_3.png").convert_alpha()]
        for i in range(3):
            self.group_images[i] = pygame.transform.scale(self.group_images[i], (int(surface.get_width()//7.8), int(surface.get_height()//20)))   # scaling image for Display
        self.image_index = 0
        self.image = self.group_images[0]   # used by sprite to blit to surface

        # bird position variables
        self.rect = self.image.get_rect()
        self.rect.x = surface.get_width() * 0.4 - self.rect.width//2
        self.rect.y = background.get_rect().height * 0.35
        self.temp_y = self.rect.y       # for repeating pattern

        # rotated images
        self.rotated_group_images = []
        for i in range(3):
            self.rotated_group_images.append(pygame.transform.rotate(self.group_images[i], 40))

        # flapping animation variables
        self.flapping_animation_time = 0.1
        self.flapping_current_time = 0
        self.bounce_x = 0

        # rotation variables
        self.max_rotation = -130
        self.rotate = -10
        self.rotated = 0
        self.rotation_animation_time = 0.05
        self.rotation_time = 0

        # rect for detecting collision
        self.collision_rect = self.rect
        self.collision_rect.y += surface.get_height() // 64    # to match bird's new position
        self.collision_rect.height += surface.get_height() // 64

        # game variables
        self.isUp = False
        self.isDown = False
        self.isJump = False
        self.jump_height = 0

        # moving variables
        self.max_jump = 10
        self.jump_count = 0

        # for different resolutions
        if self.surface.get_height() < 1920:
            self.jump_range = 0.3
        else:
            self.jump_range = 0.5

    def image_animation(self, dt, game_start):
        """
            Animation for the bird sprite
        :param dt: int, for frame animation
        :param game_start: Bool
        :return: None
        """
        if game_start:
            self.flapping_current_time += dt
            if self.flapping_current_time >= self.flapping_animation_time:      # changes every 5 frames
                self.flapping_current_time = 0
                self.image_index = (self.image_index + 1) % len(self.group_images)
                self.image = self.group_images[self.image_index]

        if not game_start:
            self.flapping_current_time += dt
            if self.flapping_current_time >= self.flapping_animation_time:      # changes every 5 frames
                self.flapping_current_time = 0
                self.rect.y += 20 * math.sin(self.bounce_x)         # moves the bird in a repeated pattern
                self.bounce_x += 0.5
                if self.bounce_x > 2 * math.pi:
                    self.bounce_x = 0
                    self.rect.y = self.temp_y       # places the bird back to original position

    def move(self):
        """
            Moves the Bird based on player input
        :return: None
        """
        if self.isJump:
            self.jump_count = self.max_jump
            self.isJump = False

        neg = 1     # for changing direction of the parabola
        if self.jump_count < 0:
            neg = -1

        self.rect.y -= self.jump_count**2 * neg * self.jump_range   # move the bird in a parabola
        self.collision_rect.y -= self.jump_count**2 * neg * self.jump_range
        if self.jump_count < 0:
            self.jump_count -= 0.5      # slows down when the bird is falling
        else:
            self.jump_count -= 1

    def rotation(self, dt):
        """
            Rotates the bird as per its position
        :param dt: for counting frames
        :return: None
        """
        if self.isJump and not self.isUp:
            old_center = self.rect.center
            for i in range(3):
                self.group_images[i] = self.rotated_group_images[i]
            self.image = self.group_images[self.image_index]
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.isUp, self.isDown = True, False

        if self.isUp and self.isJump:
            self.jump_height = self.rect.y

        if not self.isJump and not self.isDown:
            if self.rect.y > self.jump_height:
                if self.rotated >= self.max_rotation:
                    self.rotation_time += dt
                    if self.rotation_time >= self.rotation_animation_time:
                        self.isUp = False
                        old_center = self.rect.center
                        for i in range(3):
                            self.group_images[i] = pygame.transform.rotate(self.group_images[i], self.rotate)
                        self.image = self.group_images[self.image_index]
                        self.rect = self.image.get_rect()
                        self.rect.center = old_center
                        self.rotated += self.rotate
                        if self.rotated == self.max_rotation:
                            self.isDown = True
                            self.rotated = 0

    def jump(self, val):
        """
            changes the isJump when player jumps
        :return: None
        """
        self.isJump = val

    def return_pos(self):
        return self.rect.x
