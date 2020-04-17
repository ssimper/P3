import random

class Labyrinth:

	def __init__(self):
		self.paths = set() #set of paths
		self.rand_pos = set() #set of items
		self.walls = set() #set of walls
		self.size_x = 0 #board width
		self.size_y = 0 #board height

	def fonction(self, the_file):
		"""Function that reads the file, generate a set of paths and
		 a set of walls, find the size of the labyrinth, find the start
		 and finish point of the labyrinth"""
		with open(the_file, "r") as f:
			for num_lines, lines in enumerate(f):#reading each lines of the file
				num_col = 0
				for caracters in lines.strip():#reading each caracters of lines
					if caracters == ".": # a path
						self.paths.add(Position(num_col, num_lines))
					elif caracters == "#": # a wall
						self.walls.add(Position(num_col, num_lines))
					elif caracters == "S": # the start position
						self.start_pos = Position(num_col, num_lines)
					elif caracters == "F": # the finish position
						self.finish_pos = Position(num_col, num_lines)
					num_col += 1
			self.size_y = num_lines + 1
			self.size_x = num_col
			return self.walls, self.paths, self.size_x, self.size_y,\
					self.start_pos, self.finish_pos

	def start_finish_to_path(self):
		"""put the start and the finish position in the paths set"""
		self.paths.add(self.start_pos)
		self.paths.add(self.finish_pos)

	def random_position(self):
		'''Loop throught self_path, 5 times randomly pickup coords
		and add it to self.rand_path set '''
		self.rand_pos.clear()
		self.rand_pos = random.sample(self.paths, 3)
		return self.rand_pos


class Position:

	def __init__(self, posx, posy):
		self.posx = posx
		self.posy = posy

	def __eq__(self, other):
		return (
			self.posx == other.posx
			and self.posy == other.posy
			)

	def __hash__(self):
		return hash((self.posx, self.posy))

class DisplayResult:

	def __init__(self, result):
		self.result = result

	def __str__(self):
		return (
			f"Ensemble des chemins : {self.result.paths}\nEnsemble des murs : {self.result.walls}"
			)

class MacGyver:

	def __init__(self, lab):
		self.position = lab.start_pos #the first position of MG is the start point
		self.lab = lab #connector to the Labyrinth's class.
		self.accessory = 0 #At the start MG have no accessories.

	def change_position(self, direction):
		"""calculate the new MacGyver position from the keyboard input
		and determines whether it is in the path list or the wall list.
		It also verify if the new position is the same as an accessory."""
		new_position = Position(self.position.posx, self.position.posy)
		if direction == "right":
			print("on va à droite")
			new_position.posx = self.position.posx + 1
		elif direction == "left":
			print("on va à gauche")
			new_position.posx = self.position.posx - 1
		elif direction == "up":
			print("on va en haut")
			new_position.posy = self.position.posy - 1
		elif direction == "down":
			print("on va en bas")
			new_position.posy = self.position.posy + 1
		print(new_position.posx, new_position.posy)
		if new_position in self.lab.rand_pos: #if the position is an accessory
			self.accessory += 1
			print("Un objet trouvé !!!")
			self.lab.rand_pos.remove(new_position)#delete accessory from set
		if new_position in self.lab.paths:
			print("On progresse !!")
			self.position = new_position
		else:
			print("dans le mur !")
		return self.position
		
#def main():
#	lab = Labyrinth()
#	lab.fonction("fichier03.txt")
#	for wall in lab.walls:
#		print(lab.paths)
#	print(lab.size_x, lab.size_y)
#	print(Position(1, 0) in lab.paths)
#	print(Position(2, 0) in lab.walls)
#	print(lab.random_position())
#	print(lab.start_pos, lab.finish_pos)
#	lab.start_finish_to_path()
#	mg = MacGyver(lab)
	#while mg.position != lab.finish_pos:
	#	print("Position actuelle : ", mg.position.posx, mg.position.posy)
	#	direction = input("Quelle direction (gauche : g, droite : h, haut : y, bas : b)")
	#	mg.change_position(direction)
	#	print(mg.position in lab.paths)

#main()


'''Parcours et analyse du fichier
Pour chaque ligne et numéro de ligne i dans le fichier:
	Pour chaque caractère et numéro de colonne j dans la ligne:
		#Si le caractère est ".":
		#	Ajouter la position (j,i) dans les paths
		#Sinon si le caractère est "#":
		#	Ajouter la position (j, i) dans les walls
		#Sinon si le caractère est "S":
		#	Affecter la position à start
		#Sinon si le caractère est "F":
		#	Affecter le caractère à finish

Tirer N positions au sort dans les paths et stocker ces positions
dans un variable ou un attribut.

Ajouter les positions start et finish dans l ensemble des paths

Le héro aura sa propre classe et ses propores positions.
A l instanciation du héro on lui donne la position de départ.'''
