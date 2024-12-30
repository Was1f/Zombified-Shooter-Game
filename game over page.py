from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables
screen_w, screen_h = 840, 740
current_health = 100  # Placeholder for health function
current_score = 0     # Placeholder for score function
is_paused = False
is_home_page_running = True
game_over = False
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
def draw_game_over_page():
    global screen_w, screen_h

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set background color
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(screen_w, 0)
    glVertex2f(screen_w, screen_h)
    glVertex2f(0, screen_h)
    glEnd()

    # Draw "GAME OVER" text
    draw_text("GAME OVER", screen_w // 2 - 100, screen_h // 2 + 100, 1, 0.8, 0.8, 0.8)

    # Draw buttons
    draw_button("Restart", screen_w // 2 - 150, screen_h // 2 - 50, screen_w // 2 + 150, screen_h // 2)
    draw_button("Main Menu", screen_w // 2 - 150, screen_h // 2 - 150, screen_w // 2 + 150, screen_h // 2 - 100)
    draw_button("Exit", screen_w // 2 - 150, screen_h // 2 - 250, screen_w // 2 + 150, screen_h // 2 - 200)

    glutSwapBuffers()

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
    global is_home_page_running, is_paused, game_over

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = screen_h - y  # Convert to OpenGL coordinates

        # Handle clicks on the Pause Page
        if is_paused:
            # Resume button
            if screen_w // 2 - 150 <= x <= screen_w // 2 + 150 and screen_h // 2 - 50 <= y <= screen_h // 2:
                print("Resume clicked")
                is_paused = False

            # Main Menu button
            elif screen_w // 2 - 150 <= x <= screen_w // 2 + 150 and screen_h // 2 - 150 <= y <= screen_h // 2 - 100:
                print("Main Menu clicked")
                is_paused = False
                is_home_page_running = True

            # Exit button
            elif screen_w // 2 - 150 <= x <= screen_w // 2 + 150 and screen_h // 2 - 250 <= y <= screen_h // 2 - 200:
                print("Exit clicked")
                exit(0)

        # Handle clicks on the Game Over Page
        elif game_over:
            # Restart button
            if screen_w // 2 - 150 <= x <= screen_w // 2 + 150 and screen_h // 2 - 50 <= y <= screen_h // 2:
                print("Restart clicked")
                game_over = False
                restart_game()

            # Main Menu button
            elif screen_w // 2 - 150 <= x <= screen_w // 2 + 150 and screen_h // 2 - 150 <= y <= screen_h // 2 - 100:
                print("Main Menu clicked")
                game_over = False
                is_home_page_running = True

            # Exit button
            elif screen_w // 2 - 150 <= x <= screen_w // 2 + 150 and screen_h // 2 - 250 <= y <= screen_h // 2 - 200:
                print("Exit clicked")
                exit(0)

        # Handle clicks on the Home Page
        elif is_home_page_running:
            # Implement logic for buttons on the home page
            pass

        # Handle in-game buttons (e.g., Pause button)
        else:
            # Assume a pause button at a specific location
            if 10 <= x <= 60 and screen_h - 60 <= y <= screen_h - 10:
                print("Pause clicked")
                is_paused = True  # Debug


# Display callback
def display():
    if is_home_page_running:
        draw_home_page()
    elif is_paused:
        draw_pause_page()
    elif game_over:
        draw_game_over_page()
    else:
        draw_game_page()  # Swap buffers to display the updated frame

def restart_game():
    global is_home_page_running, game_over, is_paused
    # Reset game variables here
    print("Game restarted!")
    is_paused = False
def draw_button(label, x1, y1, x2, y2):
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()
    draw_text(label, (x1 + x2) // 2 - len(label) * 5, (y1 + y2) // 2 - 5, 1, 1, 1, 1)
def draw_text(text, x, y, scale, r, g, b):
    glColor3f(r, g, b)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

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
    global screen_w, screen_h
    screen_w, screen_h = 800, 600
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(screen_w, screen_h)
    glutCreateWindow("Game")
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMouseFunc(mouse)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, screen_w, 0, screen_h)
    glutMainLoop()




if __name__ == "__main__":
    main()
