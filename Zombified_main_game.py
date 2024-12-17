
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import numpy as np
import time

# Global Variables
screen_w= 1280
screen_h= 720


############################################################################################################
##-------------------------------------------##
#classes

class normal_circle:
    def __init__(self):
        self.x= random.randint(-240, 240)
        self.y= 300
        self.radius= 23

class specialcircle:
    def __init__(self):
        self.x= random.randint(-240, 240)
        self.y= 300
        self.r= 25
        self.ex_rate= 0.5
        self.current_r= self.r
        self.is_growing= True #true for growing, false for contraction
        
class shooter:
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]


##-------------------------------------------##
#zone conversion functions and midpoint circle/line algo
def zone_to_zero(x, y, zone):
    if zone== 0:
        return (x,y)    
    elif zone==1:
        return (y,x)
    elif zone==2:
        return (y,-x)    
    elif zone==3:
        return (-x,y)
    elif zone==4:
        return (-x,-y)    
    elif zone==5:
        return (-y,-x)
    elif zone==6:
        return (-y,x)  
    elif zone==7:
        return (x,-y)
def zone_normal_convert(x, y, zone):
    if zone==0:
        return (x,y)    
    elif zone==1:
        return (y,x)    
    elif zone==2:
        return (-y,x)    
    elif zone==3:
        return (-x,y)    
    elif zone==4:
        return (-x,-y)    
    elif zone==5:
        return (-y,-x)    
    elif zone==6:
        # print(y,-x)
        return (y,-x)    
    elif zone==7:
        return (x,-y)

#midpoint Line algo
def mp_line_algo(x,y,xp,yp,size=2):
    zone=0
    dy=yp-y
    dx=xp-x
    #just setting the zones here
    if abs(dy)<abs(dx):
        if dx>=0 and dy>=0:
            zone=0
        elif dx>=0 and dy<0:
            zone=7        
        elif dx<0 and dy<0:
            zone=4
        elif dx<0 and dy>=0:
            zone=3
    else:
        if dx>=0 and dy>=0:
            zone=1
        elif dx<0 and dy>=0:
            zone=2
        elif dx<0 and dy<0:
            zone=5
        elif dx>=0 and dy<0:
            zone=6

    x,y=zone_to_zero(x,y,zone)
    xp,yp=zone_to_zero(xp,yp,zone)
    dx=xp-x
    dy=yp-y
    east=2*dy
    northeast=2*(dy-dx)
    d=2*dy-dx
    x0,y0=zone_normal_convert(x,y,zone)
    draw_pixel(x0, y0,size)
    while x<xp:
        if d>0:
            d+=northeast
            x+=1
            y+=1
        else:
            d+=east
            x+=1  
        x0,y0=zone_normal_convert(x,y,zone)           
        draw_pixel(x0, y0,size)

#midpoint circle algo
def midpointcircle(r, x_main, y_main,size=2):
    x=0
    y=r
    d=1-r
    while y>x:
        draw_pixel(x+x_main,y_main+y,size)
        draw_pixel(y+x_main,y_main-x,size)
        draw_pixel(x_main-y,y_main+x,size)
        draw_pixel(x_main-y,-x+y_main,size)
        draw_pixel(x+x_main,-y+y_main,size)
        draw_pixel(x_main-x,y+y_main,size)
        draw_pixel(x_main-x,y_main-y,size)
        draw_pixel(y+x_main,x+y_main,size)
        if d<0:
            d+=2*x+3
        else:
            d+=5+2*x-2*y
            y=y- 1
        x=x+1


def draw_filled_rectangle(x1,y1,x2,y2,color,outline=False):

    if x1>x2:
        x1,x2= x2,x1
    if y1>y2:
        y1,y2= y2,y1
    glColor3fv(color)

    mp_line_algo(x1,y1,x1,y2)  
    mp_line_algo(x2,y1,x2,y2)  

    for y in range(y1, y2 + 1):
        mp_line_algo(x1, y, x2, y)  # Draw lines til we reach y2 from y1
    if outline==True:
        glColor3f(0.078,0.051,0.094)
        mp_line_algo(x1,y1,x1,y2)  
        mp_line_algo(x2,y1,x2,y2)  
        mp_line_algo(x1,y1,x2,y1)  
        mp_line_algo(x1,y2,x2,y2)

def draw_pixel(x, y,size=2): #drawing the point
    glPointSize(size)
    glBegin(GL_POINTS)
    # glColor3fv(self.color)
    glVertex2f(x,y)
    glEnd()
############################################################################################################
#Background drawing functions

