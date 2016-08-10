import pygame
import time
import random
import threading

pygame.init()

white = (255,255,255)
black = (0,0,0)

red = (190,1,1)
light_red = (255,5,5)

green = (30,177,76)
light_green = (0,255,0)

blue = (44,3,250)

yellow = (200,210,1)
light_yellow = (255,255,0)

grey = (103,120,126)

display_width = 800
display_height = 600

groundheight = 36

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('JTanks')

#icon = pygame.image.load('apple.png')
#pygame.display.set_icon(icon)

#img = pygame.image.load('untitled.png')
#appleimg = pygame.image.load('apple.png')

clock = pygame.time.Clock()

fps = 15

maintankx = display_width * 0.9
maintanky = display_height * 0.9

tankwidth = 40
tankheight = 20
gunwidth = 5
wheelwidth = 5

smfont = pygame.font.SysFont("comicsansms", 25)
medfont =  pygame.font.SysFont("comicsansms", 50)
larfont =  pygame.font.SysFont("comicsansms", 80)

barrierwidth = 50

def pause():
    paused = True

    message_to_screen("Paused",black,-100,"large")
    message_to_screen("Press C play,Q to quit",black,25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(white)
        clock.tick(15)
def score(score):
    text = smfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])

def gcont():
     control = True

     while control:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(white)
        message_to_screen("Controls", red, -100,"large")
        message_to_screen("Fire: Spacebar", black, -30)
        message_to_screen("Move Turret: Up and Down arrows", black, 10)
        message_to_screen("Move Tank: Left and Right arrows", black, 50)
        message_to_screen("Pause: P", black, 90)


        button("play",150,500,100,50,green,light_green,action="play")
        button("controls",350,500,100,50,yellow,light_yellow,action="controls")
        button("quit",550,500,100,50,red,light_red,action="quit")

        
        pygame.display.update()
        clock.tick(15)
    
def game_intro():
    intro = True

    while intro:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(white)
        message_to_screen("Welcome To JTanks", green, -100,"large")
        message_to_screen("The objective is to shoot and destroy!", black, -30)
        message_to_screen("the enemy tanks", black, 10)
        message_to_screen("The more tanks you destroy,harder the get", black, 50)

        button("play",150,500,100,50,green,light_green,action="play")
        button("controls",350,500,100,50,yellow,light_yellow,action="controls")
        button("quit",550,500,100,50,red,light_red,action="quit")

        
        pygame.display.update()
        clock.tick(15)
        
def game_over(p_health,e_health):
    over = True

    while over:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
        if p_health < 1:
            gameDisplay.fill(white)
            message_to_screen("Game Over", green, -100,"large")
            message_to_screen("You Died!", black, -30)

            button("Play Again",150,500,150,50,green,light_green,action="play")
            button("controls",350,500,100,50,yellow,light_yellow,action="controls")
            button("quit",550,500,100,50,red,light_red,action="quit")

            pygame.display.update()
            clock.tick(5)

        if e_health < 1:
            gameDisplay.fill(white)
            message_to_screen("Congratulations", green, -100,"large")
            message_to_screen("You Won!", black, -30)

            button("Play Again",150,500,150,50,green,light_green,action="play")
            button("controls",350,500,100,50,yellow,light_yellow,action="controls")
            button("quit",550,500,100,50,red,light_red,action="quit")

            pygame.display.update()
            clock.tick(5)
            
def text_objects(text, color, size):
    if size == "small":
        textsurface = smfont.render(text, True, color)
    elif size == "medium":
        textsurface = medfont.render(text, True, color)
    elif size == "large":
        textsurface = larfont.render(text, True, color)
    
    return textsurface, textsurface.get_rect()             #we can return multiple values in python

def text_to_button(msg,color,buttonx,buttony,buttonwidth,buttonheight,size="small"):
    textsurf, textrect = text_objects(msg, color, size)
    textrect.center = (buttonx+(buttonwidth/2),buttony+(buttonheight/2))
    gameDisplay.blit(textsurf, textrect)
    
