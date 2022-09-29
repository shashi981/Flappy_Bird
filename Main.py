# Flappy Bird

import pygame
from bird import Bird
from pipe import Pipe
from text import Font


def main():
    pygame.init()
    window_size = (480, 820)
    pygame.display.set_mode(window_size)
    pygame.display.set_caption("Flappy Bird")
    window_surface = pygame.display.get_surface()
    game = Game(window_surface)
    game.play()
    pygame.quit()


# Main game class
class Game:
    def __init__(self, surface):
        """
        :param surface: surface of the window
        """
        # game variables
        self.surface = surface
        self.clock = pygame.time.Clock()
        self.continue_game = True
        self.game_pause = False
        self.start_game = False
        self.collision = False

        # score variables
        self.score = 0
        self.cross_pipe1 = False
        self.cross_pipe2 = False

        # fps counter
        self.fps = 30

        # background and ground
        self.background = pygame.image.load("./Assets/images/flappy_background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (surface.get_width(), surface.get_height()))
        self.ground = pygame.image.load("./Assets/images/ground.png").convert_alpha()
        self.ground = pygame.transform.scale(self.ground, (surface.get_width(), int(surface.get_height()//5.48)))
        self.bg_scroll = 0
        self.rel_x = self.bg_scroll % self.ground.get_rect().width  # for background scrolling
        self.ground_y = self.surface.get_height() - self.ground.get_rect().height

        # flappy objects
        self.player = Bird(self.surface, self.background)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.dt = None  # timer for bird animation

        # bottom rect for collision
        self.bottom_rect = pygame.Rect(0, self.surface.get_height() - self.ground.get_rect().height,
                                       self.ground.get_rect().width, self.ground.get_rect().height)

        # pipe object
        self.pipe1 = Pipe(self.surface, self.ground)
        self.pipe2 = Pipe(self.surface, self.ground)

        # pipe scroll variables
        self.pipe1_rel_x = self.surface.get_width() + self.surface.get_width() // 1.08     # added 1000 to give some time when game starts
        self.min_pipe1_rel_x = -self.pipe1.pipe_width()

        self.pipe2_rel_x = self.surface.get_width() + self.surface.get_width() // 1.54 + self.surface.get_width() // 1.08      # added 700 due to pipe difference
        self.min_pipe2_rel_x = -self.pipe2.pipe_width()

        # game texts object
        self.game_text = Font(self.surface, self.ground)

    def play(self):
        """
            Main Game Loop
        :return: None
        """
        while self.continue_game:
            self.dt = self.clock.tick(self.fps) / 1000  # for game animation
            self.event_handler()  # handling pygame events

            if self.start_game:
                self.play_game()  # game start function

            if not self.game_pause:
                self.player.image_animation(self.dt, self.start_game)  # bird animation

            self.draw()

            if not self.start_game:
                if not self.game_pause:
                    self.game_text.draw_intro()

            if self.game_pause:
                self.game_text.draw_game_over(str(self.score))

            pygame.display.update()

    def event_handler(self):
        """
            Handles pygame events
        :return: None
        """
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                self.continue_game = False
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_SPACE]:
                    self.start_game = True
                    self.player.jump(True)
                if not keys[pygame.K_SPACE]:
                    self.player.jump(False)
                if keys[pygame.K_SPACE]:
                    if self.game_pause:
                        self.__init__(self.surface)     # restarts the game
                        self.dt = self.clock.tick(self.fps) / 1000
                if keys[pygame.K_ESCAPE]:
                    self.continue_game = False
        if self.collision:
            self.game_pause = True
            self.start_game = False

    def play_game(self):
        """
            Starts the game when space is pressed
        :return: None
        """
        self.pipe_scroll()
        self.player.rotation(self.dt)
        self.player.move()
        self.update_score()
        self.player_collision()

    def draw(self):
        """
            Draws the objects on the surface
        :return: None
        """
        self.surface.blit(self.background, (0, -self.ground.get_rect().height))
        if self.start_game:
            self.pipe1.draw(self.pipe1_rel_x)
            self.pipe2.draw(self.pipe2_rel_x)
            self.game_text.draw_score(str(self.score))
        self.all_sprites.draw(self.surface)
        if not self.game_pause:
            self.background_scroll()
        if self.game_pause:     # draws the last frame when game pauses
            self.pipe1.draw(self.pipe1_rel_x)
            self.pipe2.draw(self.pipe2_rel_x)
            self.surface.blit(self.ground, (self.rel_x - self.ground.get_rect().width, self.ground_y))
            self.surface.blit(self.ground, (self.rel_x, self.ground_y))

    def background_scroll(self):
        """
            Infinite scroll of the ground when the game is being played
        :return: None
        """
        if self.continue_game:  # stars scrolling when game starts
            self.rel_x = self.bg_scroll % self.ground.get_rect().width
        self.surface.blit(self.ground, (self.rel_x - self.ground.get_rect().width, self.ground_y))
        if self.rel_x < self.surface.get_width():
            self.surface.blit(self.ground, (self.rel_x, self.ground_y))
        if self.continue_game:
            self.bg_scroll -= 10

    def pipe_scroll(self):  # maybe make it into list
        """
            Moves the pipes 10 pixels
        :return: None
        """
        if self.pipe1_rel_x < self.min_pipe1_rel_x:  # changes the pipe position when it goes out of window
            self.pipe1_rel_x = self.pipe2_rel_x + self.surface.get_width() // 1.54  # maintains the distance between the pipes
            self.cross_pipe1 = False
            self.pipe1.pip_position()
        self.pipe1_rel_x -= 10

        if self.pipe2_rel_x < self.min_pipe2_rel_x:
            self.pipe2_rel_x = self.pipe1_rel_x + self.surface.get_width() // 1.54
            self.cross_pipe2 = False
            self.pipe2.pip_position()
        self.pipe2_rel_x -= 10

    def player_collision(self):
        """
            Checks for collision with the player and the bird
        :return: None
        """
        if self.pipe1.collision(self.player.collision_rect):
            self.collision = True
        elif self.pipe2.collision(self.player.collision_rect):
            self.collision = True
        elif self.bottom_rect.colliderect(self.player.collision_rect):
            self.collision = True

    def update_score(self):
        if self.player.return_pos() > self.pipe1_rel_x + self.pipe1.pipe_width() and self.cross_pipe1 is False:
            self.score += 1
            self.cross_pipe1 = True
        if self.player.return_pos() > self.pipe2_rel_x + self.pipe2.pipe_width() and self.cross_pipe2 is False:
            self.score += 1
            self.cross_pipe2 = True


if __name__ == "__main__":
    main()
