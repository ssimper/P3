import pygame
import os

#from hero import Hero, right
from mg03 import Labyrinth, Position, MacGyver
from colors import WHITE, RED


class HeroSprite(pygame.sprite.Sprite):
    def __init__(self, hero):
        super().__init__()
        self.hero = hero
        #self.image = pygame.Surface((50, 50))
        #self.image.fill(RED)
        self.image = pygame.image.load("pics/mg.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.update()

    def update(self):
        x, y = self.hero.position.posx, self.hero.position.posy 
        self.rect.x = x * 50
        self.rect.y = y * 50


class Game:
    def __init__(self):
        pygame.init()

        # Instancier les objets de ton jeu
        self.lab = Labyrinth() #The Laby
        self.lab.fonction("fichier03.txt") #Construction of the map
        self.lab.random_position() #generate items position
        print("Toto was here")
        self.hero = MacGyver(self.lab)
        print("Toto was here")

        # Créer la fenêtre
        self.window = pygame.display.set_mode((750, 750))#50(sprite size)*15(number of box)
        self.window.fill(WHITE)

        # créer un fond
        self.background = pygame.Surface((750, 750))
        #self.background = pygame.image.load("pics/bg.png").convert()
        # pour une image pygame.image.load("/chemin/vers/image").convert() convert_alpha()
        self.background.fill(WHITE)
        #placement des murs :
        self.wall = pygame.image.load("pics/wall50.png").convert()
        for walls in self.lab.walls:
            self.background.blit(self.wall, (walls.posx * 50, walls.posy * 50))
        #placement des chemins
        self.path = pygame.image.load("pics/path50.png").convert()
        for paths in self.lab.paths:
            self.background.blit(self.path, (paths.posx * 50, paths.posy * 50))
        #placement des items
        self.accessories_list = []
        for accessory in self.lab.rand_pos:
            self.accessories_list.append(accessory)
        print(self.accessories_list)
        self.accessorie01 = pygame.image.load("pics/gants.png").convert_alpha()
        self.background.blit(self.accessorie01, (self.accessories_list[0].posx * 50, self.accessories_list[0].posy * 50))
        self.accessorie02 = pygame.image.load("pics/masque.png").convert_alpha()
        self.background.blit(self.accessorie02, (self.accessories_list[1].posx * 50, self.accessories_list[1].posy * 50))
        self.accessorie03 = pygame.image.load("pics/gel.png").convert_alpha()
        self.background.blit(self.accessorie03, (self.accessories_list[2].posx * 50, self.accessories_list[2].posy * 50))

        #création du point d'entrée
        self.start_point = pygame.image.load("pics/start50.png").convert()
        self.background.blit(self.start_point, (self.lab.start_pos.posx * 50, self.lab.start_pos.posy * 50))

        #création du point de sortie
        self.finish_point = pygame.image.load("pics/finish50.png").convert()
        self.background.blit(self.finish_point, (self.lab.finish_pos.posx * 50, self.lab.finish_pos.posy * 50))

        self.sprites = pygame.sprite.Group(HeroSprite(self.hero))

    def start(self):
        self.running = True
        while self.running:

            self.window.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        #self.hero.move(right)
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
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
