#!/usr/bin/python
"""
    Requirements to run the code:
    Python 2.7.14
    Pygame 1.9.3
"""
import pygame
import math
import numpy as np
import time
import sys
import random
sys.setrecursionlimit(1500)

"""
Pygame screen properties
"""

background_colour = (0,0,0)
(width, height) = (850, 950)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Part 2')
screen.fill(background_colour)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

"""
Function to put text on screen
Function parameters:
    screen : The current game screen
    text: The message to be displayed
    x,y : The position of the text
    Color & font size : Self explained
"""
def text_to_screen(screen, text, x, y, color = (255, 255, 200),font_size = 50):

    font = pygame.font.SysFont('Comic Sans MS', font_size)
    try:

        text = str(text)
        # font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
        pygame.display.update()
    except Exception, e:
        print 'Font Error, saw it coming'
        raise e

"""
Function to set up the game environment
Function parameters:
    flag = true for creating a new map else loading a old map
"""
def game_env(flag = True):
    # # Global variable to store the map
    global m

    # # variable to hold the number of rows and columns in the grid
    rows=40
    columns=40

    # # If Flag create a empty map else use the saved map
    if flag:
        m = np.zeros((40,40))


    # # In m[i][j] i represents Rows and j represents Columns

    # # Setting the boundraies of the game environment
    for i in range(40):
        m[i][0]=1
        m[0][i]=1
        m[39][i]=1
        m[i][39]=1
        pygame.draw.circle(screen, (1,30,254),((i*20)+20,(39*20)+20), 8)
        pygame.draw.circle(screen, (1,30,254),((39*20)+20,(i*20)+20), 8)

    # # Reading the saved numpy array and creating a map
    # # Each game grid point is 20 pixal points away from each other
    y = 20
    for i in range(rows):
        x = 20
        for j in range(columns):

            # # Reading the map to construct the walls, start, stop and empty points
            if(m[j][i]==1):
                pygame.draw.circle(screen, (1,30,254),((i*20)+20,(j*20)+20), 8)
            elif(m[j][i]==2):
                pygame.draw.circle(screen, (253,254,2),((i*20)+20,(j*20)+20), 8)
            elif(m[j][i]==3):
                pygame.draw.circle(screen, (254,0,246),((i*20)+20,(j*20)+20), 8)
            else:
                m[j][i] = 0
                pygame.draw.circle(screen, (128,128,128), (y,x), 8)
            x = x+20
        y = y+20
    return m

"""
Function to create and monitor the generate button in the game environment
Function parameters:
    msg: the message to be displayed on the button
    mouse: the position of the mouse pointer
    x,y: position of the top left corner of the button
    w,h: width and height of the button
    ic: inactive color of the button
    ac: active color of the button
"""
def button(msg, mouse, x, y, w, h, ic = (0,255,0), ac = (0,155,0)):

    pygame.event.get()

    # # Checking for mouse click
    click = pygame.mouse.get_pressed()
    # # Checking if the mouse is over the button or not
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        # # Changing the color of the button to indicate mouse hover
        pygame.draw.rect(screen, ac,(x,y,w,h))
        # # Return true if the mouse is clicked on the button
        if click[0] == 1:
            return True
    # # If the mouse is not over the button leave the color in inactive mode
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    # # Write the required message on the button
    textsurface = myfont.render(msg, False, (0, 0, 0))
    screen.blit(textsurface,(x+5,y+8))
    pygame.display.update()

"""
Function to convert the pixal grid points to the game environment grid points
Function Parameters:
    pos: x and y pixal points to be converted to game grid points
    but: a string to denote if the points belong to a button
    m: the map
"""
def px2dp(pos,but,m):

    # # Since the game grid points are multiples of 20
    # # Divide the pixal point by 20 to get the quotient and subtract it with
    # #     the pixel point to get the game grid point
    x = pos[0] - pos[0]%20
    y = pos[1] - pos[1]%20

    # # If the pixel point belong to delete button
    if but == 'dele':
        # # Remove the points from map
        m[(y/20)-1][(x/20)-1] = 0
        return((x,y),m)

    # # If the current pixel point is empty
    if m[(y/20)-1][(x/20)-1] == 0:
        # # And if the button is start point, Update the map with the start position
        if but == 'start': m[(y/20)-1][(x/20)-1] = 2
        # # else if the button is stop point, Update the map with the stop position
        elif but == 'stop': m[(y/20)-1][(x/20)-1] = 3
        # # else, Update the map with a wall
        else: m[(y/20)-1][(x/20)-1] = 1
        return((x,y),m)

    else: return(None,m)

