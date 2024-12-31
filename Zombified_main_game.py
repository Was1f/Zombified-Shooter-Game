
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import numpy as np
import time
import math

# Global Variables
screen_w= 640
screen_h= 540
current_health=50
get_highscore = 0
current_score = 0   
is_paused = False
gameover=False
difficulty_level = "Easy"
bullet_list=[]
is_home_page_running = True

tiles_iteration_list=[] #Stores random variation values so the floor doesn't change during gameplay
#initializing the tiles variation list
for _ in range(0,screen_w*screen_h,1000):
    tiles_iteration_list.append(random.randint(1,50))


TARGET_FPS=30
FRAME_TIME= 1/TARGET_FPS
last_time = time.time()
############################################################################################################
##-------------------------------------------##
#classes

class Zombie:
    def __init__(self, x, y, rotation=0):
        self.x=x
        self.y=y
        self.rotation=rotation
        self.is_attacking=False
        self.bloodactive=False
        self.timer=5
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
        self.bloodactive=False
        self.timer=5

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

class Bullet:
    def __init__(self, x, y, rotation=0, speed=10):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.speed = speed
        self.is_active = True  # to track whether the bullet is still active

    def move(self):
        # Calculate new position based on the rotation and speed
        angle_rad = math.radians(self.rotation)
        self.x += self.speed * math.cos(angle_rad)
        self.y += self.speed * math.sin(angle_rad)

    def rotate_point(self, point, angle, center):
        angle_rad = math.radians(angle)
        x, y = point
        cx, cy = center
        x -= cx
        y -= cy
        x_new = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        y_new = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        return (x_new + cx, y_new + cy)

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
    draw_pixel(160,480,200)
    draw_pixel(360,480,200)
    draw_pixel(560,480,200)

    draw_pixel(65,375,10)
    glDisable(GL_BLEND)  


def draw_bullet(bullet):
    x, y=bullet.x, bullet.y
    rotation=bullet.rotation

    def rotate_point_and_draw(x1, y1, size, x2, y2, color):
        point1=[x1, y1]
        point2=[x2, y2]
        center=[x, y]
        p1=bullet.rotate_point(point1,rotation,center)
        p2=bullet.rotate_point(point2,rotation,center)
        glColor3f(color[0], color[1], color[2])
        mp_line_algo(p1[0], p1[1], p2[0], p2[1], size)

    rotate_point_and_draw(x,y,4,x +10,y,[1,0,0])  # red bullet line

    rotate_point_and_draw(x,y,2,x+10,y,[0.7, 0.2, 0.2])  # outline for bullet

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

def blood_splatter(position):
    dominant_red=[1,0.2,0]
    darker_red_1=[0.85, 0.1, 0.1]
    darker_red_2=[0.75, 0, 0]
    colors=[dominant_red]*10+[darker_red_1, darker_red_2] 
    x,y=position
    glColor3fv(dominant_red)
    draw_pixel(x,y,10)
    distance=[2,3,4,5,6,7,8,9,10,9,8,7,22,6,4,3,2,5,3,4,9,12,15,13,14,25,20,25,21,22,27,25,25,9,32,26,15,15,16,16,17,29,12,12,13,13,14,14,15,8,8,7,7,9,9,4,3,2,2,14,5,6]
    for i in range(1,60): 
        angle=random.uniform(0,2*math.pi)
        
        coin_toss=random.uniform(0,1)
        if coin_toss==1:
            scatter_x=x+int(math.cos(angle)*distance[i])
            scatter_y=y+int(math.sin(angle)*distance[i])
        else:
            scatter_x=x-int(math.cos(angle)*distance[i])
            scatter_y=y-int(math.sin(angle)*distance[i])
        droplet_size=random.randint(2,10)
        blood_shade=random.choice(colors)
        glColor3fv(blood_shade)
        draw_pixel(scatter_x, scatter_y,droplet_size)


def trigger_blood_splatter(splatter):
    #if zombie.bloodactive:
        #for _ in range(1): 
            #blood_splatter((zombie.x,zombie.y))
    for _ in range(1):
        blood_splatter((splatter.x,splatter.y))


