from tracemalloc import start
import pygame
from sys import exit
from random import randint as rand
# import time

"""
This is for practice only and is not my property nor is it my original ideas.
This code is copied directly from the video linked below which was published by
the channel Clear Code on YouTube.

Pygame Docs:
https://www.pygame.org/docs/

YouTube video that made it all possible:
https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=1241s&ab_channel=ClearCode
"""
#function to display score on the game screen and end screen
def display_score():
  #display time in seconds
  current_time = int((pygame.time.get_ticks()/1000)- start_time)
  score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
  score_rect = score_surf.get_rect(center = (400, 50))
  screen.blit(score_surf, score_rect)
  return current_time
#function to move enemy objects
def obstacle_movement(list):
  #if our list has items...
  if list:
    #for each item in the list...
    for item in list:
      #the x value of the item moves to the left by 5
      item.x -= 5
      if item.bottom == 300:
        screen.blit(snail,item)
      else: screen.blit(fly,item)
      if item.x <= -100: list.remove(item)
    return list
  else: return []
#function to check for collisions
def collision(player, obst):
  if obst:
    for item in obst:
      if item.colliderect(player): return False
  return True
# #function to create player animation effect
# def player_animation():
  # play walking animation while on the floor
  # play jump animation if player jumps
pygame.init()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
#Display Surface
screen = pygame.display.set_mode((800,400))

#Game active check
game_active = False

#Score Reset Variable
start_time = 0

#Score initializer
score = 0

#setting the font
test_font = pygame.font.Font('font/Pixeltype.ttf',50)

#Intro/Game-over Text
intro_surf = test_font.render('Runner', False, (64,64,64))
intro_rect = intro_surf.get_rect(center = (400,50))
restart_surf = test_font.render("Hit SPACE to start", False, (64,64,64))
restart_rect = restart_surf.get_rect(center = (400,300))

#(Regular) Setting Surface
sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

#Fly
fly = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
# fly_rect = fly.get_rect(bottomleft = (800,150))

#Snail
snail = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail.get_rect(bottomleft = (800,300))
#List of snail/fly-objects to call and delete
obst_rect_list = []

#Player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

player_rect = player_walk[player_index].get_rect(midbottom = (80,300))
player_grav = 0

#Player on Game-over/Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
#Player Scaled for Game-over/Intro Screen
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(midbottom = (400,250))

#timer (set_timer takes the time interval in ms)
obst_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obst_timer,1500)

#Running the game continuously
while True:
  for event in pygame.event.get():
    #Check for quit condition
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    
    #If the game is running, SPACE or CLICK actions:
    if game_active:
      if event.type == obst_timer:
        if rand(0,2) >= 1:
          obst_rect_list.append(snail.get_rect(bottomleft = (rand(900,1000),300)))
        else:
          obst_rect_list.append(fly.get_rect(bottomleft = (rand(900,1100),200)))
      #Check if player is clicking on sprite to jump
      if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
        if player_rect.collidepoint(event.pos):
          player_grav = -20
      #SPACE to Jump condition check
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and player_rect.bottom == 300:
          player_grav = -20
    #If the game is not running, SPACE and Reset actions:
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #Obstacles Reset
        obst_rect_list = []
        #Game Reset
        game_active = True
        #Score Reset
        start_time = int(pygame.time.get_ticks()/1000)

      

  if game_active:
    
    #Put sky_surface at position (0,0) ontop of screen
    screen.blit(sky_surf,(0,0))
    screen.blit(ground_surf,(0,300))
    #Score
    score = display_score()

    #Obstacle movement
    obst_rect_list = obstacle_movement(obst_rect_list)
    #Player movement
    player_grav += 1
    player_rect.y += player_grav
    #Simulate the ground
    if player_rect.bottom >= 300: player_rect.bottom = 300
    screen.blit(player_walk_1, player_rect)
  
    #Collision
    game_active = collision(player_rect, obst_rect_list)

  #If the game ends...
  else:
    #Game-over/Intro Screen
    screen.fill((94,129,162))
    screen.blit(intro_surf,intro_rect)
    screen.blit(player_stand, player_stand_rect)
    player_rect.midbottom(80,300)
    player_grav = 0
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