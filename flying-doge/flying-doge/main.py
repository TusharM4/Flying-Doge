#Tushar and Edwin
#Nov 25,2021
#Flyingdoge.py
#Flying doge game code

#Basic pygame imports
import sys
import random
import pygame
import time
import pandas_datareader as web
import datetime as dt

#Functions for different parts of the game

#Moving floor to look like the screen is moving
def movingfloor():
  screen.blit(bgfloor,(xfloorposition,825))
  screen.blit(bgfloor,(xfloorposition + 576,825))

#Creates the pipes and their random location
def spawnpipes():
  randomposition = random.choice(pipeheight)
  bottompipe = pipearea.get_rect(midtop = (775,randomposition))
  toppipe = pipearea.get_rect(midbottom = (775,randomposition - 350))
  return bottompipe,toppipe

#Moves the pipes toward the doge
def movespipes(pipes):
  for pipe in pipes:
    pipe.centerx -= 6
  pipesonscreen = [pipe for pipe in pipes if pipe.right > -50]
  return pipesonscreen

#Outputs the pipes to the screen
def outputspipes(pipes):
  for pipe in pipes:
    if pipe.bottom >= 924:
      screen.blit(pipearea,pipe)
    else:
      #Flips the top pipes 
      flipedpipe = pygame.transform.flip(pipearea,False,True)
      screen.blit(flipedpipe,pipe)

#Checks for collisions between the character and the pipes or the floor/ceiling
def collisions(pipes):
  for pipe in pipes:
    if dogebox.colliderect(pipe):
      return False

  if dogebox.top <= 0 or dogebox.bottom >= 825:
    return False

  #If there are no collisions the game continues
  return True

#Rotates the character when moving up or down
def rotatesdoge(doge):
  rotateddoge = pygame.transform.rotozoom(doge,-dogemovement * 3,1)
  return rotateddoge

#Outputs the score and highscore onto the screen
def scoreout(gamestate):
  if gamestate == 'GAMELOOP':
    #Score
    scoreoutput = font.render(str(int(score)),True,(white))
    scorebox = scoreoutput.get_rect(center = (288,100))
    screen.blit(scoreoutput,scorebox)

  if gamestate == 'GAMEOVER':
    #Score Output
    scoreoutput = font.render(f'Score: {int(score)}' ,True,(white))
    scorebox = scoreoutput.get_rect(center = (288,100))
    screen.blit(scoreoutput,scorebox)
    #Highscore Output
    highscoreoutput = font.render(f'High score: {int(highscore)}',True,(white))
    highscorebox = highscoreoutput.get_rect(center = (288,790))
    screen.blit(highscoreoutput,highscorebox)

#Updates the highscore once a higher score is gotten than the last
def updateshighscore(score, highscore):
  if score > highscore:
    highscore = score  
  return highscore

#Calculates the score when the character passes the pipes
def scorecalculater():
  global score, scoreon
  if pipelist:
    for pipe in pipelist:
      if 95 < pipe.centerx < 105 and scoreon:
        point.play()
        point.set_volume(0.05)
        score += 1
        scoreon = False
      if pipe.centerx < 0:
        scoreon = True

#Calculates the value of dogecoin collected using the live market price and score collected during the game
def dogecoincalculator():
  #Code from https://stackoverflow.com/questions/44012335/python-pandas-datareader-isnt-working
  start = dt.datetime(2022,1,1)
  end = dt.datetime.now()
  dogecoin = web.DataReader('DOGE-CAD', 'yahoo', start, end)
  price = float(dogecoin['Close'][-1])

  dollars = round(int(score) * float(price),2)

  dollarsout = endfont.render(f'$ {float(dollars)}' ,True,(red))
  dollarsbox = dollarsout.get_rect(center = (265,340))
  screen.blit(dollarsout,dollarsbox)

#pygame.init() initialises all imported pygame modules and the total number of successful and failed inits will be returned as a tuple 
#This checks for errors encountered by checking the second output as this is where failed modules are added
#An example output would be (5, 0) with all modules successfully initialised
check_errors = pygame.init()

#If there is more than 1 failed module(the 2nd number would be more than 1), it ends the system
if check_errors[1] > 0:
  print('Had module errors while initialising game, goodbye:(')
  sys.exit(1)
else:
  print('Game successfully initialised')

#Initialises the game window
screen = pygame.display.set_mode((576,924))
pygame.display.set_caption('Flying Doge By Tushar')

#Controls the FPS using the built in functions(the variable controls how many frames are shown per second)
fps = pygame.time.Clock()

#Font of text
font = pygame.font.SysFont('comicsansms', 40)
endfont = pygame.font.SysFont('comicsansms', 90)

#Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 102)

