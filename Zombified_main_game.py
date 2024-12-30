
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import numpy as np
import time
import math

#to do: Use a loop to render shadows

# Global Variables
screen_w= 840
screen_h= 740

tiles_iteration_list=[] #Stores random variation values so the floor doesn't change during gameplay
#initializing the tiles variation list
for _ in range(0,screen_w*screen_h,1000):
    tiles_iteration_list.append(random.randint(1,50))

############################################################################################################
##-------------------------------------------##
#classes


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

#draw square
def draw_filled_rectangle(x1, y1, x2, y2, color):
    if x1>x2:
        x1,x2=x2,x1

    if y1>y2:
        y1,y2=y2,y1

    width=x2-x1
    height=y2-y1

    glColor3fv(color)
    point_size=max(width,height)  #most of the time both will be same as it is a square
    glPointSize(point_size)

    center_x=(x1+x2)/2
    center_y=(y1+y2)/2

    glBegin(GL_POINTS)
    glVertex2i(int(center_x), int(center_y))
    glEnd()

def draw_square_outline(x1,y1,x2,y2,color,size=3):
    glColor3fv(color)
    mp_line_algo(x1,y1,x1,y2, size)  
    mp_line_algo(x2,y1,x2,y2, size)   
    mp_line_algo(x1,y1,x2,y1, size)   
    mp_line_algo(x1,y2,x2,y2, size) 

def draw_pixel(x,y,size=2): #drawing the point
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

############################################################################################################
#Background drawing functions

def draw_tiles(x1,y1,x2,y2,iteration):

    # iteration= random.randint(1,100)
    # print(iteration)
    #tile_base
    draw_filled_rectangle(x1,y1,x2,y2,[0.6078,0.6784,0.7176])
    #tile_highlight
    glColor3fv([0.6745,0.7764,0.7803])   
    mp_line_algo(x2-4, y2-3.5, x2-4, y1+3.5, 9) #width of line =9
    mp_line_algo(x2-4, y1+3.5, x1+3, y1+3.5, 9)  
    #small_dots at the edges  
    glColor3fv([0.490,0.545,0.659])
    draw_pixel(x1+3, y1+3, 9)
    draw_pixel(x1+3, y2-3.5, 9)
    draw_pixel(x2-4, y1+3, 9)
    draw_pixel(x2-4, y2-3.5, 9)


#variation part

    if iteration==24 or iteration==12 or iteration==22 or iteration==18:
        # #variation1 cross lines 
        glColor3fv([0.6745,0.7764,0.7803])   
        mp_line_algo((x1+x2)/2-4, y1+3, (x1+x2)/2-4, y2-4, 8) #highlight
        mp_line_algo(x1+3, (y1+y2)/2-4, x2-4, (y1+y2)/2-4, 8)

        glColor3fv([0.490,0.545,0.659])  
        mp_line_algo((x1+x2)/2, y1+3, (x1+x2)/2, y2-4, 6)
        mp_line_algo(x1+3, (y1+y2)/2, x2-4, (y1+y2)/2, 6)
        if iteration ==12 or iteration ==22:
            # #variation2 plus small in middle
            glColor3fv([0.33,0.313,0.439])
            mp_line_algo((x1+x2)/2, (y2+y1)/2+5, (x1+x2)/2, (y2+y1)/2-5, 6) #midcross
            mp_line_algo((x1+x2)/2-5, (y1+y2)/2, (x1+x2)/2+5, (y1+y2)/2, 6)


    if iteration<4 or iteration==18:
        # #variation 4: cracked lines
        glColor3fv([0.6745,0.7764,0.7803])
        mp_line_algo(x2-4, (y2+y1)/2-21, (x1+x2)/2+30, (y2+y1)/2-21, 6) 
        mp_line_algo((x1+x2)/2+21,(y2+y1)/2-30, (x1+x2)/2+21, y1+3.5, 6)

        mp_line_algo((x1+x2)/2+25,(y2+y1)/2-25, (x1+x2)/2+25, y1+3.5, 8) #highlight

        glColor3fv([0.490,0.545,0.659])
        mp_line_algo(x2-4, (y2+y1)/2-25, (x1+x2)/2+30, (y2+y1)/2-25, 6) #horizontal line
        mp_line_algo((x1+x2)/2+25,(y2+y1)/2-30, (x1+x2)/2+25, y1+3.5, 6) #vertical line
                    #top edge crack

        glColor3fv([0.6745,0.7764,0.7803]) #highlight
        mp_line_algo(x1+20, y2-3.5, x1+20, y2-12, 8) 
        mp_line_algo(x1+20,y2-14, x1+14, y2-14, 8)
        glColor3fv([0.490,0.545,0.659])
        mp_line_algo(x1+25, y2-3.5, x1+25, y2-14, 6) 
        mp_line_algo(x1+25,y2-15, x1+20, y2-15,6)

    #outlines of the tiles
    draw_square_outline(x1,y1,x2,y2,[0.16,0.125,0.2],5)



