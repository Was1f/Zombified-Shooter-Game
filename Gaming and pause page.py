from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables
screen_w, screen_h = 840, 740
current_health = 100  # Placeholder for health function
current_score = 0     # Placeholder for score function
is_paused = False
difficulty_level = "Easy"
def mp_line_algo(x, y, xp, yp, size=2):
    """Draws a line using the midpoint line algorithm."""
    dx = xp - x
    dy = yp - y
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    xk, yk = x, y
    glPointSize(size)
    glBegin(GL_POINTS)
    while xk <= xp:
        glVertex2f(xk, yk)
        if d > 0:
            yk += 1
            d += dNE
        else:
            d += dE
        xk += 1
    glEnd()
def midpointcircle(r, x_main, y_main, size=2):
    """Draws a circle using the midpoint circle algorithm."""
    x = 0
    y = r
    d = 1 - r
    glPointSize(size)
    glBegin(GL_POINTS)
    while x <= y:
        glVertex2f(x_main + x, y_main + y)
        glVertex2f(x_main - x, y_main + y)
        glVertex2f(x_main + x, y_main - y)
        glVertex2f(x_main - x, y_main - y)
        glVertex2f(x_main + y, y_main + x)
        glVertex2f(x_main - y, y_main + x)
        glVertex2f(x_main + y, y_main - x)
        glVertex2f(x_main - y, y_main - x)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()
def restart():
    global current_health, current_score
    current_health = 100
    current_score = 0
# Render text
def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
# Draw health bar
def draw_button(x, y, width, height, label):
    glColor3f(0.3, 0.3, 0.3)  # Button background
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    glColor3f(1, 1, 1)  # Text color
    render_text(x + 10, y + height / 4, label)
def draw_pause_menu():
    button_width, button_height = 200, 50
    spacing = 20
    base_x = (screen_w - button_width) / 2
    base_y = (screen_h - (button_height * 4 + spacing * 3)) / 2
    # Draw buttons
    draw_button(base_x, base_y + (button_height + spacing) * 3, button_width, button_height, "Return")
    draw_button(base_x, base_y + (button_height + spacing) * 2, button_width, button_height, "Restart")
    draw_button(base_x, base_y + (button_height + spacing) * 1, button_width, button_height, f"Difficulty: {difficulty_level}")
    draw_button(base_x, base_y, button_width, button_height, "Leave")
def draw_health_bar(x, y, width, height, health):
    glColor3f(1, 0, 0)  # Red for health bar background
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    glColor3f(1, 0, 0)  # Green for current health
    health_width = width * (health / 100)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + health_width, y)
    glVertex2f(x + health_width, y + height)
    glVertex2f(x, y + height)
    glEnd()
# Draw pause icon
def draw_pause_icon(x, y, size):
    bar_width = size / 4
    spacing = bar_width / 2
    glColor3f(1, 1, 1)  # White for pause icon
    glBegin(GL_QUADS)
    # Left bar
    glVertex2f(x, y)
    glVertex2f(x + bar_width, y)
    glVertex2f(x + bar_width, y + size)
    glVertex2f(x, y + size)
    # Right bar
    glVertex2f(x + bar_width + spacing, y)
    glVertex2f(x + 2 * bar_width + spacing, y)
    glVertex2f(x + 2 * bar_width + spacing, y + size)
    glVertex2f(x + bar_width + spacing, y + size)
    glEnd()
# Draw top rectangle
def draw_top_rectangle():
    glColor3f(0, 0, 0)  # Black for the rectangle
    glBegin(GL_QUADS)
    glVertex2f(0, screen_h - 80)
    glVertex2f(screen_w, screen_h - 80)
    glVertex2f(screen_w, screen_h)
    glVertex2f(0, screen_h)
    glEnd()
    # Health display
    glColor3f(0, 1, 1)  # White for text
    render_text(10, screen_h - 35, f"Health: {current_health}", GLUT_BITMAP_HELVETICA_18)

    # Health bar
    draw_health_bar(10, screen_h - 70, 200, 20, current_health)

    # Score display
    render_text(400, screen_h - 60, f"Score: {current_score}", GLUT_BITMAP_TIMES_ROMAN_24)
    # Pause icon
    draw_pause_icon(screen_w - 60, screen_h - 50, 20)
# Display callback
def keyboard(key, x, y):
    global is_paused
    if key == b'p':  # Press 'p' to toggle pause
        is_paused = not is_paused
        glutPostRedisplay()  # Update display after toggling
def mouse(button, state, x, y):
    global is_paused, difficulty_level

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert mouse coordinates to match OpenGL's system
        y = screen_h - y  # OpenGL's y-axis is inverted relative to GLUT
        print(f"Mouse clicked at ({x}, {y})")  # Debug: Print the converted coordinates
        if not is_paused :
            if 780<=x<=795 and  690<=y<=715:
                is_paused = not is_paused
                glutPostRedisplay()

        if is_paused:
            button_width, button_height = 200, 50
            spacing = 20
            base_x = (screen_w - button_width) / 2
            base_y = (screen_h - (button_height * 4 + spacing * 3)) / 2

            # Check if "Return" button is clicked
            if base_x <= x <= base_x + button_width and base_y + (button_height + spacing) * 3 <= y <= base_y + (button_height + spacing) * 3 + button_height:
                print("Return button clicked.")  # Debug
                is_paused = False  # Resume the game
                glutPostRedisplay()

            # Check if "Restart" button is clicked
            elif base_x <= x <= base_x + button_width and base_y + (button_height + spacing) * 2 <= y <= base_y + (button_height + spacing) * 2 + button_height:
                print("Restart button clicked.")  # Debug
                restart()  # Restart the game
                is_paused = False
                glutPostRedisplay()

            # Check if "Difficulty" button is clicked
            elif base_x <= x <= base_x + button_width and base_y + (button_height + spacing) * 1 <= y <= base_y + (button_height + spacing) * 1 + button_height:
                print("Difficulty button clicked.")  # Debug
                # Cycle through difficulty levels
                difficulty_levels = ["Easy", "Medium", "Hard"]
                current_index = difficulty_levels.index(difficulty_level)
                difficulty_level = difficulty_levels[(current_index + 1) % len(difficulty_levels)]
                glutPostRedisplay()

            # Check if "Leave" button is clicked
            elif base_x <= x <= base_x + button_width and base_y <= y <= base_y + button_height:
                print("Leave button clicked.")  # Debug
                glutLeaveMainLoop()  # Exit the program
        else:
            print(f"Mouse clicked outside pause menu at ({x}, {y})")  # Debug


# Display callback
def display():
    glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen once

    if is_paused:
        draw_pause_menu()  # Render pause menu when paused
    else:
        # Draw the top rectangle and contents
        draw_top_rectangle()

        # Bottom part color
        glColor3f(0.2, 0.2, 0.2)  # Dark gray for bottom part
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(screen_w, 0)
        glVertex2f(screen_w, screen_h - 80)
        glVertex2f(0, screen_h - 80)
        glEnd()

    glutSwapBuffers()  # Swap buffers to display the updated frame



# Reshape callback
def reshape(w, h):
    global screen_w, screen_h
    screen_w, screen_h = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(screen_w, screen_h)
    glutCreateWindow(b"Game Page")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)  # Keyboard callback for pausing
    glutMouseFunc(mouse)        # Mouse callback for interaction
    glutMainLoop()




if __name__ == "__main__":
    main()
