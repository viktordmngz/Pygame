from tracemalloc import start
import pygame
from sys import exit
from random import randint as rand, randrange as randr, choice


"""
This is for practice only and is not my property nor is it my original ideas.
This code is copied directly from the video linked below which was published by
the channel Clear Code on YouTube.

Pygame Docs:
https://www.pygame.org/docs/

YouTube video that made it all possible:
https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=1241s&ab_channel=ClearCode
"""

#Player Class
class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    #PLAYER
    player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
    player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
    self.player_walk = [player_walk_1,player_walk_2]
    self.player_index = 0
    self.player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()
    self.image = self.player_walk[self.player_index]
    self.rect = self.image.get_rect(midbottom = (80,300))

    #Gravity
    self.grav = 0
    #Jump Sound
    self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
    self.jump_sound.set_volume(0.1)

  #Player Input
  def player_input(self):
    keys = pygame.key.get_pressed()
    #JUMP
    if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
      self.jump_sound.play()
      self.grav = -20
  
  #Player Animation
  def player_anim(self):
    if self.rect.bottom < 300:
      self.image = self.player_jump
    else:
      self.player_index += 0.1
      if self.player_index >= len(self.player_walk): self.player_index = 0
      self.image = self.player_walk[int(self.player_index)]

  #Passive Gravity
  def apply_grav(self):
    self.grav += 1
    self.rect.y += self.grav
    if self.rect.bottom >= 300: self.rect.bottom = 300
    
  def update(self):
    self.player_input()
    self.apply_grav()
    self.player_anim()

#Obstacle Class
class Obstacle(pygame.sprite.Sprite):
  def __init__(self,type):
    super().__init__()
    if type == 'fly':
      fly1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
      fly2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
      self.frames = [fly1,fly2]
      y_pos = 200
      #Different Speed for FLIES
      self.x_speed = randr(6,10,1)
    else:
      snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
      snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
      self.frames = [snail1,snail2]
      y_pos = 300
      #Different Speed for SNAILS
      self.x_speed = 5
    
    self.animation_index = 0
    self.image = self.frames[self.animation_index]
    self.rect = self.image.get_rect(midbottom = (rand(900,1100),y_pos))

  #Obstacle Animation
  def obst_anim(self):
    self.animation_index += 0.1
    if self.animation_index >= len(self.frames): self.animation_index = 0
    self.image = self.frames[int(self.animation_index)]

  def update(self):
    self.obst_anim()
    self.rect.x -= self.x_speed
    self.destroy()

  #Remove sprites that go off-screen
  def destroy(self):
    if self.rect.x <= -100:
      self.kill()
      
#function to display score on screen
def display_score():
  #display time in seconds
  current_time = int((pygame.time.get_ticks()/1000)- start_time)
  score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
  score_rect = score_surf.get_rect(center = (400, 50))
  screen.blit(score_surf, score_rect)
  return current_time

#Sprite Collision
def collision():
  if pygame.sprite.spritecollide(player.sprite, obst_group, False):
    obst_group.empty()
    return False
  else: return True

#GAME INTIALIZERS
#------------------
pygame.init()
#DISPLAY
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
#GAME ACTIVE
game_active = False
#TIME (used for restarts)
start_time = 0
#SCORE
score = 0
#BG MUSIC
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.05)
bg_music.play(loops = -1)

#FONT
test_font = pygame.font.Font('font/Pixeltype.ttf',50)

#--------------------
#OBJECTS and TEXTS
#--------------------

#INTRO/GAME-OVER TEXT
intro_surf = test_font.render('Runner', False, (64,64,64))
intro_rect = intro_surf.get_rect(center = (400,50))
restart_surf = test_font.render("Hit SPACE to start", False, (64,64,64))
restart_rect = restart_surf.get_rect(center = (400,300))

#BACKGROUND SURFACES
sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

#Obstacle Sprite Group
obst_group = pygame.sprite.Group()

#Player Sprite Group
player = pygame.sprite.GroupSingle()
player.add(Player())

#Player on Game-over/Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
#Player Scaled for Game-over/Intro Screen
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(midbottom = (400,250))

#TIMERS
#timer for obstacle population
obst_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obst_timer,randr(1300,1500,100))

#------
#GAME
#------

#Running the game continuously
while True:
  for event in pygame.event.get():
    #Check for quit condition
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    
    #Obstacle Sprites being made at interval time (random choice for which type)
    if game_active:
      if event.type == obst_timer:
        obst_group.add(Obstacle(choice(['fly','',''])))

    #If the game is not running, SPACE --> Reset actions:
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #Game Reset
        game_active = True
        #************************************************#
        #NOTE: Player starts each round with a JUMP. Fix?
        #************************************************#
        #Score Reset
        start_time = int(pygame.time.get_ticks()/1000)

      
  #If the game is running...
  if game_active:    
    #BACKGROUND SURFACES
    screen.blit(sky_surf,(0,0))
    screen.blit(ground_surf,(0,300))
    #SCORE
    score = display_score()

    #Obstacle Sprites
    obst_group.draw(screen)
    obst_group.update()

    #Player Sprites    
    player.draw(screen)
    player.update()
    
    #Check for collisions
    game_active = collision()

  #If the game ends...
  else:
    #Game-over/Intro Screen
    screen.fill((94,129,162))
    screen.blit(intro_surf,intro_rect)
    screen.blit(player_stand, player_stand_rect)

    #If you played at least once...
    #Score at the end of game
    score_message = test_font.render(f"Your Score: {score}", False, (64,64,64))
    score_rect = score_message.get_rect(center = (400,300))
    
    #Condition check
    if score == 0:
      #Show restart message
      screen.blit(restart_surf,restart_rect)
    else:
      #Show score
      screen.blit(score_message, score_rect)

  pygame.display.update()
  #FPS
  clock.tick(60)