def message_to_screen(msg, color, y_displace=0, size="small"):
    textsurf, textrect = text_objects(msg, color, size)             #we r wantig to make a function to return the rectnge of the text and the surface of the text
    #screen_text = font.render(msg, True, color)
    #gameDisplay.blit(screen_text, [display_width/2, display_height/2])
    textrect.center =(int(display_width/2), int(display_height/2)+y_displace)
    gameDisplay.blit(textsurf, textrect)

def tank(x,y,turpos):                              #if we only modify x and y then entire tank will move
    x = int(x)
    y = int(y)

    possibleturrets = [(x-27,y-2),(x-26,y-5),(x-25,y-8),(x-23,y-12),(x-20,y-14),(x-18,y-15),(x-15,y-17),(x-13,y-19),(x-15,y-20)]

    pygame.draw.circle(gameDisplay,grey,(x,y),int(tankheight/2))
    pygame.draw.rect(gameDisplay,grey,(x-int(tankwidth/2),y,tankwidth,tankheight))
    pygame.draw.line(gameDisplay,grey,(x,y),possibleturrets[turpos],5)

    startx = 15
    for i in range(4):
        pygame.draw.circle(gameDisplay,grey,(x-startx,y+tankheight),wheelwidth)
        startx -= 10

    return(possibleturrets[turpos])

def enemy_tank(x,y,turpos):                              #if we only modify x and y then entire tank will move
    x = int(x)
    y = int(y)

    possibleturrets = [(x+27,y-2),(x+26,y-5),(x+25,y-8),(x+23,y-12),(x+20,y-14),(x+18,y-15),(x+15,y-17),(x+13,y-19),(x+15,y-20)]

    pygame.draw.circle(gameDisplay,grey,(x,y),int(tankheight/2))
    pygame.draw.rect(gameDisplay,grey,(x-int(tankwidth/2),y,tankwidth,tankheight))
    pygame.draw.line(gameDisplay,grey,(x,y),possibleturrets[turpos],5)

    startx = 15
    for i in range(4):
        pygame.draw.circle(gameDisplay,grey,(x-startx,y+tankheight),wheelwidth)
        startx -= 10

    return(possibleturrets[turpos])


def barrier(width,height):
    pygame.draw.rect(gameDisplay,black,((display_width/2)+width,display_height-height,barrierwidth,height))

def fireshell(xy,tankx,tanky,turpos,power,width,height,barrierwidth,enemytankx,enemytanky):
    fire = True
    damage = 0
    startingshell = list(xy)        #coz xy is a tuple so converting to a list
    
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        pygame.draw.circle(gameDisplay,red,(startingshell[0],startingshell[1]),5)

        startingshell[0] -= (12-turpos)*2
        startingshell[1] += int(((startingshell[0]-xy[0])*0.015/(power/50))**2) - int(turpos+turpos/(12-turpos))

        if startingshell[1] > display_height - groundheight:
            hit_x = int(startingshell[0]*(display_height - groundheight)/startingshell[1])
            hit_y = display_height - groundheight
            explosion(hit_x,hit_y)
            if enemytankx-25 < hit_x < enemytankx+25:
                damage = 15
            elif enemytankx-15 < hit_x < enemytankx+15:
                damage = 20
            elif enemytankx-5 < hit_x < enemytankx+5:
                damage = 25
            fire = False

        check_x1 = startingshell[0] <= display_width/2 + width + barrierwidth
        check_x2 = startingshell[0] >= display_width/2 + width
        check_y1 = startingshell[1] <= display_height
        check_y2 = startingshell[1] >= display_height - height

        #print(check_x1)
        
        if check_x1 and check_x2 and check_y1 and check_y2:
            #print("last shell:",startingshell[0],startingshell[1])
            hit_x = int(startingshell[0])
            hit_y = int(startingshell[1])
            explosion(hit_x,hit_y)
            fire = False
        
        pygame.display.update()
        clock.tick(50)
    return damage