"""
Function for the Game play
"""
def game_play():
    # # Global variable for storing the map
    global m

    # # Creating buttons for respective functions
    clear = button('clear map',pygame.mouse.get_pos(),10,840,105,40,)
    start = button('start pt',pygame.mouse.get_pos(),130,840,90,40,)
    stop = button('stop pt',pygame.mouse.get_pos(),250,840,90,40,)
    wall = button('build wall',pygame.mouse.get_pos(),360,840,110,40,)
    end_wall = button('end wall',pygame.mouse.get_pos(),490,840,98,40,)
    dele = button('delete pt',pygame.mouse.get_pos(),610,840,95,40,)
    save = button('save map',pygame.mouse.get_pos(),718,840,95,40,)
    run = button('Run robot',pygame.mouse.get_pos(),350,900,120,40,)

    # # If Clear button is pressed clean the entire map
    if clear:
        m = game_env()

    # # If start button is pressed create a start point
    if start:

        # # Wait for 20 Seconds for the user to place a start point
        start_time = time.time()
        while time.time()-start_time<20:
            pygame.event.get()

            # # If the user clicks the mouse
            if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                # # Record the position of the mouse
                pos = pygame.mouse.get_pos()
                # # Check if it is within the game boundraies
                if 40 <= pos[0] <= 790 and 40 <= pos[1] <= 790:
                    # # Convert the pixal points to digital points and update the map
                    pts,m = px2dp(pos,'start', m)
                    # # Draw a circle representing the start point
                    if pts != None:
                        pygame.draw.circle(screen, (253,254,2),pts, 8)
                    # # Break the while loop
                    break

    if stop:

        # # Wait for 20 Seconds for the user to place a stop point
        start_time = time.time()
        while time.time()-start_time<20:
            pygame.event.get()

            # # If the user clicks the mouse
            if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                # # Record the position of the mouse
                pos = pygame.mouse.get_pos()
                # # Check if it is within the game boundraies
                if 40 <= pos[0] <= 790 and 40 <= pos[1] <= 790:
                    # # Convert the pixal points to digital points and update the map
                    pts,m = px2dp(pos,'stop', m)
                    # # Draw a circle representing the start point
                    if pts != None:
                        pygame.draw.circle(screen, (254,0,246),pts, 8)
                    # # Break the while loop
                    break
    if dele:
        # # Wait for 20 Seconds for the user to a delete point
        start_time = time.time()
        while time.time()-start_time<20:
            pygame.event.get()

            # # If the user clicks the mouse
            if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                # # Record the position of the mouse
                pos = pygame.mouse.get_pos()
                # # Check if it is within the game boundraies
                if 40 <= pos[0] <= 790 and 40 <= pos[1] <= 790:
                    # # Convert the pixal points to digital points and update the map
                    pts,m = px2dp(pos,'dele', m)
                    # # Draw a circle representing the start point
                    if pts != None:
                        pygame.draw.circle(screen, (128,128,128),pts, 8)
                    # # Break the while loop
                    break

    # # If the save button is pressed save the map as a numpy array and as txt
    if save:
        np.save('map.npy', m)
        np.savetxt('map.txt',m.astype(int))

    # # If run button is pressed execute the search operation
    if run:

        # # Search the entire map for the Start point
        for i in range(40):
            for j in range(40):
                if(m[j][i]==2):
                    # # Call the find_path function with the position of the start point
                    find_path((j,i))

    # # If wall button is pressed build walls
    if wall:

        # # Keep running the loop till end wall button is pressed
        while True:
            # # Flag to monitor mouse button hold
            Flag = False
            # # If the mouse button is held set the flag to true
            if pygame.mouse.get_pressed()[0]:
                Flag = True
                time.sleep(1)
            # # If the mouse button is held draw wall at the location of mouse
            while Flag:
                # # Getting the location of the mouse
                pos = pygame.mouse.get_pos()
                # # Checking if it is within the boundraies of the game
                if 20 <= pos[0] <= 810 and 20 <= pos[1] <= 810:
                    # # Convert the pixal point to game grid points and update the map
                    pts,m = px2dp(pos,'None', m)
                    if pts != None:
                        # # Color the points to indicate wall
                        pygame.draw.circle(screen, (1,30,254),pts, 8)

                # # Clear the event queue (event queue monitors mouse clicks)
                pygame.event.clear()
                pygame.display.update()
                pygame.event.get()
                # # If the mouse is released reset the flag to exit the while loop
                if pygame.mouse.get_pressed()[0] != 1:
                        Flag = False

            # # If end wall button is pressed exit wall building mode
            end_wall = button('end wall',pygame.mouse.get_pos(),490,840,98,40,)
            if end_wall:
                pygame.event.clear()
                wall = None
                break

