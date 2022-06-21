import pygame, os
from sys import exit
from random import randint, choice

""" 
Added a multi jump (similar to flappy bird but does not gain height)
Changed spawn rate of enemies 
Changed hitboxes 
Changed player jump height and enemy travel speed
Changed all assests, including sfx and music
"""

#This class contains everything related to the player controlled character (sasuke)
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		#this loads the sasuke character sprites and stores/sets character values
		player_walk_1 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "player_walk_1.png")), (64, 80)).convert_alpha()
		player_walk_2 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "player_walk_2.png")), (64, 80)).convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "jump.png")), (64, 80)).convert_alpha()

		self.image = self.player_walk[self.player_index]
		#This sets the bottom of the character and the "gravity" at the bottom
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		#This loads and changed the volume of the jump sound
		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.9)

	#Checks to see if the player is at the required height to jump and sets the height of the jump
	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 200:
			self.gravity = -15
			self.jump_sound.play()

	#If player is not at it's determined bottom value, the character will fall until reaching that value
	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	"""
	 if player is not at the bottom value, the jump sprite will be displayed instead of the walk sprite
	and also alternates walking sprites to make it look animated
	"""
	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	#one function to call athe other functions at once
	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

#Class containing everything involving enermy characters (naruto clones)
class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		#Loads the sky and floor naruto sprites and the height they will eventually spawn
		if type == 'naruto_sky':
			naruto_sky_1 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "naruto_sky1.png")), (64, 80)).convert_alpha()
			naruto_sky_2 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "naruto_sky2.png")), (64, 80)).convert_alpha()
			self.frames = [naruto_sky_1,naruto_sky_2]
			y_pos = 210
		else:
			naruto_floor_1 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "naruto_floor1.png")), (64, 80)).convert_alpha()
			naruto_floor_2 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "naruto_floor2.png")), (64, 80)).convert_alpha()
			self.frames = [naruto_floor_1,naruto_floor_2]
			y_pos  = 300

		#this assures that the enemies spawn at varying intervals
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	#This changes the sprite of the enenmy to make it look like they are running
	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	#this controls the speed of the enemies 
	def update(self):
		self.animation_state()
		self.rect.x -= 7
		self.destroy()

	#deletes an enemy sprite after passing the indicted x value 
	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

#This calculates the score based on how long the player has survived in the game then displays it
def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(44,44,44))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

#This function chooses either athe gorund naruto for the floor or sky naruto for the sky then displays them
def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= 10

			if obstacle_rect.bottom == 300: screen.blit(naruto_floor_surf,obstacle_rect)
			else: screen.blit(naruto_sky_surf,obstacle_rect)

		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

		return obstacle_list
	else: return []

#This checks if the player hit aaan enemy character
def collisions(player,obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect): return False
	return True

#This function continues the game as long as the player has not hit an enemy
def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True


#This creates the screen and the title
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Final Valley Runner')
#This creates a clock that keeps trackof time and allows timed events
clock = pygame.time.Clock()
#This loads a font document allowing to use non-defautl fonts 
test_font = pygame.font.Font(os.path.join("font", "Pixeltype.ttf"), 50)
#beginning variables before the ame starts
game_active = False
start_time = 0
score = 0
#Adds naruto music to the game and loops it when the song ends
bg_music = pygame.mixer.Sound('audio/music1.mp3')
bg_music.play(loops = -1)

#Groups 
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

#Sets the background to a saved image
sky_surface = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "Sky.png")), (800, 450)).convert()


#This creates/displays the character sprite for the ground naruto 
naruto_floor_frame_1 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "naruto_floor1.png")), (55, 80)).convert_alpha()
naruto_floor_frame_2 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "naruto_floor2.png")), (55, 80)).convert_alpha()
naruto_floor_frames = [naruto_floor_frame_1, naruto_floor_frame_2]
naruto_floor_frame_index = 0
naruto_floor_surf = naruto_floor_frames[naruto_floor_frame_index]

#This creates/displays the character sprite for the flying naurto 
naruto_sky_frame1 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "naruto_sky1.png")), (55, 80)).convert_alpha()
naruto_sky_frame2 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "naruto_sky2.png")), (55, 80)).convert_alpha()
naruto_sky_frames = [naruto_sky_frame1, naruto_sky_frame2]
naruto_sky_frame_index = 0
naruto_sky_surf = naruto_sky_frames[naruto_sky_frame_index]

obstacle_rect_list = []

#This creates/displays the character sprite for sasuke that can be used with the physics/gravity 
player_walk_1 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "player_walk_1.png")), (55, 80)).convert_alpha()
player_walk_2 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "player_walk_2.png")), (55, 80)).convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "jump.png")), (55, 80)).convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#This creates the intro screen seen when first opening the game
player_stand = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "player_stand.png")), (90, 106)).convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))
game_name = test_font.render('Final Valley Runner',False,(0,0,0))
game_name_rect = game_name.get_rect(center = (400,80))
game_message = test_font.render('Press space to run',False,(0,0,0))
game_message_rect = game_message.get_rect(center = (400,330))

#This times the frequency of enemy spawning 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1000)
naruto_floor_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(naruto_floor_animation_timer,400)
naruto_sky_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(naruto_sky_animation_timer,150)

while True:
	for event in pygame.event.get():
     #This closes the game when the window is closed
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if game_active:
			#Checks if spacebar is clicked and jumps if at right position while the game is active
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
					player_gravity = -15
		else:
      #If the game is not active, this means the player is at the start/end screen and a spacebar click will start another game
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True				
				start_time = int(pygame.time.get_ticks() / 1000)

		if game_active:
      #While the game is active, a corresponding enemy sprite is chosen and spawned in the window at the set time interval
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['naruto_sky','naruto_floor','naruto_floor','naruto_floor'])))

			if event.type == naruto_floor_animation_timer:
				if naruto_floor_frame_index == 0: naruto_floor_frame_index = 1
				else: naruto_floor_frame_index = 0
				naruto_floor_surf = naruto_floor_frames[naruto_floor_frame_index] 

			if event.type == naruto_sky_animation_timer:
				if naruto_sky_frame_index == 0: naruto_sky_frame_index = 1
				else: naruto_sky_frame_index = 0
				naruto_sky_surf = naruto_sky_frames[naruto_sky_frame_index] 

	"""
 	When the game is active, the background is sset, and the score and player models are constantly loaded to simulate 
 	animation/movement, while also checking to assure that the player hasn't hit an enemy
   	"""
	if game_active:
		screen.blit(sky_surface,(0,0))
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		#The game will be active as long as the character ahs not hit an enemy
		game_active = collision_sprite()
		
	else:
	#This is the end screen when you lose, similar to the start screen but displayed your score at the bottom
		screen.fill((30,70,235))
		screen.blit(player_stand,player_stand_rect)
		obstacle_rect_list.clear()
		player_rect.midbottom = (80,300)
		player_gravity = 0

		score_message = test_font.render(f'Your score: {score}',False,(0,0,0))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)
