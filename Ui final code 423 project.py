from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Global variables
screen_w, screen_h = 1280, 720
health = 100  # Example health value
current_score = 0  # Example score value
high_score = 0  # Example high score value
blood_particles = []  # For blood animation
current_difficulty = "Easy"  # Initial difficulty
paused = False

# Initialize blood particles
def init_blood_particles(count):
    global blood_particles
    blood_particles = [{"x": random.uniform(0, 1), "y": random.uniform(0.9, 1), "speed": random.uniform(0.001, 0.003)} for _ in range(count)]

# Update blood particles
def update_blood_particles():
    for particle in blood_particles:
        particle["y"] -= particle["speed"]  # Drip down
        if particle["y"] <= 0:  # Reset at the top
            particle["y"] = random.uniform(0.9, 1)
            particle["x"] = random.uniform(0, 1)

# Draw blood particles
def draw_blood_particles():
    glColor3f(0.545, 0, 0)  # Blood red
    glBegin(GL_POINTS)
    for particle in blood_particles:
        glVertex2f(particle["x"] * screen_w, particle["y"] * screen_h)
    glEnd()

# Draw health bar
def draw_health_bar():
    glColor3f(0.8, 0, 0)  # Red color
    bar_width = (health / 100) * 0.2 * screen_w
    glBegin(GL_QUADS)
    glVertex2f(0.02 * screen_w, 0.9 * screen_h)
    glVertex2f(0.02 * screen_w + bar_width, 0.9 * screen_h)
    glVertex2f(0.02 * screen_w + bar_width, 0.88 * screen_h)
    glVertex2f(0.02 * screen_w, 0.88 * screen_h)
    glEnd()

# Draw current score
def draw_current_score():
    glColor3f(1, 1, 0)  # Yellow
    glRasterPos2f(0.45 * screen_w, 0.89 * screen_h)
    for char in f"Score: {current_score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Draw high score
def draw_high_score():
    glColor3f(1, 1, 0)  # Yellow
    glRasterPos2f(0.45 * screen_w, 0.93 * screen_h)
    for char in f"High Score: {high_score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Draw pause button
def draw_pause_button():
    glColor3f(0, 0, 1)  # Blue
    glBegin(GL_QUADS)
    glVertex2f(0.85 * screen_w, 0.9 * screen_h)
    glVertex2f(0.9 * screen_w, 0.9 * screen_h)
    glVertex2f(0.9 * screen_w, 0.88 * screen_h)
    glVertex2f(0.85 * screen_w, 0.88 * screen_h)
    glEnd()
    glColor3f(1, 1, 1)
    glRasterPos2f(0.86 * screen_w, 0.885 * screen_h)
    for char in "Pause":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Draw home page
def draw_home_page():
    glClear(GL_COLOR_BUFFER_BIT)

    # Background color
    glColor3f(0.2, 0.2, 0.2)  # Dark grey
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(screen_w, 0)
    glVertex2f(screen_w, screen_h)
    glVertex2f(0, screen_h)
    glEnd()

    # Menu options
    menu_items = ["Return", "Restart", "Difficulty", "Leave"]
    colors = [(0, 1, 0), (1, 0.5, 0), (0, 0, 1), (1, 0, 0)]
    y_positions = [0.6, 0.5, 0.4, 0.3]

    for i, (item, color, y) in enumerate(zip(menu_items, colors, y_positions)):
        glColor3f(*color)
        glRasterPos2f(0.4 * screen_w, y * screen_h)
        for char in item:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Display current difficulty
    glColor3f(1, 1, 1)  # White
    glRasterPos2f(0.4 * screen_w, 0.2 * screen_h)
    for char in f"Difficulty: {current_difficulty}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glutSwapBuffers()

# Mouse click handler
def mouse_click(button, state, x, y):
    global paused, current_difficulty

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if paused:
            # Convert to normalized coordinates
            normalized_x = x / screen_w
            normalized_y = 1 - y / screen_h

            if 0.35 <= normalized_x <= 0.6:
                if 0.58 <= normalized_y <= 0.62:  # Return
                    paused = False
                elif 0.48 <= normalized_y <= 0.52:  # Restart
                    reset_game()
                elif 0.38 <= normalized_y <= 0.42:  # Difficulty
                    current_difficulty = "Medium" if current_difficulty == "Easy" else "Hard" if current_difficulty == "Medium" else "Easy"
                elif 0.28 <= normalized_y <= 0.32:  # Leave
                    exit_game()
        else:
            # Check if pause button is clicked
            normalized_x = x / screen_w
            normalized_y = 1 - (y / screen_h)
            if 0.85 <= normalized_x <= 0.9 and 0.88 <= normalized_y <= 0.9:
                paused = True

# Reset the game
def reset_game():
    global health, current_score
    health = 100
    current_score = 0
    paused = False

# Exit the game
def exit_game():
    glutLeaveMainLoop()

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    if paused:
        draw_home_page()
    else:
        draw_health_bar()
        draw_current_score()
        draw_high_score()
        draw_pause_button()
        draw_blood_particles()
    glutSwapBuffers()

# Draw a single pixel
def draw_pixel(x, y, size=2):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# Midpoint Line Algorithm
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
# def display():
#     glClear(GL_COLOR_BUFFER_BIT)
#     if paused:
#         draw_home_page()
#     else:
#         draw_health_bar()
#         draw_current_score()
#         draw_high_score()
#         draw_pause_button()
#         draw_blood_particles()
#     glutSwapBuffers()

# Main function
def main():
    global screen_w, screen_h

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(screen_w, screen_h)
    glutCreateWindow(b"Zombified Game")
    glClearColor(0, 0, 0, 1)
    gluOrtho2D(0, screen_w, 0, screen_h)

    init_blood_particles(100)

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMouseFunc(mouse_click)

    glutMainLoop()

if __name__ == "__main__":
    main()
