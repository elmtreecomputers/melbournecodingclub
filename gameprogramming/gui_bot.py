import pygame
from comms import gameClient as gc
import random

pTeam = ''
pColor = (0,0,0)


pTeam = 'bot'
pColor = (10, 255, 10)
#https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-tutorial-movement/
pygame.init()

screen_w = 500
screen_h = 500
win = pygame.display.set_mode((screen_h, screen_w))
pygame.display.set_caption("Tank Battle: Team " + pTeam)

x = screen_w//2
y = screen_h//2


tank_width = 40
tank_height = 60
vel = 5

run = True

gc.makeConnection()

lastX = x
lastY = y

direction_list = ["east", "south east", "south", "south west", "west", "north west", "north", "north east"]
dir = 0 
direction = direction_list[0]

index = 0
steps = 0
change_after = 10

steps_before_stop = 100


while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    if steps_before_stop <20:
        vel = 0
    if steps_before_stop == 0:
        vel = 5
        steps_before_stop = 100

    if direction == direction_list[0]:
        x += vel
        
    elif direction == direction_list[1]:
        x += vel
        y += vel

    elif direction == direction_list[2]:
        y += vel

    elif direction == direction_list[3]:
        y += vel
        x -= vel
    
    if direction == direction_list[4]:
        x -= vel
        
    elif direction == direction_list[5]:
        x -= vel
        y -= vel

    elif direction == direction_list[6]:
        y -= vel

    elif direction == direction_list[7]:
        y -= vel
        x += vel

    steps_before_stop-=1

    steps+=1
    print(steps, " " , change_after)
    index = direction_list.index(direction)
    print("Current index: ", index)
    
    if x< 0 or x > screen_w-tank_width or y > screen_h-tank_height or y < 0: 
        if(x<0):
            x = 1
        if(x>screen_w-tank_width):
            x = screen_w-tank_width-1
        if(y>screen_h-tank_height):
            y = screen_h-tank_height-1
        if(y<0):
            y = 1
        new_dir = direction_list[:index]+direction_list[index+1:]
        index = random.randint(0, len(new_dir)-1) 
        #index = random.randint(-2,2)

        change_after = random.randint(1, 4) * 6
        direction = new_dir[index]
        steps = 0
    
    elif steps>change_after:
    
        #new_dir = direction_list[:index]+direction_list[index+1:]
        #index = random.randint(0, len(new_dir)-1) 
        index = random.randint(index-1,index+1)
        if index>len(direction_list)-1:
            index = index - len(direction_list)
        change_after = random.randint(1, 4) * 6
        direction = direction_list[index]
        steps = 0


    print("x:" + str(x) + "y:" +  str(y) + " index:" +str(index) + " dir:" + direction)


    win.fill((0, 0, 0))  # Fills the screen with black
    pygame.draw.rect(win, pColor, (x, y, tank_width, tank_height))
    tank = gc.getTank()

    col = (245,10,10)
    if tank['team']=='blue':
        col = (10,10,245)
        pygame.draw.rect(win, col, (tank['x'], tank['y'], tank_width, tank_height))
    elif tank['team']=='red':
        col = (245, 10, 10)
        pygame.draw.rect(win, col, (tank['x'], tank['y'], tank_width, tank_height))
    elif tank['team']=='bot':
        col = (10, 255, 10)
        pygame.draw.rect(win, col, (tank['x'], tank['y'], tank_width, tank_height))

    message = {'id': gc.getID(),'team': pTeam, 'x':x, 'y':y , 'bulletX':-1, 'bulletY':-1}
    if lastX!=x or lastY!=y:
        gc.send(message)
    lastX = x
    lastY = y

    pygame.display.update()

pygame.quit()
