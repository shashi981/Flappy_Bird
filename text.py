# Font class for Flappy Bird

import pygame


class Font:
    """
        Create the texts and images of text to be displayed
    """
    def __init__(self, surface, bottom):
        """
            Creating the intro and outro of the game
        :param surface: Main Surface window
        :param bottom: Ground surface
        """
        self.surface = surface
        self.bottom = bottom

        # font objects
        self.game_font = pygame.font.Font("./Assets/font/FB.ttf", int(surface.get_width()//10.8))
        self.score_font = pygame.font.Font("./Assets/font/FB.ttf", int(surface.get_width()//8.30))
        self.intro_font = pygame.font.Font("./Assets/font/PixelFJVerdana12pt.ttf", int(surface.get_width()/54))
        # restart image
        restart = pygame.image.load("./Assets/images/restart.png").convert_alpha()
        self.restart = pygame.transform.scale(restart, (int(self.surface.get_width() // 3.36), int(self.surface.get_height() // 17.06)))

        # score card image
        score_card = pygame.image.load("./Assets/images/score.png").convert_alpha()
        self.score_card = pygame.transform.scale(score_card, (int(surface.get_width() // 3.13), int(surface.get_height() // 4.21)))

        # main text surface
        self.main_text = self.game_font.render("Flappy Bird", True, pygame.Color("white"))
        self.main_text2 = self.game_font.render("Flappy Bird", True, pygame.Color("black"))     # black shadow

        # intro text surface
        self.intro_text = self.intro_font.render("press SPACE to start the game", True, pygame.Color(83, 55, 70))

        # game over surface
        self.game_over_text = self.game_font.render("Game Over", True, pygame.Color("white"))
        self.game_over_text2 = self.game_font.render("Game Over", True, pygame.Color("black"))  # black shadow

        # center y co-ordinate of the surface
        self.middle_position = self.surface.get_height() // 2 - self.bottom.get_rect().height - int(self.surface.get_height() // 6.4)

        # +10 offset for text
        self.x_offset = int(self.surface.get_width() // 108)
        self.y_offset = int(self.surface.get_height() // 192)

    def draw_intro(self):
        """
            Blits the intro on the screen
        :return: None
        """
        # intro text
        x = self.surface.get_width() // 2 - self.main_text.get_width() // 2
        y = self.surface.get_height() // 2 - self.bottom.get_rect().height - self.surface.get_height() // 4.8
        self.surface.blit(self.main_text2, (x + self.x_offset, y + self.y_offset))
        self.surface.blit(self.main_text, (x, y))
        self.surface.blit(self.intro_text, (x, y + int(self.surface.get_height() // 14.76)))

    def draw_game_over(self, score):
        """
            Blits the game over screen
        :return: None
        """
        # game over text
        x = self.surface.get_width() // 2 - self.game_over_text.get_width() // 2
        self.surface.blit(self.game_over_text2, (x + self.x_offset, self.middle_position + self.y_offset))
        self.surface.blit(self.game_over_text, (x, self.middle_position))

        # score text variable
        score_text = self.score_font.render(score, True, pygame.Color('white'))
        score_text2 = self.score_font.render(score, True, pygame.Color('black'))

        # score card
        x = self.surface.get_width() // 2 - self.score_card.get_rect().width // 2
        y = self.middle_position + int(self.surface.get_height() // 12.8)
        self.surface.blit(self.score_card, (x, y))

        # score text
        x = x + self.score_card.get_rect().width//2 - score_text.get_rect().width//2
        y = y + self.score_card.get_rect().height//2 - score_text.get_rect().height//2
        self.surface.blit(score_text2, (x + self.x_offset, y + self.y_offset))
        self.surface.blit(score_text, (x, y))

        # restart
        self.surface.blit(self.restart, (self.surface. get_width() // 2 - self.restart.get_rect().width // 2, self.middle_position + self.score_card.get_rect().height + int(self.surface.get_height() // 11.29)))

    def draw_score(self, score):
        """
            Blit the current score on the screen
        :return: None
        """
        # score text
        x = self.surface.get_width() // 2
        y = self.surface.get_height() * 0.1
        score_text = self.score_font.render(score, True, pygame.Color('white'))
        score_text2 = self.score_font.render(score, True, pygame.Color('black'))
        self.surface.blit(score_text2, (x + self.x_offset, y + self.y_offset))
        self.surface.blit(score_text, (x, y))