#Game Loop Variables
global scoreon
gravity = 0.22
dogemovement = 0
gameon = True
score = 0
highscore = 0
scoreon = True
xfloorposition = 0
speed = 0
gamespeed = 0

#Sounds
gamemusic = pygame.mixer.Sound('sound/chillmain.wav')
death = pygame.mixer.Sound('sound/dead.wav')
point = pygame.mixer.Sound('sound/point.wav')
lobby = pygame.mixer.Sound('sound/lobby.mp3')

#Loading images to put on the screen
background = pygame.transform.scale2x(pygame.image.load('images/background-night.png').convert())
bgfloor = pygame.transform.scale2x(pygame.image.load('images/base.png').convert())
dogeimage = pygame.transform.scale2x(pygame.image.load('images/Nyandoge.gif').convert_alpha())
pipearea = pygame.transform.scale2x(pygame.image.load('images/pipe-green.png'))
gameoverscreen = pygame.transform.scale2x(pygame.image.load('images/start-message.png').convert_alpha())
startscreen = pygame.transform.scale2x(pygame.image.load('images/Startscreen.png').convert())
start = pygame.image.load("images/start.png").convert()
controls = pygame.image.load("images/controls.png").convert()
back = pygame.image.load("images/back.jpeg").convert()
endscreen = pygame.transform.scale2x(pygame.image.load('images/endscreen.png').convert())

#Rectangles around images with co-ordinates for  blitting on screen
dogebox = dogeimage.get_rect(center = (100,462))
gameoverbox = gameoverscreen.get_rect(center = (288,430))
startbox = start.get_rect(topleft = (150,362))
controlsbox = controls.get_rect(topleft = (100,540))

#Pipe variables
pipelist = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1300)
pipeheight = [400,600,800]

#Loop to choose difficulty
#The speed determines the fps
while(1):
  try:
    starttitle = font.render(f'Look at the Console!' ,True,(white))
    starttitlebox = starttitle.get_rect(center = (282,400))
    screen.blit(starttitle,starttitlebox)
    pygame.display.update()

    print('What difficulty would you like to play on?\n1 = Easy\n2 = Medium\n3 = Hard\n4 = Very Hard\nEnter an integer(eg. 3)')
    difficulty = int(input())
    if difficulty == 1:
      gamespeed = 80
      speed = gamespeed
      break
    elif difficulty == 2:
      gamespeed = 100
      speed = gamespeed
      break
    elif difficulty == 3:
      gamespeed = 120
      speed = gamespeed
      break
    elif difficulty == 4:
      gamespeed = 140
      speed = gamespeed
      break
  except ValueError:
    print('\nThere was an invalid input, please try again.')

#Loop for the starting menu
running = True
while running == True:

    #Plays lobby music
    lobby.play()
    lobby.set_volume(0.05)

    #Blits the images and text on screen
    screen.blit(startscreen,(0,0))

    starttitle = endfont.render(f'Flying Doge' ,True,(white))
    starttitlebox = starttitle.get_rect(center = (282,150))
    screen.blit(starttitle,starttitlebox)
  
    screen.blit(start,startbox)
    screen.blit(controls,controlsbox)

    pygame.display.update()

    #Gets input from user
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
          #Sets the x and y postions of the mouse click
          x, y = event.pos

          #If the start button is pressed the loop is exitted and the game begins
          if startbox.collidepoint(x,y):
            running = False

          #If the Controls button is pressed all the text and images are outputted
          elif controlsbox.collidepoint(x,y):

            screen.blit(startscreen,(0,0))

            controlstext = endfont.render(f'Controls' ,True,(black))
            controlstextbox = controlstext.get_rect(center = (282,150))
            screen.blit(controlstext,controlstextbox)
            
            controlstext = endfont.render(f'Goal' ,True,(black))
            controlstextbox = controlstext.get_rect(center = (282,380))
            screen.blit(controlstext,controlstextbox)

            controlstext = font.render(f'W or Space Key to move up' ,True,(white))
            controlstextbox = controlstext.get_rect(center = (282,250))
            screen.blit(controlstext,controlstextbox)

            controlstext = font.render(f'Fly through all the pipes' ,True,(white))
            controlstextbox = controlstext.get_rect(center = (282,485))
            screen.blit(controlstext,controlstextbox)

            controlstext = font.render(f'and collect the dogecoin' ,True,(white))
            controlstextbox = controlstext.get_rect(center = (282,525))
            screen.blit(controlstext,controlstextbox)

            #Code to return back to menu
            backbutton = True
            while backbutton == True:
              backbox = back.get_rect(topleft = (10,5))
              screen.blit(back, (10,5))
              pygame.display.update()
              for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                  #Sets the x and y postions of the mouse click
                  x, y = event.pos

                  #If the back button is pressed the user returns to the menu
                  if backbox.collidepoint(x,y):
                    backbutton = False