"""
Function to compute the available positions for the robot to move from the current position
Function parameters:
    pos: current position of the robot
"""
def adjacent_pos(pos):

    global flag
    # # Variables for holding the new position
    new_pos = None
    temp_hold = []

    # # Check if the north south, west and east positions are occupied by a wall,
    # # start point or stop point. Also check if the adjacent_positions are already explored
    # # If free make it as a possible next step
    if (m[pos[0]][pos[1]-1]) == 0:
        if (pos[0],pos[1]-1) not in path:
            temp_hold.append((pos[0],pos[1]-1))

            new_pos = ((pos[0],pos[1]-1))
    if (m[pos[0]][pos[1]+1]) == 0:
        if (pos[0],pos[1]+1) not in path:
            temp_hold.append((pos[0],pos[1]+1))

            new_pos = ((pos[0],pos[1]+1))
    if (m[pos[0]-1][pos[1]]) == 0:
        if (pos[0]-1,pos[1]) not in path:
            temp_hold.append((pos[0]-1,pos[1]))

            new_pos = ((pos[0]-1,pos[1]))
    if (m[pos[0]+1][pos[1]]) == 0:
        if (pos[0]+1,pos[1]) not in path:
            temp_hold.append((pos[0]+1,pos[1]))
            new_pos = ((pos[0]+1,pos[1]))

    # # If stopped stop position exit the game
    elif(m[pos[0]][pos[1]-1] == 3 or m[pos[0]][pos[1]+1] == 3 or m[pos[0]-1][pos[1]] == 3 or m[pos[0]+1][pos[1]] == 3):
        text_to_screen(screen,'Total steps taken: '+str(c) , 400,100)
        while True:
            if pygame.event.get(pygame.QUIT):
                sys.exit()

    # # If there are more than one vaiable next position, choose one randomly
    if len(temp_hold)>1:
        new_pos = random.choice(temp_hold)
        vertex_trak.append(1)

    else:
        vertex_trak.append(0)

    return new_pos

"""
Function to find the path to the stop point
Function parameters:
    pos: current position of the robot
"""

# # Variable to store the path from start to stop point
path = []
# # A vaiable to hold the history of position
back_track = []
# # A vairable to keep track of the positions which had multiple next positions
vertex_trak = []
# # Variable to count the number of iterations
c = 0
# # Variable for coloring the pixals
co = 100
# # Variable for controlling the speed of the simulation
delay = 0.08
def find_path(pos):
    global vertex_trak
    global back_track
    global path
    global c
    global co
    global delay
    # # Incrementing the iteration count
    c = c+1

    # # Changing the shades of a color
    co = co+1
    if co == 254:
        co = 100

    # print("iter ",c)

    # # If close button is clicked exit the game
    if pygame.event.get(pygame.QUIT):
        sys.exit()

    # # Get new position to move from the current position
    new_pos = adjacent_pos(pos)

    # # If a new position exit
    if new_pos:
        # # append the position to path and back track
        path.append(new_pos)
        back_track.append(new_pos)

        # # Color the circle to indicate the robot moving to the position
        j,i = new_pos[0],new_pos[1]
        pygame.draw.circle(screen, (0,co,0),((i*20)+20,(j*20)+20), 8)
        pygame.display.update()
        time.sleep(delay)

        # # With the new position call the same function to get a new position and update the path
        find_path(new_pos)

    # # If a new position doesnt exist the robot is stuck
    else:
        temp = []
        temp_vertex_len = len(vertex_trak)

        # # Reverse iterate through the list that kept track of position with multiple new position options
        for a in range(len(vertex_trak)-1):

            # # Get the game grid point of the previous locations traveled
            j,i = back_track[len(back_track)-a-1][0],back_track[len(back_track)-a-1][1]

            pygame.display.update()
            time.sleep(delay)

            # # If the code went back to the latest position it traveled with
            # #     multiple options go for the other option
            if vertex_trak[len(vertex_trak)-a-1] == 1:

                # # Iterate theough the temporary variable that holds the deleted points
                for a in range(len(temp)):
                    # # Remove the points from back track history and vertex history
                    back_track.remove(temp[a])
                    vertex_trak.pop(temp_vertex_len-a-1)

                # # Find a new path with the alternate option
                find_path((j,i))

            else:
                # # Color the reversed points red
                pygame.draw.circle(screen, (128,128,128),((i*20)+20,(j*20)+20), 8)
                # # Remove these points from the path track
                path.remove((j,i))
                # # Attribute these points as walls so the robot doesnt go there again
                m[j][i] = 1
                # # append the points removed to a temporary variable
                temp.append(back_track[len(back_track)-a-1])



"""
Begining of the program
"""
if __name__ == '__main__':

    # # Load a map, if it exists in the same folder
    try:
        m = np.load('map.npy')
        # print("Loaded a map")
        # # Calling the function game_env to setup the loaded map
        m = game_env(False)

    # # If there is no map create a new one
    except:
        # print("New map")

        # # Setting up the main game environment with a new map
        m = game_env(True)
    while True:
        # # Start the game play
        game_play()
        pygame.display.update()