def generate_floor(screen_h,screen_w):
    iteration=0
    global tiles_iteration_list
    for i in range(0,screen_h-100,100):
        for j in range(0,screen_w,100):
            draw_tiles(j,i,j+100,i+100,tiles_iteration_list[iteration])
            iteration+=1
            # print("iteration: ",iteration,"Value: ", tiles_iteration_list[iteration])
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.15, 0.1, 0.35,0.2)  

    draw_pixel(-40,100,200)
    draw_pixel(-40,300,200)
    draw_pixel(-40,500,200)
    draw_pixel(160,620,200)
    draw_pixel(360,620,200)
    draw_pixel(560,620,200)
    draw_pixel(760,620,200)
    draw_pixel(65,515,10)
    glDisable(GL_BLEND)  

class Zombie:
    def __init__(self, x, y, rotation=0):
        self.x=x
        self.y=y
        self.rotation=rotation
        self.is_attacking=False
    def rotate_point(self,point,angle,center):
            angle_rad=math.radians(angle)
            x,y=point
            cx,cy=center
            x-=cx
            y-=cy
            x_new=x*math.cos(angle_rad)-y*math.sin(angle_rad)
            y_new=x*math.sin(angle_rad)+y*math.cos(angle_rad)
            # print(x_new+cx,y_new+cy)
            return (x_new+cx,y_new+cy)
        
class Special_Zombie:
    def __init__(self, x, y, rotation=0):
        self.x=x
        self.y=y
        self.rotation=rotation
        self.is_attacking=False

    def rotate_point(self,point,angle,center):
            angle_rad=math.radians(angle)
            x,y=point
            cx,cy=center
            x-=cx
            y-=cy
            x_new=x*math.cos(angle_rad)-y*math.sin(angle_rad)
            y_new=x*math.sin(angle_rad)+y*math.cos(angle_rad)
            # print(x_new+cx,y_new+cy)
            return (x_new+cx,y_new+cy)

class Player:
    def __init__(self, x, y, rotation=0):
        self.x=x
        self.y=y
        self.rotation=rotation
    def rotate_point(self,point,angle,center):
            angle_rad=math.radians(angle)
            x,y=point
            cx,cy=center
            x-=cx
            y-=cy
            x_new=x*math.cos(angle_rad)-y*math.sin(angle_rad)
            y_new=x*math.sin(angle_rad)+y*math.cos(angle_rad)
            # print(x_new+cx,y_new+cy)
            return (x_new+cx,y_new+cy)