def draw_tiles(x1,y1,x2,y2):
    #tile_base
    draw_filled_rectangle(x1,y1,x2,y2,[0.60,0.67,0.717],True)


    #tile_highlight
    glColor3fv([0.70,0.77,0.817])   
    mp_line_algo(x2-4, y2-3.5, x2-4, y1+3.5, 5) #width of line =5
    mp_line_algo(x2-4, y1+3.5, x1+3, y1+3.5, 5)  
    #small_dots at the edges  
    glColor3fv([0.29,0.27,0.317])
    draw_pixel(x1+3, y1+3, 5)
    draw_pixel(x1+3, y2-3.5, 5)
    draw_pixel(x2-4, y1+3, 5)
    draw_pixel(x2-4, y2-3.5, 5)


    #variation1 cross lines 
    glColor3fv([0.70,0.77,0.817])   
    mp_line_algo((x1+x2)/2-4, y1+3, (x1+x2)/2-4, y2-4, 5) #highlight
    mp_line_algo(x1+3, (y1+y2)/2-4, x2-4, (y1+y2)/2-4, 5)

    glColor3fv([0.45,0.5,0.6])  
    mp_line_algo((x1+x2)/2, y1+3, (x1+x2)/2, y2-4, 5)
    mp_line_algo(x1+3, (y1+y2)/2, x2-4, (y1+y2)/2, 5)

    #variation2 plus small in middle
    glColor3fv([0.29,0.27,0.387])
    mp_line_algo((x1+x2)/2, (y2+y1)/2+5, (x1+x2)/2, (y2+y1)/2-5, 5) #midcross
    mp_line_algo((x1+x2)/2-5, (x1+x2)/2, (x1+x2)/2+5, (x1+x2)/2, 5)

    # #variation3 double border 
    #        
    # glColor3fv([0.70,0.77,0.817])
    # mp_line_algo(x1 + 5, y1 + 5, x1 + 5, y2 - 5, 3)  # Left inner border
    # mp_line_algo(x2 - 5, y1 + 5, x2 - 5, y2 - 5, 3)  # Right inner border
    # mp_line_algo(x1 + 5, y1 + 5, x2 - 5, y1 + 5, 3)  # Top inner border
    # mp_line_algo(x1 + 5, y2 - 5, x2 - 5, y2 - 5, 3)  # Bottom inner border

    #variation 4: cracked lines
    glColor3fv([0.70,0.77,0.817])
    mp_line_algo(x2-4, (y2+y1)/2-21, (x1+x2)/2+30, (y2+y1)/2-21, 5) 
    mp_line_algo((x1+x2)/2+21,(y2+y1)/2-30, (x1+x2)/2+21, y1+3.5, 5)

    mp_line_algo((x1+x2)/2+25,(y2+y1)/2-25, (x1+x2)/2+25, y1+3.5, 5) #highlight

    glColor3fv([0.45,0.5,0.6])
    mp_line_algo(x2-4, (y2+y1)/2-25, (x1+x2)/2+30, (y2+y1)/2-25, 5) #horizontal line
    mp_line_algo((x1+x2)/2+25,(y2+y1)/2-30, (x1+x2)/2+25, y1+3.5, 5) #vertical line
                #top edge crack

    glColor3fv([0.70,0.77,0.817]) #highlight
    mp_line_algo(x1+20, y2-3.5, x1+20, y2-12, 5) 
    mp_line_algo(x1+20,y2-14, x1+14, y2-14, 5)
    glColor3fv([0.45,0.5,0.6])
    mp_line_algo(x1+25, y2-3.5, x1+25, y2-14, 5) 
    mp_line_algo(x1+25,y2-15, x1+20, y2-15, 5)



############################################################################################################
#main function

def mainfunc_animate():
    return None

############################################################################################################
#input handling functions

# def keyboardListener(key, x, y):
#     global bullet,is_paused,game_over_state,player_shooter
#     if key==b' ':
#         if is_paused==False and game_over_state<3:
#             bullet.append([player_shooter.x,-365])
#     elif key==b'a':
#         if player_shooter.x >-225 and is_paused==False:
#             player_shooter.x-=15
#     elif key==b'd':
#         if player_shooter.x<225 and is_paused==False:
#             player_shooter.x+=15
#     glutPostRedisplay()

# def mouseListener(button, state, x, y):
#     global  circles_bubs,bullet,miss,game_over_state,score,is_paused,spcl_cir

#     if button==GLUT_LEFT_BUTTON and state ==GLUT_DOWN:
#         c_x,c_y=convert_coordinate(x, y)
#         # print(f"Mouse clicked at: {c_x}, {c_y}")  # Debugging 
#         if -210 < c_x < -180 and 230 < c_y < 280:  # Reset
#             is_paused=False
#             print('new game')
#             circles_bubs=[]
#             for i in range(3):
#                 circles_bubs.append(normal_circle())
#                 # print(bubble)
#             circles_bubs.sort(key=lambda b:b.x)
#             spcl_cir=specialcircle()
#             score = 0
#             game_over_state = 0
#             miss = 0
#             bullet = []
#         elif -30 < c_x < 30 and 230 < c_y < 280:  # Pause
#             is_paused = not is_paused
#             print(f"Pause toggled to: {is_paused}")        
#         elif 165 < c_x < 220 and 230 < c_y < 280:  # Exit
#             print('Thanks for playing! Score:', score)
#             glutLeaveMainLoop()
#     glutPostRedisplay()




############################################################################################################
#UI Functions

# def draw_score():
#     global score, miss
#     glColor3f(1,1,1)
#     glRasterPos2f(150, -380)
#     score_text = f"Chances: {3-miss}"
#     for char in score_text:
#         glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18,ord(char))

#     draw_special_circle()
#     if gameover==False:
#         draw_score()

#     glutSwapBuffers()


############################################################################################################ 
#glui functions
def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    iterate()

    glColor3f(1,0,0)
    midpointcircle(10, 250, 250)
    # draw_filled_rectangle(100,100,200,200)
    draw_tiles(100,100,200,200)

    glutSwapBuffers()
def iterate():
    global screen_h, screen_w
    glViewport(0, 0, screen_w, screen_h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, screen_w, 0.0, screen_h, 0.0, 1.0) 
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
glutInit()
glutInitWindowSize(screen_w, screen_h)
glutInitWindowPosition(200,20)
glutInitDisplayMode(GLUT_RGBA)

glutCreateWindow(b"Spaceship Shooter")


# uq_cir=normal_circle()
# player_shooter=shooter()
# spcl_cir=specialcircle()

#fullscreen mode in options
# glutFullScreen()

glutDisplayFunc(display)
glutIdleFunc(mainfunc_animate)
# glutMouseFunc(mouseListener)
# glutKeyboardFunc(keyboardListener)
glutMainLoop()