def checkIfCollision(object,player,type):
    if type!="bullettype":
        player_min_x=player.x-35
        player_max_x=player.x+33
        player_min_y=player.y-20
        player_max_y=player.y+70
    else:
        object_min_x=object.x
        object_max_x=object.x+10
        object_min_y=object.y
        object_max_y=object.y+10

        player_min_x=player.x-35
        player_max_x=player.x+33
        player_min_y=player.y-20
        player_max_y=player.y+70

    if type=="normalzombie":
        object_min_x=object.x-35
        object_max_x=object.x+35
        object_min_y=object.y-20
        object_max_y=object.y+45
    elif type=="specialzombie":
        object_min_x=object.x-60
        object_max_x=object.x+60
        object_min_y=object.y-30
        object_max_y=object.y+67.5

    if player_max_x>=object_min_x and player_min_x<=object_max_x:
        if player_max_y>=object_min_y and player_min_y<=object_max_y:
            return True 

    return False
    
def update_zombie_pos(zombie,player,speed=10):
    direction_x=player.x-zombie.x
    direction_y=player.y-zombie.y
    distance=math.sqrt(direction_x**2+direction_y**2)
    if distance>0:
        direction_x/=distance
        direction_y/=distance
    zombie.x+=direction_x*speed
    zombie.y+=direction_y*speed
    #updating rotation here
    zombie.rotation=math.degrees(math.atan2(direction_y, direction_x))-90 
  
############################################################################################################
#main function
count=0
specialcount=0
current_score=0
splatter=[]
splatter_time=0
def mainfunc_animate():
    global player_shooter,zombies,special_zombies, current_health, is_paused, gameover, last_time,bullet_list, is_home_page_running,count,specialcount,current_score,splatter_time
    if difficulty_level=="Easy":
        z=2
        s=1
    elif difficulty_level=="Medium":
        z=4
        s=1
    elif difficulty_level=="Hard":
        z=5
        s=2
    if is_home_page_running==False:
        current_time=time.time()
        elapsed_time=current_time-last_time

        if elapsed_time >= FRAME_TIME:
            last_time = current_time
            splatter_time+=1
            if splatter_time>20:
                if len(splatter)>0:
                    splatter.pop(0)
                    splatter_time=0
            if difficulty_level == "Easy":
                speed = 2
                damage_combo=1
            elif difficulty_level == "Medium":
                speed = 4
                damage_combo=2
            elif difficulty_level == "Hard":
                speed = 8
                damage_combo=3
            if not is_paused:
                for i in bullet_list:
                    bulletspeed=50 
                    i.x+=bulletspeed*math.cos(math.radians(i.rotation))
                    i.y+=bulletspeed*math.sin(math.radians(i.rotation))   

                    if i.x < -20 or i.x > screen_w+20 or i.y < -40 or i.y > screen_h+40:
                        bullet_list.remove(i)     
                    for j in zombies:
                        if checkIfCollision(i,j,type="bullettype"):
                            if len(bullet_list)>0:
                                bullet_list.remove(i)
                            # print("bullet+zombie collision",count)
                            count+=1
                            if count>2:
                                splatter.append(j)
                                zombies.remove(j)
                                
                                current_score+=10*damage_combo
                                count=0
                                spawn_zombie()

                    for j in special_zombies:
                        if checkIfCollision(i,j,type="bullettype"):
                            if len(bullet_list)>0:
                                bullet_list.remove(i)
                            # print("bullet+zombie collision",current_score)
                            specialcount+=1
                            if specialcount>5:
                                splatter.append(j)
                                special_zombies.remove(j)
                                spawn_special_zombie()
                                
                                current_score+=30*damage_combo
                                specialcount=0
                for zoms in zombies:
                    update_zombie_pos(zoms,player_shooter,speed) #need to update speed accoring to difficulty level
                for sup_zoms in special_zombies:
                    update_zombie_pos(sup_zoms,player_shooter,speed)


                for i in zombies:
                    if checkIfCollision(i,player_shooter,type="normalzombie"):
                        if i.timer==0:
                            current_health-=1* damage_combo
                            # print("collision")
                            # print(current_health)
                            i.timer=5
                        else:
                            i.timer-=1
                for i in special_zombies:
                    if checkIfCollision(i,player_shooter,type='specialzombie'):
                        if i.timer==0:
                            current_health-=3* damage_combo
                            # print("Special collision")
                            # print(current_health)
                            i.timer=5
                        else:
                            i.timer-=1
            
                if current_health<=0:
                    current_health=0
                    is_home_page_running = False
                    gameover=True

        else:
            return 

    glutPostRedisplay()