def draw_player(player):
    x, y = player.x, player.y
    rotation = player.rotation

    def rotate_point_and_draw(x1, y1,size, x2, y2,color):
            point1=[x1, y1]
            point2=[x2, y2]
            center=[x, y]
            p1 = player.rotate_point(point1,rotation,center)
            p2 = player.rotate_point(point2,rotation,center)
            glColor3f(color[0], color[1], color[2])
            mp_line_algo(p1[0], p1[1], p2[0], p2[1],size)

    #left hand
    rotate_point_and_draw(x-25, y-7,6,x-10,y+41,[0.4784,0.043,0.796])
    rotate_point_and_draw(x-30, y-8,5,x-15,y+43,[0.4784,0.043,0.796])
    rotate_point_and_draw(x-35, y-7,6,x-20,y+41,[0.4784,0.043,0.796])

    rotate_point_and_draw(x-35, y-7,6,x-20,y+41,[0.3784,0.023,0.596])
    rotate_point_and_draw(x-35, y-7,6,x-10,y-7,[0.3784,0.023,0.596])

    rotate_point_and_draw(x-10, y+38,4,x-25,y+38,[0.93,0.549,0.48])
    rotate_point_and_draw(x-8, y+41,4,x-26,y+41,[0.976,0.745,0.65]) #handskin
    
    #outline
    #left hand
    rotate_point_and_draw(x-20, y-10,4,x-5,y+45,[0.047,0.103,0.0]) #closest long
    rotate_point_and_draw(x-40, y-10,4,x-25,y+45,[0.047,0.103,0.0])
    rotate_point_and_draw(x-25, y+45,4,x-5,y+45,[0.047,0.103,0.0])
    rotate_point_and_draw(x-40, y-10,4,x-20,y-10,[0.047,0.103,0.0]) #bottom short


    #right hand
    rotate_point_and_draw(x+25, y-7,6,x+10,y+41,[0.4784,0.043,0.796])
    rotate_point_and_draw(x+30, y-8,5,x+15,y+43,[0.4784,0.043,0.796])
    rotate_point_and_draw(x+35, y-7,6,x+20,y+41,[0.4784,0.043,0.796])

    rotate_point_and_draw(x+35, y-7,6,x+20,y+41,[0.3784,0.023,0.596])
    rotate_point_and_draw(x+35, y-7,6,x+10,y-7,[0.3784,0.023,0.596])

    rotate_point_and_draw(x+10, y+38,4,x+25,y+38,[0.93,0.549,0.48])
    rotate_point_and_draw(x+8, y+41,4,x+25,y+41,[0.976,0.745,0.65]) #handskin
    #outline
    rotate_point_and_draw(x+20, y-10,4,x+5,y+45,[0.047,0.103,0.0]) #closest long
    rotate_point_and_draw(x+40, y-10,4,x+25,y+45,[0.047,0.103,0.0])
    rotate_point_and_draw(x+25, y+45,4,x+5,y+45,[0.047,0.103,0.0])
    rotate_point_and_draw(x+40, y-10,4,x+20,y-10,[0.047,0.103,0.0]) #bottom short



    #Head Filled
    rotate_point_and_draw(x, y+15,10,x,y-15,[0.439,0.243,0.31])
    rotate_point_and_draw(x+10, y+15,10,x+10,y-15,[0.439,0.243,0.31])
    rotate_point_and_draw(x-10, y+15,10,x-10,y-15,[0.439,0.243,0.31])
    rotate_point_and_draw(x+15, y+15,7,x+15,y-15,[0.439,0.243,0.31])
    # rotate_point_and_draw(x-15, y+15,7,x-15,y-15,[0.439,0.243,0.31])

    #headshadow
    rotate_point_and_draw(x-13, y+13,10,x-13,y-13,[0.250,0.1490,0.2])
    rotate_point_and_draw(x-14, y-15,7,x+14,y-15,[0.250,0.1490,0.2])
    rotate_point_and_draw(x-7, y-10,5,x-3,y-10,[0.250,0.1490,0.2])

    #Eyes
    #eyeshadow
    rotate_point_and_draw(x+10,y+15,10,x-10,y+15,[0.9764,0.745,0.650])

    #right Eye
    rotate_point_and_draw(x+12,y+16,5,x+8,y+16,[0,0,0])
    rotate_point_and_draw(x+12,y+12,4,x+8,y+12,[1,1,1])
    #left eye
    rotate_point_and_draw(x-12,y+16,5,x-8,y+16,[0,0,0])
    rotate_point_and_draw(x-12,y+12,4,x-8,y+12,[1,1,1])

    #blood head
    rotate_point_and_draw(x-17, y-16,8,x-10,y-16,[0.219,0.137,0.176])
    rotate_point_and_draw(x-17, y-16,8,x-17,y-10,[0.219,0.137,0.176])
    rotate_point_and_draw(x-17, y-16,4,x-17,y-13,[0.219,0.137,0.176])
    rotate_point_and_draw(x-17, y-16,4,x-13,y-16,[0.219,0.137,0.176])

    rotate_point_and_draw(x+17, y-16,5,x+10,y-16,[0.219,0.137,0.176])
    rotate_point_and_draw(x+17, y-16,6,x+17,y-10,[0.219,0.137,0.176])

    # Head Outline
    rotate_point_and_draw(x+20,y+20,4,x-20,y+20,[0.047,0.103,0.0])
    rotate_point_and_draw(x+20,y+20,4,x+20,y-20,[0.047,0.103,0.0]) 
    rotate_point_and_draw(x-20, y+20,4,x-20,y-20,[0.047,0.103,0.0])
    rotate_point_and_draw(x-20, y-20,4,x+20,y-20,[0.047,0.103,0.0])

    # Gun
    # Body
    rotate_point_and_draw(x+4,y+44,10,x+4,y+70,[0.278,0.294,0.337])
    rotate_point_and_draw(x-4,y+44,10,x-4,y+70,[0.278,0.294,0.337])
    # Outline
    rotate_point_and_draw(x+8,y+40,4,x+8,y+75,[0.117,0.113,0.125])
    rotate_point_and_draw(x-8,y+40,4,x-8,y+75,[0.117,0.113,0.125])
    rotate_point_and_draw(x-8,y+75,4,x+8,y+75,[0.117,0.113,0.125])
    rotate_point_and_draw(x-8,y+40,4,x+8,y+40,[0.117,0.113,0.125])

    # Ridge
    rotate_point_and_draw(x-3,y+50,2,x+3,y+50,[0.337,0.337,0.345])
    rotate_point_and_draw(x-2,y+55,2,x+2,y+55,[0.337,0.337,0.345])
    # Screw
    rotate_point_and_draw(x-6,y+65,1,x-6,y+65,[0.6,0.6,0.6])
    rotate_point_and_draw(x+6,y+65,1,x+6,y+65,[0.6,0.6,0.6])
  
    rotate_point_and_draw(x,y+42,2,x,y+46,[0.1,0.1,0.1])
    # Muzzle
    rotate_point_and_draw(x-2,y+75,3,x+2,y+75,[0.278,0.294,0.337])
    rotate_point_and_draw(x-1,y+76,2,x+1,y+76,[0.117,0.113,0.125])

    rotate_point_and_draw(x-8,y+73,2,x+8,y+73,[0.117,0.113,0.125])



        
