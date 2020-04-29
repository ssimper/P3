import random


class Labyrinth:
    """Building the maze.

    The construction is made from a txt file.
Each '.' representing a path and each '#' representing a wall.
Pick 3 random position for the accessories MacGyver needs to win.
Positioning of the strat and end points of the game.
Creation of MacGyver, the information title and the score.
    """

    def __init__(self):
        self.paths = set()  # set of paths
        self.walls = set()  # set of walls
        self.rand_pos = set()  # set of items
                
    def build_map(self, the_file):
        """Function that reads the file, generate a set of paths and
         a set of walls, find the size of the labyrinth, find the start
         and finish point of the labyrinth"""
        with open(the_file, "r") as f:
            # reading each lines of the file
            for num_lines, lines in enumerate(f):
                num_col = 0
                # read each caracters of lines
                for caracters in lines.strip():
                    if caracters == ".":  # a path
                        self.paths.add(Position(num_col, num_lines))
                    elif caracters == "#":  # a wall
                        self.walls.add(Position(num_col, num_lines))
                    elif caracters == "S":  # the start position
                        self.start_pos = Position(num_col, num_lines)
                    elif caracters == "F":  # the finish position
                        self.finish_pos = Position(num_col, num_lines)
                    num_col += 1
            return self.walls, self.paths, self.start_pos, self.finish_pos

    def start_finish_to_path(self):
        """Put the start and the finish position in the paths set"""
        self.paths.add(self.start_pos)
        self.paths.add(self.finish_pos)

    def random_position(self):
        '''Loop throught self_path, 3 times randomly pickup coords
        and add it to self.rand_pos set '''
        self.rand_pos.clear()
        self.rand_pos = random.sample(self.paths, 3)
        return self.rand_pos


class Position:
    """Create and compare positions."""

    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def __eq__(self, other):
        """Special method to compare two positions."""
        return (
            self.posx == other.posx
            and self.posy == other.posy
        )

    def __hash__(self):
        """Keep the hashability for the set."""
        return hash((self.posx, self.posy))


class TitleScore:
    """Title position."""

    def __init__(self):
        self.position = (3, 15)


class Score:
    """Score Position"""

    def __init__(self):
        self.position = (10, 15)


class MacGyver:
    """Creating the hero."""

    def __init__(self, lab):
        # the first position of MG is the start point
        self.position = lab.start_pos
        # Connector to the Labyrinth's class.
        self.lab = lab
        # Number of accessories to pick-up.
        self.accessory_number = len(lab.rand_pos)
        # Information to show to the gamer.
        self.destiny = "title_score"
        # Default representation of the MacGyver sprite.
        self.profil = "right"
        # As long as MacGyver hasn't reach the guard.
        self.status = True

    def change_position(self, direction):
        """Calculate the new MacGyver position from the keyboard input
        and determines whether it is in the path list or the wall list.
        It also verify if the new position is the same as an accessory."""
        new_position = Position(self.position.posx, self.position.posy)
        if direction == "right":
            self.profil = "right"
            new_position.posx = self.position.posx + 1
        elif direction == "left":
            self.profil = "left"
            new_position.posx = self.position.posx - 1
        elif direction == "up":
            self.profil = "up"
            new_position.posy = self.position.posy - 1
        elif direction == "down":
            new_position.posy = self.position.posy + 1
        # Verify if the new position is an accessory
        if new_position in self.lab.rand_pos:
            self.accessory_number -= 1
            # delete picked-up accessory from set
            self.lab.rand_pos.remove(new_position)
        if new_position in self.lab.paths:
            self.position = new_position
        if new_position == self.lab.finish_pos:
            if self.accessory_number == 0:
                self.profil = self.destiny = "win"
            else:
                print("You loose !!!")
                self.profil = self.destiny = "loose"
            self.status = False
        return self.position, self.profil