############################################################################################################
#input handling functions
player_shooter = Player(425, 325, rotation=270)
# bullet=None
def keyboardListener(key,x,y):
    global player_shooter
    if not is_paused:
        if key==b'd': 
            if player_shooter.x<screen_w-120:  
                player_shooter.x+=30
                player_shooter.rotation=270
        elif key==b'a': 
            if player_shooter.x>100:
                player_shooter.x-=30
                player_shooter.rotation=90
        elif key==b'w': 
            if player_shooter.y<screen_h-160: 
                player_shooter.y+=30
                player_shooter.rotation=0
        elif key==b's': 
            if player_shooter.y>100: 
                player_shooter.y-=30
                player_shooter.rotation=180


        elif key==b'k':
            player_shooter.rotation-=20

        elif key==b'j':
            player_shooter.rotation+=20

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global player_shooter, bullet_list, screen_h, screen_w, is_paused, difficulty_level, gameover, is_home_page_running

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        screen_x = x
        screen_y = screen_h - y  
        # print(f"Mouse clicked at ({screen_x}, {screen_y})")

        if is_home_page_running:
            if 190 <= screen_x <= 450 and 261 <= screen_y <= 314:
                is_home_page_running = False
                gameover = False
                restart()
                glutPostRedisplay()
            elif 190 <= screen_x <= 450 and 200 <= screen_y <= 250:
                difficulty_levels = ["Easy", "Medium", "Hard"]
                current_index = difficulty_levels.index(difficulty_level)
                difficulty_level = difficulty_levels[(current_index + 1) % len(difficulty_levels)]
                glutPostRedisplay()
            elif 190 <= screen_x <= 450 and 160 <= screen_y <= 190 and not is_paused:
                is_home_page_running = False
                glutLeaveMainLoop()
        elif gameover:
            if 0.35 * screen_w <= screen_x <= 0.65 * screen_w:
                if 0.4 * screen_h <= screen_y <= 0.47 * screen_h:
                    is_home_page_running = True
                    gameover = False
                    glutPostRedisplay()
                elif 0.3 * screen_h <= screen_y <= 0.37 * screen_h:
                    gameover = False
                    restart()
                    glutPostRedisplay()
                elif 0.2 * screen_h <= screen_y <= 0.27 * screen_h:
                    glutLeaveMainLoop()
        else:
            if screen_y < screen_h - 60 and not is_paused:
                dx = screen_x - player_shooter.x
                dy = screen_y - player_shooter.y
                angle = math.degrees(math.atan2(dy, dx))

                bullet1 = Bullet(player_shooter.x, player_shooter.y, angle)
                if len(bullet_list) < 3:
                    bullet_list.append(bullet1)
                
                # print(f"Bullet fired at angle {angle} towards ({screen_x}, {screen_y})!")

                player_shooter.rotation = angle - 90
            else:
                if 570 <= screen_x <= 595 and 490 <= screen_y <= 510 and not is_paused:
                    is_paused = not is_paused
                    glutPostRedisplay()
            if is_paused:
                button_width, button_height = 200, 50
                spacing = 20
                base_x = (screen_w - button_width) / 2
                base_y = (screen_h - (button_height * 4 + spacing * 3)) / 2

                if base_x <= screen_x <= base_x + button_width and base_y + (button_height + spacing) * 3 <= screen_y <= base_y + (button_height + spacing) * 3 + button_height:
                    # print("Return button clicked.") 
                    is_paused = False  # Resume the game
                    glutPostRedisplay()

                elif base_x <= screen_x <= base_x + button_width and base_y + (button_height + spacing) * 2 <= screen_y <= base_y + (button_height + spacing) * 2 + button_height:
                    # print("Restart button clicked.")
                    restart()  # Restart the game
                    is_paused = False
                    glutPostRedisplay()

                elif base_x <= screen_x <= base_x + button_width and base_y + (button_height + spacing) * 1 <= screen_y <= base_y + (button_height + spacing) * 1 + button_height:
                    # print("Difficulty button clicked.")  # Debug
                    difficulty_levels = ["Easy", "Medium", "Hard"]
                    current_index = difficulty_levels.index(difficulty_level)
                    difficulty_level = difficulty_levels[(current_index + 1) % len(difficulty_levels)]
                    # call_zombie(difficulty_level)
                    glutPostRedisplay()

                elif base_x <= screen_x <= base_x + button_width and base_y <= screen_y <= base_y + button_height:
                    # print("Leave button clicked.")  # Debug
                    glutLeaveMainLoop()