def draw_zombie(zombie):
    x, y = zombie.x, zombie.y
    rotation = zombie.rotation

    def rotate_point_and_draw(x1, y1,size, x2, y2,color):
            point1=[x1, y1]
            point2=[x2, y2]
            center=[x, y]
            p1 = zombie.rotate_point(point1,rotation,center)
            p2 = zombie.rotate_point(point2,rotation,center)
            glColor3f(color[0], color[1], color[2])
            mp_line_algo(p1[0], p1[1], p2[0], p2[1],size)

    #left hand
    rotate_point_and_draw(x-25, y-7,6,x-25,y+41,[0.147,0.445,0.28])
    rotate_point_and_draw(x-30, y-8,5,x-30,y+43,[0.147,0.445,0.28])
    rotate_point_and_draw(x-35, y-7,6,x-35,y+41,[0.147,0.445,0.28])

    rotate_point_and_draw(x-35, y-7,6,x-35,y+41,[0.047,0.345,0.18])
    rotate_point_and_draw(x-35, y-7,6,x-25,y-7,[0.047,0.345,0.18])

    rotate_point_and_draw(x-34, y+8,5,x-37,y+5,[0.758,0.35,0.35])

    rotate_point_and_draw(x-22, y+42,7,x-22,y+35,[0.3527,0.565,0.3512])#green color

    rotate_point_and_draw(x-37, y+25,3,x-37,y+30,[0.758,0.05,0.05])
    #outline
    rotate_point_and_draw(x-20, y-10,4,x-20,y+45,[0.047,0.103,0.0]) #closest long
    rotate_point_and_draw(x-40, y-10,4,x-40,y+45,[0.047,0.103,0.0])
    rotate_point_and_draw(x-40, y+45,4,x-20,y+45,[0.047,0.103,0.0])
    rotate_point_and_draw(x-40, y-10,4,x-20,y-10,[0.047,0.103,0.0]) #bottom short



     #right hand
    rotate_point_and_draw(x+25, y-7,6,x+25,y+41,[0.147,0.445,0.28])
    rotate_point_and_draw(x+30, y-8,5,x+30,y+43,[0.147,0.445,0.28])
    rotate_point_and_draw(x+35, y-7,6,x+35,y+41,[0.147,0.445,0.28])

    rotate_point_and_draw(x+35, y-7,6,x+35,y+41,[0.047,0.345,0.18])
    rotate_point_and_draw(x+35, y-7,6,x+25,y-7,[0.047,0.345,0.18])

    rotate_point_and_draw(x+34, y+8,5,x+37,y+5,[0.758,0.35,0.35])
    rotate_point_and_draw(x+33, y+10,3,x+37,y+7,[0.758,0.05,0.05])
    rotate_point_and_draw(x+22, y+42,7,x+22,y+35,[0.3527,0.565,0.3512])
     #outline
    rotate_point_and_draw(x+20, y-10,4,x+20,y+45,[0.047,0.103,0.0]) #closest long
    rotate_point_and_draw(x+40, y-10,4,x+40,y+45,[0.047,0.103,0.0])
    rotate_point_and_draw(x+40, y+45,4,x+20,y+45,[0.047,0.103,0.0])
    rotate_point_and_draw(x+40, y-10,4,x+20,y-10,[0.047,0.103,0.0]) #bottom short

    #Head Filled
    rotate_point_and_draw(x, y+15,10,x,y-15,[0.147,0.445,0.28])
    rotate_point_and_draw(x+10, y+15,10,x+10,y-15,[0.147,0.445,0.28])
    rotate_point_and_draw(x-10, y+15,10,x-10,y-15,[0.147,0.445,0.28])
    rotate_point_and_draw(x+15, y+15,7,x+15,y-15,[0.147,0.445,0.28])
    rotate_point_and_draw(x-15, y+15,7,x-15,y-15,[0.147,0.445,0.28])

    #headshadow
    rotate_point_and_draw(x-13, y+13,10,x-13,y-13,[0.047,0.345,0.18])
    rotate_point_and_draw(x-14, y-15,7,x+14,y-15,[0.047,0.345,0.18])
    rotate_point_and_draw(x-7, y-10,5,x-3,y-10,[0.047,0.345,0.18])

    #Eyes
    #eyeshadow
    rotate_point_and_draw(x+10,y+17,3,x-10,y+17,[0.029,0.198,0.1068])

    #right Eye
    rotate_point_and_draw(x+10,y+15,4,x+16,y+15,[1,1,1])
    rotate_point_and_draw(x+10,y+12,4,x+16,y+12,[1,1,1])
    #left eye
    rotate_point_and_draw(x-10,y+15,4,x-16,y+15,[1,1,1])
    rotate_point_and_draw(x-10,y+12,4,x-16,y+12,[1,1,1])

    #blood head
    rotate_point_and_draw(x-17, y-16,8,x-10,y-16,[0.758,0.05,0.05])
    rotate_point_and_draw(x-17, y-16,8,x-17,y-10,[0.758,0.05,0.05])
    rotate_point_and_draw(x-17, y-16,4,x-17,y-13,[0.55,0.05,0.05])
    rotate_point_and_draw(x-17, y-16,4,x-13,y-16,[0.5,0.05,0.05])

    rotate_point_and_draw(x+17, y-16,5,x+10,y-16,[0.758,0.05,0.05])
    rotate_point_and_draw(x+17, y-16,6,x+17,y-10,[0.758,0.35,0.35])

    # Head Outline
    rotate_point_and_draw(x+20,y+20,4,x-20,y+20,[0.047,0.103,0.0])
    rotate_point_and_draw(x+20,y+20,4,x+20,y-20,[0.047,0.103,0.0]) 
    rotate_point_and_draw(x-20, y+20,4,x-20,y-20,[0.047,0.103,0.0])
    rotate_point_and_draw(x-20, y-20,4,x+20,y-20,[0.047,0.103,0.0])

    
