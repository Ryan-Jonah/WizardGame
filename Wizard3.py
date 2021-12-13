from pathlib import Path
import pygame
import time
import random


pygame.init()
pygame.mixer.init()

#COLOURS
WHITE      = (255, 255, 255)
BLACK      = (0  , 0  , 0  )
RED        = (255, 0  , 0  )
GREEN      = (0  , 255, 0  )
BLUE       = (0  , 0  , 255)
YELLOW     = (255, 255, 0  )
DARKGREEN  = (0  , 150, 0  )
DARKRED    = (150, 0,   0  )
DARKYELLOW = (150, 150, 60 )
GREY       = (200, 200, 200)
DARKBLUE   = (20 , 0  , 85 )


#MUSIC & SOUNDS
music_path = str(Path('./Music/Still_Night.mp3'))
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1.0)

laser1 = pygame.mixer.Sound(str(Path('SFX/Laser Sound 1.wav')))
laser2 = pygame.mixer.Sound(str(Path('SFX/Laser Sound 2.wav')))
laser3 = pygame.mixer.Sound(str(Path('SFX/Laser Sound 3.wav')))
laser4 = pygame.mixer.Sound(str(Path('SFX/Laser Sound 4.wav')))
laser5 = pygame.mixer.Sound(str(Path('SFX/Laser Sound 5.wav')))
laser6 = pygame.mixer.Sound(str(Path('SFX/Laser Sound 6.wav')))
laser7 = pygame.mixer.Sound(str(Path('SFX/Laser Sound 7.wav')))
laser8 = pygame.mixer.Sound(str(Path('SFX/Laser Sound 8.wav')))

#DISPLAY
display_width  = 800
display_height = int(display_width/2)
gameDisplay = pygame.display.set_mode((display_width, display_height))

img_WizardIcon = pygame.image.load(str(Path('Images/Wizard.png')))
pygame.display.set_caption("Wizard")
pygame.display.set_icon(img_WizardIcon)

pygame.display.update()
clock = pygame.time.Clock()
fps = 45

#IMAGES
img_Wizard     = pygame.image.load(str(Path('Images/Wizard2.png'))).convert_alpha()
img_Wizard2    = pygame.image.load(str(Path('Images/Wizard_L2.png'))).convert_alpha()
img_Moon       = pygame.image.load(str(Path('Images/Moon.png'))).convert_alpha()

#START POSITION
wizard_X = display_width / 8
wizard_Y = display_height - (display_height/4)

class Wizard(object):
	'''Class used to control the main character'''
	health = 100
	current_direction = 'right'
	sprite_width  = 36
	sprite_height = 48
	
	def __init__(self, x_coor, y_coor, sprite = img_Wizard):
		self.x = x_coor
		self.y = y_coor
		self.sprite = sprite
		self.jump_height = y_coor
		
	def move(self, direction, displace = 4):
	
		if direction == 'left':
			if self.current_direction == 'right':
				wiz = pygame.transform.flip(self.sprite, True, False)
				self.current_direction = 'left'
				self.sprite = wiz
			return displace - (displace*2) #Negative value
			
		elif direction == 'right':
			if self.current_direction == 'left':
				wiz = pygame.transform.flip(self.sprite, True, False)
				self.current_direction = 'right'
				self.sprite = wiz
			return displace
			
	def jump(self, jump_bool = False, jump_height = 30, displace = 6):
		
		if self.y >= (wizard_Y - jump_height) and jump_bool == True:
			self.y -= displace
		if wizard.y <= (wizard_Y - jump_height) and jump_bool != False:
			jump_bool = False
		if self.y <= wizard_Y and jump_bool == False:
			self.y += displace
			
		return jump_bool
		
	def attack(self, mouse_x, mouse_y):
	
		pygame.draw.line(gameDisplay, RED, ((self.x +self.sprite_width/2), (self.y +self.sprite_height/2)), (mouse_x, mouse_y), 3)
		pygame.draw.circle(gameDisplay, RED, (mouse_x, mouse_y), 5)
		pygame.display.update()
		
		#ATTACK SOUND
		if mouse_y <= 50:
			pygame.mixer.Sound.play(laser1)
		elif mouse_y >= 50 and mouse_y <= 100:
			pygame.mixer.Sound.play(laser2)
		elif mouse_y >= 100 and mouse_y <= 150:
			pygame.mixer.Sound.play(laser3)
		elif mouse_y >= 150 and mouse_y <= 200:
			pygame.mixer.Sound.play(laser4)
		elif mouse_y >= 200 and mouse_y <= 250:
			pygame.mixer.Sound.play(laser5)
		elif mouse_y >= 250 and mouse_y <= 300:
			pygame.mixer.Sound.play(laser6)
		elif mouse_y >= 300 and mouse_y <= 350:
			pygame.mixer.Sound.play(laser7)
		elif mouse_y >= 350 and mouse_y <= 400:
			pygame.mixer.Sound.play(laser8)
			
		#print("Attack!")