def e_fireshell(xy,tankx,tanky,turpos,power,width,height,barrierwidth,maintankx, maintanky):
    currentpower = 1
    power_found = False
    damage = 0
    
    while not power_found:
        currentpower +=1
        if currentpower > 100:
            power_found = True
        
        startingshell = list(xy)        
        fire = True

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            startingshell[0] += (12-turpos)*2
            startingshell[1] += int(((startingshell[0]-xy[0])*0.015/(currentpower/50))**2) - int(turpos+turpos/(12-turpos))
       
            if startingshell[1] > display_height - groundheight:
                hit_x = int(startingshell[0]*(display_height - groundheight)/startingshell[1])
                hit_y = display_height - groundheight
                if maintankx-15 < hit_x < maintankx+15:
                    power_found = True
                fire = False
            
            check_x1 = startingshell[0] <= display_width/2 + width + barrierwidth
            check_x2 = startingshell[0] >= display_width/2 + width
            check_y1 = startingshell[1] <= display_height
            check_y2 = startingshell[1] >= display_height - height

            #print(check_x1)
            
            if check_x1 and check_x2 and check_y1 and check_y2:
                hit_x = int(startingshell[0])
                hit_y = int(startingshell[1])
                fire = False
            
    startingshell = list(xy)        
    fire = True

    power = random.randrange(int(0.9*currentpower),int(1.1*currentpower))
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                    
        pygame.draw.circle(gameDisplay,red,(startingshell[0],startingshell[1]),5)

        
        startingshell[0] += (12-turpos)*2
        startingshell[1] += int(((startingshell[0]-xy[0])*0.015/(power/50))**2) - int(turpos+turpos/(12-turpos))

        if startingshell[1] > display_height - groundheight:
            hit_x = int(startingshell[0]*(display_height - groundheight)/startingshell[1])
            hit_y = display_height - groundheight
            explosion(hit_x,hit_y)
            if maintankx-25 < hit_x < maintankx+25:
                    damage = 15
                    power_found = True
            elif maintankx-15 < hit_x < maintankx+15:
                damage = 20
                power_found = True
            elif maintankx-5 < hit_x < maintankx+5:
                damage = 25
                power_found = True
            fire = False

        check_x1 = startingshell[0] <= display_width/2 + width + barrierwidth
        check_x2 = startingshell[0] >= display_width/2 + width
        check_y1 = startingshell[1] <= display_height
        check_y2 = startingshell[1] >= display_height - height
        
        if check_x1 and check_x2 and check_y1 and check_y2:
            hit_x = int(startingshell[0])
            hit_y = int(startingshell[1])
            explosion(hit_x,hit_y)
            fire = False
        
        pygame.display.update()
        clock.tick(50)
    return damage

def explosion(hit_x,hit_y):

    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        colors = [light_red, red, green, yellow]
        magnitude = 1
        while magnitude <= 50:
            pygame.draw.circle(gameDisplay, colors[random.randrange(0,4)],(hit_x + random.randrange(-1*magnitude,magnitude),hit_y + random.randrange(-1*magnitude,magnitude)),random.randrange(0,4))
            pygame.display.update()
            clock.tick(90)
            magnitude +=1

        explode = False
        

def power(level):
    text = smfont.render("Power Level: "+str(level),True,black)
    gameDisplay.blit(text, [display_width*0.6,0])