def draw_special_zombie(zombie):
    scale_factor = 1.5  # Adjust scale factor as needed
    x, y = zombie.x, zombie.y
    rotation = zombie.rotation

    def rotate_point_and_draw(x1, y1, size, x2, y2, color):
        point1=[x+(x1-x)*scale_factor,y+(y1-y)*scale_factor]
        point2=[x+(x2-x)*scale_factor,y+(y2-y)*scale_factor]
        center=[x, y]
        p1=zombie.rotate_point(point1,rotation,center)
        p2=zombie.rotate_point(point2,rotation,center)
        glColor3f(color[0], color[1], color[2])
        mp_line_algo(p1[0], p1[1], p2[0], p2[1], size * scale_factor)
    #left hand
    rotate_point_and_draw(x-25, y-7,6,x-25,y+41,[0.780,0.670,0.435])
    rotate_point_and_draw(x-30, y-8,5,x-30,y+43,[0.780,0.670,0.435])
    rotate_point_and_draw(x-35, y-7,6,x-35,y+41,[0.780,0.670,0.435])

    rotate_point_and_draw(x-35, y-7,6,x-35,y+41,[0.576,0.505,0.353])
    rotate_point_and_draw(x-35, y-7,6,x-25,y-7,[0.576,0.505,0.353])

    rotate_point_and_draw(x-34, y+8,5,x-37,y+5,[0.33,0.30,0.262])