############################################################################################################
#UI Functions
def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

# Draw health bar
def draw_button(x, y, width, height, label):
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    

    glColor3f(0.9, 0.7, 0.7)
    mp_line_algo(x+25, y+height/2,x+width-25, y+height/2, 50)
    

    glColor3f(0.5, 0.5, 0.5)
    mp_line_algo(x, y, x + width, y, 2)
    mp_line_algo(x + width, y, x + width, y + height, 2)
    mp_line_algo(x + width, y + height, x, y + height, 2)
    mp_line_algo(x, y + height, x, y, 2)
    
    # Draw button label
    glColor3f(0, 0, 0)  # Text color
    render_text(x + 30, y + height / 3, label)

def draw_pause_menu():
    button_width, button_height = 200, 50
    spacing = 20
    base_x = int(screen_w - button_width) / 2
    base_y = int(screen_h - (button_height * 4 + spacing * 3)) / 2
    # Draw buttons
    draw_button(base_x, base_y + (button_height + spacing) * 3, button_width, button_height, "Return")
    draw_button(base_x, base_y + (button_height + spacing) * 2, button_width, button_height, "Restart")
    draw_button(base_x, base_y + (button_height + spacing) * 1, button_width, button_height, f"Difficulty: {difficulty_level}")
    draw_button(base_x, base_y, button_width, button_height, "Leave")

def draw_health_bar(x, y, width, height, health):
    
    glColor3f(0,0.3,0.3)
    # Draw health bar outline
    mp_line_algo(x, y, x + width, y, 20)

    # Draw current health
    glColor3f(0.5,1,1)
    if health>0:
        health_width = width * (health / 100)
        mp_line_algo(x, y, x + health_width, y, 17)
    else: 
        mp_line_algo(x, y, x, y, 17)

# Draw pause icon
def draw_pause_icon(x, y, size):
    bar_width = size / 4
    spacing = bar_width / 2
    # Draw left bar
    mp_line_algo(x, y, x, y + size/1.5, bar_width)
    # Draw right bar
    mp_line_algo(x+bar_width+spacing,y,x+bar_width+spacing,y+size/1.5,bar_width)
# Draw top rectangle
def draw_top_rectangle():
    glColor3f(0, 0, 0) 
    mp_line_algo(0,screen_h-60,screen_w,screen_h-60,50)
    mp_line_algo(0,screen_h-20,screen_w,screen_h-20,50)
    # Health display
    glColor3f(0.5,1,1)
    render_text(10, screen_h-35, f"Health: {current_health}", GLUT_BITMAP_HELVETICA_18)
    # Health bar
    draw_health_bar(10, screen_h-55,200,20, current_health)
    # Score display
    glColor3f(0.5,1,1)
    render_text(350, screen_h-50, f"Score: {current_score}", GLUT_BITMAP_TIMES_ROMAN_24)
    # Pause icon
    draw_pause_icon(screen_w-60, screen_h-50,20)

def draw_gameover_screen():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1, 0, 0)
    render_text(0.4 * screen_w, 0.7 * screen_h, "GAME OVER", GLUT_BITMAP_HELVETICA_18)

    glColor3f(1, 1, 1)
    render_text(0.4 * screen_w, 0.6 * screen_h, f"Score: {current_score}", GLUT_BITMAP_HELVETICA_18)

    draw_button(0.35 * screen_w, 0.4 * screen_h, 0.3 * screen_w, 0.07 * screen_h, "MAIN MENU")
    draw_button(0.35 * screen_w, 0.3 * screen_h, 0.3 * screen_w, 0.07 * screen_h, "RESTART")
    draw_button(0.35 * screen_w, 0.2 * screen_h, 0.3 * screen_w, 0.07 * screen_h, "EXIT")

    glutSwapBuffers()
############################################################################################################ 
# initialize
#player_shooter=Player(150,250,rotation=0)
zombies=[]
special_zombies = []