stars = []
star_count = 60
star_frames = 1

for i in range(star_count):
	x = random.randrange(0, display_width)
	y = random.randrange(0, (display_height/2) + (display_height/20))
	stars.append([x, y])
	
def backGround(star_frames, x = display_width, y = display_height):
	road_width = y/4
	moon_sprite = 50
	
	#Grass -> Road -> Water -> Sky
	pygame.draw.rect(gameDisplay, DARKGREEN , (0, (y/2) + (y/8)       , x, (x/4) + (x/8)        ))
	pygame.draw.rect(gameDisplay, DARKYELLOW, (0, ((y/4)*3) - (y/20)  , x, road_width           ))
	pygame.draw.rect(gameDisplay, BLUE      , (0, ((y/2)+(y/8))-(y/20), x, (y/20)               ))
	pygame.draw.rect(gameDisplay, DARKBLUE  , (0, 0                   , x, ((y/2)+(y/8))-(y/20) ))
	
	for i in range(star_count):
		if i%random.randrange(20, 24) == 0 and star_frames == 1:
			pygame.draw.circle(gameDisplay, YELLOW, stars[i], random.randrange(2, 4))
		else: pygame.draw.circle(gameDisplay, YELLOW, stars[i], 2)
		
	gameDisplay.blit(img_Moon, ((x - moon_sprite) - (x/30), (y - y) +(y/20)))
		
wizard = Wizard(wizard_X, wizard_Y)
speed = 0
jump_height = 64
jump_condition = False
momentum = 0
attack_condition = False

text = pygame.font.Font(None, 20)
soundMixer = pygame.mixer.Channel(0)

gameExit = False
while not(gameExit):
	
	mouseX, mouseY = pygame.mouse.get_pos() 

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
		
		#MOVEMENT + JUMPING
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				speed = wizard.move('left')
			elif event.key == pygame.K_d:
				speed = wizard.move('right')
			elif event.key == pygame.K_w and wizard.y >= wizard_Y:
				jump_condition = True
					
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a and speed < 0:
				momentum = wizard.move('left') / 2
				speed = 0
			elif event.key == pygame.K_d and speed > 0:
				momentum = wizard.move('right') / 2
				speed = 0
			elif event.key == pygame.K_w:
				jump_condition = False
				
		#ATTACK
		if event.type == pygame.MOUSEBUTTONDOWN:
			if wizard.current_direction == 'right' and mouseX > wizard.x:
				attack_condition = True

			elif wizard.current_direction == 'left' and mouseX < wizard.x:
				attack_condition = True
				
		if event.type == pygame.MOUSEBUTTONUP:
			attack_condition = False
				
		if attack_condition == True:
			wizard.attack(mouseX, mouseY)

			
	gameDisplay.fill(GREY)
	backGround(star_frames)
	
	star_frames += 1
	if star_frames >= 16:
		star_frames = 1
	
	##END OF MAP
	if wizard.x >= (display_width) and speed >= 0:
		wizard.x = 0 - wizard.sprite_width
	elif wizard.x <= (0 - wizard.sprite_width) and speed <= 0:
		wizard.x = display_width
		
	if momentum != 0:
		wizard.x += momentum
		momentum += 1 if momentum < 0 else - 1
	else: wizard.x += speed
	
	jump_condition = wizard.jump(jump_bool = jump_condition, jump_height = jump_height)
	
	gameDisplay.blit(wizard.sprite, (wizard.x, wizard.y))
	
	fpsText = text.render("Fps: {0}".format(fps), True, WHITE)
	songText = text.render("Song: Silent Night" , True, WHITE)
	gameDisplay.blit(fpsText ,(0, 15))
	gameDisplay.blit(songText,(0,  0))
	
	clock.tick(fps)
	pygame.display.update()
	
pygame.quit()
quit()
