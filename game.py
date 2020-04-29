import pygame

from labyrinth import Labyrinth, MacGyver, TitleScore, Score
from colors import BLACK
from dimensions import (
    SPRITE_SIZE_X,
    SPRITE_SIZE_Y,
    BOARD_SIZE_X,
    BOARD_SIZE_Y
)


class HeroSprite(pygame.sprite.Sprite):
    """Sprite of MacGyver."""

    def __init__(self, hero):
        super().__init__()
        self.hero = hero
        self.image = pygame.image.load(
            f"pics/mg_{self.hero.profil}.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()

        self.update()

    def update(self):
        """Update the sprite image after a move.

        The representation of MacGyver change with the direction.
        Specific sprites for left, right and up.
        """
        self.image = pygame.image.load(
            f"pics/mg_{self.hero.profil}.png"
        ).convert_alpha()
        x, y = self.hero.position.posx, self.hero.position.posy
        self.rect.x = x * SPRITE_SIZE_X
        self.rect.y = y * SPRITE_SIZE_Y


class AccessorySprite(pygame.sprite.Sprite):
    """Sprites representing the three accessories."""

    def __init__(self, lab, accessory_position, image_name):
        super().__init__()
        self.lab = lab
        self.accessory_position = accessory_position
        self.image = pygame.image.load(
            f"pics/{image_name}.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.update()

    def update(self):
        """Update the sprite.

        If MacGyver takes an object the image is replaced by the path.
        """
        x, y = self.accessory_position.posx, self.accessory_position.posy
        if self.accessory_position in self.lab.rand_pos:
            self.rect.x = x * SPRITE_SIZE_X
            self.rect.y = y * SPRITE_SIZE_Y
        else:
            self.image = pygame.image.load("pics/path50.png").convert()


class TitleScoreSprite(pygame.sprite.Sprite):
    """Sprite for the infomrations of scoring and status.

    Those informations are : objects to pick-up, you win or you loose.
    """

    def __init__(self, hero, title_score):
        super().__init__()
        self.hero = hero
        self.title_score = title_score
        self.image = pygame.image.load(
            f"pics/{self.hero.destiny}.png").convert()
        self.rect = self.image.get_rect()

        self.update()

    def update(self):
        """Updte the sprite.

        If the gamer wins or loses, the sprite coords change to be centered.
        """
        self.image = pygame.image.load(
            f"pics/{self.hero.destiny}.png").convert()
        x, y = self.title_score.position
        if self.hero.destiny == "win" or self.hero.destiny == "loose":
            self.rect.x = 0
            self.rect.y = 750
        else:
            self.rect.x = x * SPRITE_SIZE_X
            self.rect.y = y * SPRITE_SIZE_Y


class ScoreSprite(pygame.sprite.Sprite):
    """Sprite representing the number of accessories left."""

    def __init__(self, hero, score):
        super().__init__()
        self.hero = hero
        self.score = score
        self.image = pygame.image.load(
            f"pics/{self.hero.accessory_number}.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.update()

    def update(self):
        """Update the sprite."""
        self.image = pygame.image.load(
            f"pics/{self.hero.accessory_number}.png").convert()
        x, y = self.score.position
        self.rect.x = x * SPRITE_SIZE_X
        self.rect.y = y * SPRITE_SIZE_Y


class Game:
    """Creation of the maze.

    Creation of the window containing the game.
    Instantiation of the labyrinth, the hero, the title barre and the score.
    Calling the functions to build the map, create random position for the
    accessories, the start and eding position.
    """

    def __init__(self):
        pygame.init()
        # The labyrinth
        self.lab = Labyrinth()
        # Map construction
        self.lab.build_map("maze.txt")
        # Random positions for the accessories
        self.lab.random_position()
        # Replace the start en finish position in the path
        self.lab.start_finish_to_path()
        # Creating the Hero
        self.hero = MacGyver(self.lab)
        # Creating the information title
        self.title_score = TitleScore()
        # Creating the score countdown
        self.score = Score()
        # The windows of the game
        self.window = pygame.display.set_mode(
            (BOARD_SIZE_X, BOARD_SIZE_Y)
        )
        self.window.fill(BLACK)
        self.background = pygame.Surface((750, 750))
        self.background.fill(BLACK)
        # Walls positioning
        self.wall = pygame.image.load("pics/wall50.png").convert()
        for walls in self.lab.walls:
            self.background.blit(
                self.wall,
                (walls.posx * SPRITE_SIZE_X, walls.posy * SPRITE_SIZE_Y)
            )
        # Paths positioning
        self.path = pygame.image.load("pics/path50.png").convert()
        for paths in self.lab.paths:
            self.background.blit(
                self.path,
                (paths.posx * SPRITE_SIZE_X, paths.posy * SPRITE_SIZE_Y)
            )
        # Starting point positioning
        self.start_point = pygame.image.load("pics/start50.png").convert()
        self.background.blit(
            self.start_point,
            (
                self.lab.start_pos.posx * SPRITE_SIZE_X,
                self.lab.start_pos.posy * SPRITE_SIZE_Y
            )
        )
        # Finish point positioning
        self.finish_point = pygame.image.load("pics/finish50.png").convert()
        self.background.blit(
            self.finish_point,
            (
                self.lab.finish_pos.posx * SPRITE_SIZE_X,
                self.lab.finish_pos.posy * SPRITE_SIZE_Y
            )
        )
        # Coordinate assignment to the accessories.
        tub_position, ether_position, syringe_position = self.lab.rand_pos
        # Creation of the sprites group
        self.sprites = pygame.sprite.Group(
            AccessorySprite(self.lab, tub_position, "tub"),
            AccessorySprite(self.lab, ether_position, "ether"),
            AccessorySprite(self.lab, syringe_position, "syringe"),
            HeroSprite(self.hero),
            ScoreSprite(self.hero, self.score),
            TitleScoreSprite(self.hero, self.title_score)
        )

    def start(self):
        """Starting the game !"""
        self.running = True
        while self.running:
            self.window.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Waiting for left, right, up and down keys as long as MacGyver
                # hasn't reached the guard yet.
                elif event.type == pygame.KEYDOWN and self.hero.status:
                    if event.key == pygame.K_RIGHT:
                        self.hero.change_position("right")
                    elif event.key == pygame.K_LEFT:
                        self.hero.change_position("left")
                    elif event.key == pygame.K_UP:
                        self.hero.change_position("up")
                    elif event.key == pygame.K_DOWN:
                        self.hero.change_position("down")

            self.sprites.update()
            self.sprites.draw(self.window)

            pygame.display.update()


def main():
    """Instantiation and starting the game."""
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