def spawn_zombie():
    chooze= random.choice([0,1,2,3])
    if chooze==0:
        x=random.randint(-60,-50)
        y=random.randint(-60,screen_h+60)        
    elif chooze==1:
        x=random.randint(screen_w+60,screen_w+60)
        y=random.randint(-60,screen_h+60)
    elif chooze==2:
        x=random.randint(-40,screen_w+40)
        y=random.randint(screen_h+50,screen_h+50)
    else:
        x=random.randint(40,screen_w+40)
        y=random.randint(-60,-50)          


    rotation=calculate_rotation(x, y,player_shooter.x,player_shooter.y)
    zombies.append(Zombie(x,y,rotation))

def spawn_special_zombie():
    chooze= random.choice([0,1,2,3])
    if chooze==0:
        x=random.randint(-150,-50)
        y=random.randint(-50,screen_h+150)        
    elif chooze==1:
        x=random.randint(screen_w+50,screen_w+150)
        y=random.randint(-50,screen_h+150)
    elif chooze==2:
        x=random.randint(-50,screen_w+50)
        y=random.randint(screen_h+50,screen_h+150)
    else:
        x=random.randint(-50,screen_w+50)
        y=random.randint(-150,-50)          


    rotation = calculate_rotation(x, y, player_shooter.x, player_shooter.y)
    special_zombies.append(Special_Zombie(x, y, rotation))

# Function to calculate rotation to face the player
def calculate_rotation(zombie_x, zombie_y, player_x, player_y):
    direction_x=player_x-zombie_x
    direction_y=player_y-zombie_y
    angle=math.degrees(math.atan2(direction_y, direction_x)) #getting the slope in radians and making it in degrees
    # print(angle)
    return angle-90

def call_zombie(difficulty="Easy"):
    if difficulty=="Easy":
        z=2
        s=1
    elif difficulty=="Medium":
        z=4
        s=1
    elif difficulty=="Hard":
        z=5
        s=2
    for _ in range(z):
        spawn_zombie()
    for _ in range(s):  
        spawn_special_zombie()
call_zombie(difficulty_level)
def restart(): #need to fix this later so a fresh match starts
    global current_health, current_score, get_highscore, zombies, special_zombies,bullet_list,gameover,splatter,specialcount,count
    zombies=[]
    splatter=[]
    special_zombies=[]
    bullet_list=[]
    count=0
    specialcount=0
    gameover=False
    call_zombie()
    if current_score>get_highscore:
        get_highscore=current_score
    current_health = 100
    current_score = 0
##########################################################
#Homepage
options = {
    "play": (0.3, 0.5),
    "difficulty": (0.44, 0.4),
    "exit": (0.3, 0.3)
}
def is_hovered(x, y, opt_x, opt_y):
    rect_w, rect_h = 0.2 * screen_w, 0.07 * screen_h
    return opt_x * screen_w <= x <= opt_x * screen_w + rect_w and opt_y * screen_h <= y <= opt_y * screen_h + rect_h

hovered_option = None
clicked_option = None
def draw_home_page():
    glClear(GL_COLOR_BUFFER_BIT)

    # title
    glColor3f(1, 0, 0)
    render_text(0.42 * screen_w, 0.8 * screen_h, "ZOMBIFY", GLUT_BITMAP_HELVETICA_18)

    # high score
    glColor3f(1, 0.65, 0)
    render_text(0.35 * screen_w, 0.6 * screen_h, f"High Score: {get_highscore}")

    # Draw buttons
    draw_button(0.3 * screen_w, 0.5 * screen_h, 0.4 * screen_w, 0.07 * screen_h, "PLAY")
    draw_button(0.3 * screen_w, 0.4 * screen_h, 0.4 * screen_w, 0.07 * screen_h, f"Difficulty: {difficulty_level}")
    draw_button(0.3 * screen_w, 0.3 * screen_h, 0.4 * screen_w, 0.07 * screen_h, "EXIT")

    glutSwapBuffers()
#glui functions
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    if not is_home_page_running and not gameover:
        if is_paused:
            draw_pause_menu()
        else:
            generate_floor(screen_h, screen_w)
            for i in splatter:
                trigger_blood_splatter(i)

            for bullet in bullet_list:
                draw_bullet(bullet)
            draw_player(player_shooter)
            for zombie in zombies:
                draw_zombie(zombie)
            for special_zombie in special_zombies:
                draw_special_zombie(special_zombie)


            draw_top_rectangle()
    elif gameover:
        draw_gameover_screen()
    else:
        draw_home_page()
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


#fullscreen mode in options
# glutFullScreen()

glutDisplayFunc(display)
glutIdleFunc(mainfunc_animate)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)

glutMainLoop()
