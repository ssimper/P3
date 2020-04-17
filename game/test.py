from mg03 import Labyrinth, Position

def main():
	lab2 = Labyrinth()
	lab2.fonction("fichier03.txt")
	for wall in lab2.walls:
		print(wall.posx, wall.posy)
	

main()