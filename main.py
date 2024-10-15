import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Light parameters
LIGHT_AMBIENT = [0.2, 0.2, 0.2, 1.0]
LIGHT_DIFFUSE = [0.8, 0.8, 0.8, 1.0]
LIGHT_SPECULAR = [1.0, 1.0, 1.0, 1.0]
LIGHT_POSITION = [1.0, 1.0, 1.0, 0.0]

# Atom colors and configurations
NUCLEUS_COLOR = (0.5, 0.5, 1.0, 0.5)  # Light blue for the nucleus
ORBIT_COLOR = (0.5, 0.5, 1.0, 0.5)  # Light blue for the orbits
TILT_ANGLES = [-30, 30]  # Tilt angles for electron orbits
NUM_ORBITS = 3  # Number of orbits
NUCLEUS_RADIUS = 0.5  # Radius of the nucleus
ORBIT_RADIUS = 1.0  # Orbit radius

# Minimum window size
MIN_WIDTH = 400
MIN_HEIGHT = 300


# Function to initialize Pygame and OpenGL
def init_window(display_size):
    pygame.init()
    pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL | RESIZABLE)
    gluPerspective(45, (display_size[0] / display_size[1]), 0.5, 50.0)
    glTranslatef(0.0, 0.0, -5)  # Set camera distance
    glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering


# Function to setup lighting in the scene
def setup_lighting():
    glLightfv(GL_LIGHT0, GL_AMBIENT, LIGHT_AMBIENT)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LIGHT_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_SPECULAR, LIGHT_SPECULAR)
    glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


# Function to draw the nucleus
def draw_nucleus(radius, slices, stacks, color):
    quad = gluNewQuadric()
    glColor4f(*color)  # Set color for nucleus
    gluSphere(quad, radius, slices, stacks)  # Draw the sphere
    gluDeleteQuadric(quad)


# Function to draw electron orbits
def draw_electron_orbits(radius, num_orbits, tilt_angle, color):
    glColor4f(*color)  # Set orbit color
    glLineWidth(2)  # Set line thickness
    for i in range(num_orbits):
        glPushMatrix()
        glRotatef(i * (360 / num_orbits), 1, 1, 0)  # Rotate to spread orbits evenly
        glRotatef(tilt_angle, 1, 0, 1)  # Tilt each orbit layer
        glBegin(GL_LINE_LOOP)
        for j in range(100):
            theta = 2.0 * np.pi * j / 100  # Angle for each point in the orbit
            x = radius * np.cos(theta)  # X position of orbit point
            y = radius * np.sin(theta)  # Y position of orbit point
            glVertex3f(x, y, 0.0)
        glEnd()
        glPopMatrix()


# Function to adjust the viewport and projection when window is resized
def resize_window(width, height):
    if height == 0:
        height = 1  # Avoid division by zero
    glViewport(0, 0, width, height)  # Reset the viewport
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.5, 50.0)  # Adjust the perspective
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)  # Reapply the camera transformation


# Main rendering loop
def main():
    display_size = (800, 600)
    init_window(display_size)
    setup_lighting()  # Set up lighting for the scene

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == VIDEORESIZE:  # Handle window resize
                # Enforce minimum window size
                new_width = max(event.w, MIN_WIDTH)
                new_height = max(event.h, MIN_HEIGHT)

                # Resize the window and adjust the viewport
                pygame.display.set_mode((new_width, new_height), DOUBLEBUF | OPENGL | RESIZABLE)
                resize_window(new_width, new_height)  # Update viewport and perspective

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear buffers
        glRotatef(0.6, 1, 0, 0)  # Continuous rotation for a dynamic view

        # Draw the nucleus
        draw_nucleus(NUCLEUS_RADIUS, 50, 50, NUCLEUS_COLOR)

        # Draw electron orbits
        for tilt_angle in TILT_ANGLES:
            draw_electron_orbits(ORBIT_RADIUS, NUM_ORBITS, tilt_angle, ORBIT_COLOR)

        pygame.display.flip()  # Update the display
        pygame.time.wait(10)  # Delay to control frame rate


if __name__ == "__main__":
    main()
