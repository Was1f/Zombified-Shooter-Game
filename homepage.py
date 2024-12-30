from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables
screen_w, screen_h = 840, 740
is_home_page_running = True
get_highscore = 0  # Temporary high score value
difficulty = "Easy"  # Initial difficulty
hovered_option = False
clicked_option = False  # Track clicked option

# Mouse hover detection
options = {
    "play": (0.3, 0.5),
    "difficulty": (0.44, 0.4),
    "exit": (0.3, 0.3)
}

def is_hovered(x, y, opt_x, opt_y):
    rect_w, rect_h = 0.2 * screen_w, 0.07 * screen_h
    return opt_x * screen_w <= x <= opt_x * screen_w + rect_w and opt_y * screen_h <= y <= opt_y * screen_h + rect_h

# Render text
def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, scale=2.0):
    glPushMatrix()
    glRasterPos2f(x, y)
    glPixelZoom(scale, scale)  # Scale bitmap text
    for char in text:
        glutBitmapCharacter(font, ord(char))
    glPixelZoom(1.0, 1.0)  # Reset scale
    glPopMatrix()

# Draw button with hover effect and clicked state
def draw_button(x, y, text, is_hovered, is_clicked):
    rect_w, rect_h = 0.2 * screen_w, 0.07 * screen_h
    # Change button color based on hover and click state
    if is_clicked:
        glColor3f(0, 0.6, 0)
    elif is_hovered:
        glColor3f(0, 1.0, 0)
    else:
        glColor3f(1, 1, 1)

    # Draw the button text
    text_x = x * screen_w + (rect_w - len(text) * 10 * 2) / 2  # Center text horizontally
    render_text(text_x, y * screen_h + 0.02 * screen_h, text)

# Draw home page
def draw_home_page():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw title
    glColor3f(1, 0, 0)  # Red
    render_text(0.42 * screen_w, 0.8 * screen_h, "ZOMBIFY", GLUT_BITMAP_HELVETICA_18, scale=2.0)

    # Draw high score
    glColor3f(1, 0.65, 0)  #orange
    render_text(0.35 * screen_w, 0.6 * screen_h, f"High Score: {get_highscore}", scale=2.0)

    # Draw buttons
    draw_button(0.3, 0.5, "PLAY", hovered_option == "play", clicked_option == "play")
    draw_button(0.44, 0.4, f"Difficulty: {difficulty}", hovered_option == "difficulty", clicked_option == "difficulty")
    draw_button(0.3, 0.3, "EXIT", hovered_option == "exit", clicked_option == "exit")

    glutSwapBuffers()

# Mouse click handler
def mouse_click(button, state, x, y):
    global is_home_page_running, difficulty, clicked_option
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        normalized_x, normalized_y = x, screen_h - y
        for option, (opt_x, opt_y) in options.items():
            if is_hovered(normalized_x, normalized_y, opt_x, opt_y):
                clicked_option = option  # Set the clicked option
                if option == "play":
                    is_home_page_running = False
                elif option == "difficulty":
                    difficulty = "Medium" if difficulty == "Easy" else "Hard" if difficulty == "Medium" else "Easy"
                elif option == "exit":
                    is_home_page_running = False
                    glutLeaveMainLoop()

# Mouse motion handler
def mouse_motion(x, y):
    global hovered_option
    normalized_x, normalized_y = x, screen_h - y
    hovered_option = None
    for option, (opt_x, opt_y) in options.items():
        if is_hovered(normalized_x, normalized_y, opt_x, opt_y):
            hovered_option = option
            break

# Display callback
def display():
    if is_home_page_running:
        draw_home_page()
    else:
        glClear(GL_COLOR_BUFFER_BIT)
        render_text(0.3 * screen_w, 0.5 * screen_h, "Game Page Coming Soon!", scale=2.0)
        glutSwapBuffers()

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
    glutCreateWindow(b"ZOMBIFY Home Page")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse_click)
    glutPassiveMotionFunc(mouse_motion)
    glutMainLoop()

if __name__ == "__main__":
    main()