#Stops lobby music and plays main game music                          
lobby.stop()
gamemusic.play()
gamemusic.set_volume(0.25)

#Main Game loop
while True:
  #Gets input from user
  for event in pygame.event.get():
    #If the X is pressed game the game ends
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
      
    if event.type == pygame.KEYDOWN:
      #If w or space is pressed, the doge goes up
      if event.key == ord('w') or event.key == pygame.K_SPACE and gameon:
        dogemovement = 0
        dogemovement -= 7
      #If w is pressed when the start message screen is up, the game begins
      if event.key == ord('w') and gameon == False:
        gameon = True
        pipelist.clear()
        dogebox.center = (100,462)
        dogemovement = 0
        score = 0
      #If space is pressed when the start message screen is up, the game begins
      if event.key == pygame.K_SPACE and gameon == False:
        gameon = True
        pipelist.clear()
        dogebox.center = (100,462)
        dogemovement = 0
        score = 0

    #Spawns pipe if nessasary
    if event.type == SPAWNPIPE:
      pipelist.extend(spawnpipes())

  screen.blit(background,(0,0))

  #If the game is running(the player is alive)
  if gameon:

    end = True
    #Character movement and more
    dogemovement += gravity
    rotateddogeout = rotatesdoge(dogeimage)
    dogebox.centery += dogemovement
    screen.blit(rotateddogeout,dogebox)
    gameon = collisions(pipelist)

    #Outputs and moves pipes
    pipelist = movespipes(pipelist)
    outputspipes(pipelist)
    
    #Calculates and outputs Score
    scorecalculater()
    scoreout('GAMELOOP')
    
    #If the score is between 5 and 10 slowmode is enabled
    if score >= 5 and score < 10:
      background = pygame.image.load('images/background-day.png').convert()
      background = pygame.transform.scale2x(background)
      slow = font.render(f'*Slow Mode Enabled*' ,True,(white))
      slowbox = slow.get_rect(center = (295,150))
      screen.blit(slow,slowbox)
      speed = gamespeed - 20
        
    #If the score is between 15 and 20 speed mode is enabled
    elif score >= 15 and score < 20:
      background = pygame.image.load('images/background-day.png').convert()
      background = pygame.transform.scale2x(background)
      slow = font.render(f'*Speed Mode Enabled*' ,True,(white))
      slowbox = slow.get_rect(center = (295,150))
      screen.blit(slow,slowbox)
      speed = gamespeed + 20

    #If the score is between 25 and 30 slowmode is enabled
    elif score >= 25 and score < 30:
      background = pygame.image.load('images/background-day.png').convert()
      background = pygame.transform.scale2x(background)
      slow = font.render(f'*Slow Mode Enabled*' ,True,(white))
      slowbox = slow.get_rect(center = (295,150))
      screen.blit(slow,slowbox)
      speed = gamespeed - 20
        
    #If the score is between 35 and 40 speed mode is enabled
    elif score >= 35 and score < 40:
      background = pygame.image.load('images/background-day.png').convert()
      background = pygame.transform.scale2x(background)
      slow = font.render(f'*Speed Mode Enabled*' ,True,(white))
      slowbox = slow.get_rect(center = (295,150))
      screen.blit(slow,slowbox)
      speed = gamespeed + 20

    #After that the game returns to normal  
    elif score >= 10 or score >= 20 or score >= 30 or score >= 40 :
      background = pygame.image.load('images/background-night.png').convert()
      background = pygame.transform.scale2x(background)
      speed = gamespeed

  #If the player is dead the game over screen is outputted with the dogecoin price and the end music is played
  else:
    while end == True:
      #Music is played
      gamemusic.stop()
      death.play()
      death.set_volume(0.25)
      gamemusic.play()

      #Game end screen and the dogecoin price is found and outputted
      screen.blit(endscreen, (0,0))
      dogecoincalculator()
      pygame.display.update()

      #1 Second delay to see the end screen
      time.sleep(1)

      #Game is reset
      background = pygame.image.load('images/background-night.png').convert()
      background = pygame.transform.scale2x(background)
      end = False

    #Score and start screen is outputted 
    screen.blit(gameoverscreen,gameoverbox)
    highscore = updateshighscore(score,highscore)
    scoreout('GAMEOVER')
    #Fps is reset
    speed = gamespeed

  #Floor movement
  xfloorposition -= 1
  movingfloor()
  if xfloorposition <= -576:
    xfloorposition = 0
    
  #Updates the display at the chosen frames per second(depends on the difficulty chosen at the start)
  pygame.display.update()
  fps.tick(speed)   