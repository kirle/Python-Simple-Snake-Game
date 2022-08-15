import pygame
from pygame import mixer
import numpy as np
import time
import random	

#---------------------------------
# --> GLOBAL VARIABLES
#---------------------------------

#Game 
speed = 0.5 
width, height = 1000,1000
bg_color = 255,0,255 #RGB(pink)

#Board
NUMBX, NUMBY = 10, 10
dimCW = width/NUMBX
dimCH = height/NUMBY


#---------------------------------
# --> FUNCTIONS
#---------------------------------

#Shows "text" message on a new screen
def showMessage(text):
	pygame.init()
	screen = pygame.display.set_mode(size=(height, width))
	screen.fill(bg_color)

	font = pygame.font.Font(None, 40)

	message = font.render(text, 1, (231, 76, 60))
	screen.blit(message, (width/2 -100, height/2 -100))
	pygame.display.flip()

#Returns a tuple with current direction on x and y axis 
def detect_direction():
	time.sleep(0.2)
	events = pygame.event.get()
	dirX = 0
	dirY = 0

	for event in events:
	 	if event.type == pygame.KEYDOWN: 

		 	if event.key == pygame.K_DOWN:
	 			dirX = 0
	 			dirY = 1
	 		if event.key == pygame.K_UP:
	 			dirX = 0 
	 			dirY = -1
		 	if event.key == pygame.K_RIGHT:
	 			dirX = 1
	 			dirY = 0
	 		if event.key == pygame.K_LEFT:
	 			dirX = -1 
	 			dirY = 0

	return dirX, dirY



#---------------------------------

def main():

	pygame.init()

	#Mixer initialitation
	mixer.init()
	mixer.music.load("born.mp3") 
	mixer.music.set_volume(0.7)
	mixer.music.play()

	#Screen initialitation
	screen = pygame.display.set_mode(size=(height, width))
	screen.fill(bg_color)

	initial_gameState = np.zeros((NUMBX,NUMBY)) #matrix of ceros of (NUMBX,NUMBY) as initial state of the game

	#Random location for player
	initial_x = random.randint(0, NUMBX-1)
	initial_y = random.randint(0, NUMBY-1)

	#Random location for item
	item_x = random.randint(0, NUMBX - 1) 
	item_y = random.randint(0, NUMBY - 1)

	while(item_x == initial_x or item_y == initial_y):
		item_x = random.randint(0, NUMBX - 1)
		item_y = random.randint(0, NUMBY - 1)	
	initial_gameState[item_x,item_y] = 2  # Items on board will be marked as "2"

	#Variables for game
	pause = False 
	tailSize = 0 
	dirActualX = 0
	dirActualY = 0
	player = [0]*30 #Positions of each player square

	#First iteration
	player[0] = initial_x,initial_y	#head position
	initial_gameState[player[0]] = 1 


	continueGame = True
	gameOver = False

	#Execution loop
	while continueGame:
		
		current_gameState = np.copy(initial_gameState) 
		screen.fill(bg_color)
		
		### *****************
		### Moving player
		### *****************

		dirX , dirY = detect_direction()
		
		if( (dirX != 0 or dirY !=0) and (dirX != -dirActualX or dirY != -dirActualY) ):
			dirActualX = dirX
			dirActualY = dirY
		

		initial_gameState[player[0]] = 0 


		#Moving the tail
		if(tailSize != 0): 
			player_aux = np.copy(player)
	
			for i in range(0,tailSize):
				initial_gameState[player[i+1]] = 0

				player[i+1] = player_aux[i] #Moving i+1 to original and safe-copied i position
				
				initial_gameState[player[i+1]] = 3 # Tail squares marked as "3"


		#Moving head

		initial_x = initial_x + dirActualX
		initial_y = initial_y + dirActualY
		
		if(initial_x >= NUMBX):
			initial_x = 0
		if(initial_y >= NUMBY):
			initial_y = 0	
		if(initial_x < 0):
			initial_x = NUMBX - 1	
		if(initial_y < 0):
			initial_y = NUMBY - 1

		player[0] = (initial_x, initial_y) #new head position

		initial_gameState[player[0]] = 1 # next head position

		#If head collides with the tail
		if(current_gameState[player[0]] == 3):
			continueGame = False
			gameOver = True

		


		### *****************
		### Taking items
		### *****************		

		if(current_gameState[player[0] ] == 2): 

			initial_gameState[player[0]] = 1

			tailSize = tailSize+1

			dirColaX = (player[tailSize-1])[0]
			dirColaY = (player[tailSize-1])[1]
			
			player[tailSize] = (dirColaX - dirActualX, dirColaY - dirActualY)
			
			#If trying to add tail out of the limits
			if(player[tailSize][0] > 9):
				player[tailSize] = (9,player[tailSize][1])
			if(player[tailSize][1] > 9):
				player[tailSize] = (player[tailSize][0],9)  

			initial_gameState[ player[tailSize] ] = 3

			#Plays a sound when taking an item
			sounda= pygame.mixer.Sound("audio.wav")
			sounda.play()

			#New item position
			item_x = random.randint(0, NUMBX - 1)
			item_y = random.randint(0, NUMBY - 1)

			while(initial_gameState[item_x,item_y] == 1 or initial_gameState[item_x,item_y] == 3):
				item_x = random.randint(0, NUMBX - 1)
				item_y = random.randint(0, NUMBY - 1)

			initial_gameState[item_x,item_y] = 2

		

		### *****************
		### Generating board
		### *****************
		
		for x in range(0,NUMBY):
			for y in range(0,NUMBX):
				box_polygon = [( (x)   * dimCW, y * dimCH),
					( (x+1) * dimCW, y * dimCH),
					( (x+1) * dimCW, (y+1) * dimCH),
					( (x)   * dimCW, (y+1) * dimCH)]

				

				if(current_gameState[x,y] == 0):
					pygame.draw.polygon(screen, (0xFFFFFF), box_polygon, 1) #Draws black square
				elif(current_gameState[x,y] == 1):
					pygame.draw.polygon(screen, (0x000000), box_polygon, 0) #For HEAD square
				elif(current_gameState[x,y] == 3):
					pygame.draw.polygon(screen, (0x0000FF), box_polygon, 0) #For TAIL square
				else:
					pygame.draw.polygon(screen, (0x00FF00), box_polygon, 0) #For ITEM square

		

		pygame.display.flip() #Updating displayed board
		
		#End of the game, max size reached
		if(tailSize == len(player)):
			continueGame = False

		#Prints debugging section

		'''
		print("player:\n")
		print(player)
		print(tailSize)
		'''

	# END OF GAME LOOP
 	
	if (gameOver == True):
		time.sleep(4)
		showMessage("Game over")
		
	else: 
		time.sleep(4)
		showMessage("You win")
		




if __name__ == "__main__":
	main()	