# [0.552,0.498,0.498]
    rotate_point_and_draw(x-22, y+42,7,x-22,y+35,[0.890,0.792,0.572])#green color

    rotate_point_and_draw(x-37, y+25,3,x-37,y+30,[0.152,0.137,0.105])
    #outline
    rotate_point_and_draw(x-20, y-10,4,x-20,y+45,[0.094,0.086,0.066]) #closest long
    rotate_point_and_draw(x-40, y-10,4,x-40,y+45,[0.094,0.086,0.066])
    rotate_point_and_draw(x-40, y+46,4,x-20,y+46,[0.094,0.086,0.066])
    rotate_point_and_draw(x-40, y-10,4,x-20,y-10,[0.094,0.086,0.066]) #bottom short



     #right hand
    rotate_point_and_draw(x+25, y-7,6,x+25,y+41,[0.780,0.670,0.435])
    rotate_point_and_draw(x+30, y-8,5,x+30,y+43,[0.780,0.670,0.435])
    rotate_point_and_draw(x+35, y-7,6,x+35,y+41,[0.780,0.670,0.435])

    rotate_point_and_draw(x+35, y-7,6,x+35,y+41,[0.576,0.505,0.353])
    rotate_point_and_draw(x+35, y-7,6,x+25,y-7,[0.576,0.505,0.353])

    # rotate_point_and_draw(x+34, y+8,5,x+37,y+5,[0.758,0.05,0.05])
    rotate_point_and_draw(x+33, y+10,3,x+37,y+7,[0.758,0.35,0.35]) #pink
    rotate_point_and_draw(x+22, y+42,7,x+22,y+35,[0.890,0.792,0.572])
     #outline
    rotate_point_and_draw(x+20, y-10,4,x+20,y+45,[0.094,0.086,0.066]) #closest long
    rotate_point_and_draw(x+40, y-10,4,x+40,y+45,[0.094,0.086,0.066])
    rotate_point_and_draw(x+40, y+46,4,x+20,y+46,[0.094,0.086,0.066])
    rotate_point_and_draw(x+40, y-10,4,x+20,y-10,[0.094,0.086,0.066]) #bottom short

    #Head Filled
    rotate_point_and_draw(x, y+15,10,x,y-15,[0.301,0.262,0.211])
    rotate_point_and_draw(x+10, y+15,10,x+10,y-15,[0.301,0.262,0.211])
    rotate_point_and_draw(x-10, y+15,10,x-10,y-15,[0.301,0.262,0.211])
    rotate_point_and_draw(x+15, y+15,7,x+15,y-15,[0.301,0.262,0.211])
    rotate_point_and_draw(x-15, y+15,7,x-15,y-15,[0.301,0.262,0.211])

    #headshadow
    rotate_point_and_draw(x-13, y+13,10,x-13,y-13,[0.145,0.125,0.094])
    rotate_point_and_draw(x-14, y-15,7,x+14,y-15,[0.145,0.125,0.094])
    rotate_point_and_draw(x-7, y-10,5,x-3,y-10,[0.145,0.125,0.094])

    #Eyes
    #eyeshadow
    rotate_point_and_draw(x+10,y+17,3,x-10,y+17,[0.145,0.125,0.094])

    #right Eye
    rotate_point_and_draw(x+10,y+17,4,x+16,y+17,[1,1,1])
    rotate_point_and_draw(x+10,y+14,4,x+16,y+14,[1,1,1])
    #left eye
    rotate_point_and_draw(x-10,y+17,4,x-16,y+17,[1,1,1])
    rotate_point_and_draw(x-10,y+14,4,x-16,y+14,[1,1,1])

    #blood head
    rotate_point_and_draw(x-17, y-16,8,x-10,y-16,[0.758,0.05,0.05])
    rotate_point_and_draw(x-17, y-16,8,x-17,y-10,[0.758,0.05,0.05])
    rotate_point_and_draw(x-17, y-16,4,x-17,y-13,[0.55,0.05,0.05])
    rotate_point_and_draw(x-17, y-16,4,x-13,y-16,[0.5,0.05,0.05])

    rotate_point_and_draw(x+17, y-16,5,x+10,y-16,[0.758,0.05,0.05])
    rotate_point_and_draw(x+17, y-16,6,x+17,y-10,[0.758,0.35,0.35])

    # Head Outline
    rotate_point_and_draw(x+20,y+20,4,x-20,y+20,[0.094,0.086,0.066])
    rotate_point_and_draw(x+20,y+20,4,x+20,y-20,[0.094,0.086,0.066]) 
    rotate_point_and_draw(x-20, y+20,4,x-20,y-20,[0.094,0.086,0.066])
    rotate_point_and_draw(x-20, y-20,4,x+20,y-20,[0.094,0.086,0.066])


        
  
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
    generate_floor(screen_h, screen_w)
    zombie1 = Player(150, 250, rotation=0)
    zombie2 = Zombie(300, 200, rotation=0)
    zombie3 = Special_Zombie(556, 200, rotation=180)
    zombie4 = Player(150, 650, rotation=90)
    zombie5 = Player(550, 550, rotation=215)
    # draw_zombie(zombie1)
    draw_zombie(zombie2)
    draw_special_zombie(zombie3)
    draw_player(zombie1)
    draw_player(zombie4)
    draw_player(zombie5)
    # draw_zombie(zombie3)
    # draw_zombie(zombie4)
    # draw_zombie(zombie5)
    glutSwapBuffers()
def iterate():
    global screen_h, screen_w
    glViewport(0, 0, screen_w, screen_h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, screen_w, 0.0, screen_h, 0, 1.0) 
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
glutInit()
glutInitWindowSize(screen_w, screen_h)
glutInitWindowPosition(200,20)
glutInitDisplayMode(GLUT_RGBA)
glutCreateWindow(b"Zombified: Shooter Game")


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