def button(text,x,y,width,height,color,active_color,action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+width > cur[0] > x and y+height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                gcont()
            if action == "play":
                gameLoop()
    else:
        pygame.draw.rect(gameDisplay, color, (x,y,width,height))

    text_to_button(text,black,x,y,width,height)

def healthbar(ptank,etank):
    if ptank > 75:
        p_color = green
    elif ptank >25:
        p_color = yellow
    else:
        p_color = red

    if etank > 75:
        e_color = green
    elif etank >25:
        e_color = yellow
    else:
        e_color = red

    pygame.draw.rect(gameDisplay,p_color,(680,25,ptank,20))
    pygame.draw.rect(gameDisplay,black,(680,25,ptank,20),2)

    pygame.draw.rect(gameDisplay,e_color,(20,25,etank,20))
    pygame.draw.rect(gameDisplay,black,(20,25,etank,20),2)

    pygame.display.update()
    
def gameLoop():

    maintankx = display_width * 0.9
    maintanky = display_height * 0.9
    tankmove = 0

    enemytankx = display_width * 0.1
    enemytanky = display_height * 0.9
    
    currentturpos = 0
    changetur = 0
    
    gameExit = False
    gameOver = False
    fps = 15

    width =  random.randint(-0.3*(display_width/2),0.3*(display_width/2))
    height = random.randint(0.3*display_height,0.6*display_height)

    fire_power = 80
    power_change = 0

    p_health = 100
    e_health =100

    p_damage =0
    e_damage =0
    while not gameExit:
        
        if gameOver == True:
            message_to_screen("Game Over", red, -50, "large")
            message_to_screen("press c to play again or q to quit", black, 50, "medium")
            pygame.display.update()
            
##        while gameOver == True:
##            for event in pygame.event.get():
##                if event.type == pygame.QUIT:
##                    gameExit = True
##                    gameOver = False
##                if event.type == pygame.KEYDOWN:
##                    if event.key == pygame.K_q:
##                        gameExit = True
##                        gameOver = False
##                    elif event.key == pygame.K_c:
##                        gameLoop()
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    tankmove = -5
                    
                elif event.key == pygame.K_RIGHT:
                    tankmove = 5
                    
                elif event.key == pygame.K_UP:
                     changetur = 1
                    
                elif event.key == pygame.K_DOWN:
                    changetur = -1
                
                elif event.key == pygame.K_p:
                    pause()
                    
                elif event.key == pygame.K_SPACE:
                    e_damage = fireshell(gun, maintankx, maintanky, currentturpos,fire_power,width,height,barrierwidth,enemytankx,enemytanky)
                    e_health -= e_damage

                    possible_move = ['f','r']
                    moveindex = random.randrange(0,2)

                    for x in range(random.randrange(0,10)):
                        if display_width*0.3 > enemytankx:
                            if possible_move[moveindex] == 'f':
                                enemytankx +=5
                        if enemytankx > display_width * 0.03:       
                            if possible_move[moveindex] == 'r':
                                enemytankx -=5

                            gameDisplay.fill(white)
                            gun = tank(maintankx,maintanky,currentturpos)
                            enemy_gun = enemy_tank(enemytankx,enemytanky,8)
                            power(fire_power)        #function to display fire power

                            healthbar(p_health,e_health)

                            barrier(width,height)

                            gameDisplay.fill(green,rect=[0, display_height-groundheight, display_width, groundheight])
                            pygame.display.update()
                            clock.tick(fps)
                                                
                    p_damage = e_fireshell(enemy_gun, enemytankx, enemytanky,8,fire_power,width,height,barrierwidth,maintankx, maintanky)
                    p_health -= p_damage
                     
                elif event.key == pygame.K_x:
                    power_change = -1
                elif event.key == pygame.K_z:
                    power_change = 1
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankmove = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                     changetur = 0
                if event.key == pygame.K_x or event.key == pygame.K_z:
                    power_change = 0
                    
        maintankx += tankmove
        currentturpos += changetur
        fire_power += power_change
        
        if maintankx >= display_width:
            maintankx = display_width
        
        if(0 > currentturpos):
            currentturpos = 0
        elif(currentturpos > 8):
            currentturpos = 8

        if(maintankx-(tankwidth/2) <= (display_width/2)+width+barrierwidth):
            maintankx += 5

        if fire_power >= 100:
            fire_power = 100   
        elif fire_power <= 1:
            fire_power = 1

        if p_health < 1:
            p_health = 0
        if e_health < 1:
            e_health = 0
        if p_health<1 or e_health<1:
            game_over(p_health,e_health)
            
        gameDisplay.fill(white)
        gun = tank(maintankx,maintanky,currentturpos)
        enemy_gun = enemy_tank(enemytankx,enemytanky,8)
        power(fire_power)        #function to display fire power

        healthbar(p_health,e_health)
        
        barrier(width,height)

        gameDisplay.fill(green,rect=[0, display_height-groundheight, display_width, groundheight])
        pygame.display.update()
        clock.tick(fps)
        

    pygame.quit()
    quit()

game_intro()
gameLoop()





    
