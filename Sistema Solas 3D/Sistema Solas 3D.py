import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

rotate_x = 0
rotate_y = 0
dragging = False
drag_start = (0, 0)

def load_texture(image):
    texture_surface = pygame.image.load(image)
    texture_data = pygame.image.tostring(texture_surface, 'RGBA', True)
    
    width, height = texture_surface.get_rect().size
    
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture

def load_background_texture(image):
    texture_surface = pygame.image.load(image)
    texture_data = pygame.image.tostring(texture_surface, 'RGBA', True)
    
    width, height = texture_surface.get_rect().size
    
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture

def draw_background(texture):
    glPushMatrix()
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, -1)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, -1)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def draw_sphere(color, radius, slices, stacks, texture=None):
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glColor3fv(color)
    gluSphere(quadric, radius, slices, stacks)
    
    glDisable(GL_TEXTURE_2D)

def draw_saturn_rings(inner_radius, outer_radius, slices, texture, rotation_angle):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor3fv((1, 1, 1))
    
    glPushMatrix()
    glRotatef(rotation_angle, 0, 0, 1)
    glBegin(GL_QUADS)
    for i in range(slices):
        angle1 = 2 * math.pi * (i / slices)
        angle2 = 2 * math.pi * ((i + 1) / slices)
        
        x1 = inner_radius * math.cos(angle1)
        y1 = inner_radius * math.sin(angle1)
        x2 = outer_radius * math.cos(angle1)
        y2 = outer_radius * math.sin(angle1)
        
        x3 = outer_radius * math.cos(angle2)
        y3 = outer_radius * math.sin(angle2)
        x4 = inner_radius * math.cos(angle2)
        y4 = inner_radius * math.sin(angle2)
        
        glTexCoord2f(0, 0)
        glVertex3f(x1, y1, 0)
        glTexCoord2f(1, 0)
        glVertex3f(x2, y2, 0)
        glTexCoord2f(1, 1)
        glVertex3f(x3, y3, 0)
        glTexCoord2f(0, 1)
        glVertex3f(x4, y4, 0)
    
    glEnd()
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D)

def draw_planet(orbit_radius, color, radius, texture, rotation_angle, draw_rings=False, ring_texture=None):
    glPushMatrix()
    glRotatef(rotation_angle, 0, 0, 1)
    glTranslatef(orbit_radius, 0, 0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor3fv(color)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, 30, 30)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    if draw_rings and ring_texture:
        draw_saturn_rings(0.3, 0.5, 200, ring_texture, rotation_angle)

def open_planet_window(planet_texture, background_texture):
    pygame.init()
    display = (1200, 1200)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                handle_mouse_events(event)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)

        draw_background(background_texture)
        draw_sphere((1, 1, 1), 0.2, 30, 30, texture=planet_texture)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

def handle_mouse_events(event):
    global dragging, drag_start, earth_rotation, mars_rotation, jupiter_rotation, saturn_rotation, urano_rotation, neptuno_rotation, sun_rotation
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        dragging = True
        drag_start = pygame.mouse.get_pos()
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
        dragging = False
    elif event.type == pygame.MOUSEMOTION and dragging:
        delta_x, delta_y = pygame.mouse.get_pos()[0] - drag_start[0], pygame.mouse.get_pos()[1] - drag_start[1]
        earth_rotation += delta_y * 0.2
        mars_rotation += delta_y * 0.2
        jupiter_rotation += delta_y * 0.2
        saturn_rotation += delta_y * 0.2
        urano_rotation += delta_y * 0.2
        neptuno_rotation += delta_y * 0.2
        sun_rotation += delta_y * 0.2
        drag_start = pygame.mouse.get_pos()

# Inicializar variables de rotación
earth_rotation = 0
mars_rotation = 0
jupiter_rotation = 0
saturn_rotation = 0
urano_rotation = 0
neptuno_rotation = 0
sun_rotation = 0

def setup_light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    light_position = [0.0, 0.0, -10.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.01)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.001)

def draw_sun_with_light(sun_texture, sun_rotation):
    glPushMatrix()
    glRotatef(sun_rotation, 0, 0, 1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, sun_texture)
    glColor3fv((1, 1, 0))
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, 5, 50, 50)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def main():
    global rotate_x, rotate_y, dragging, earth_rotation, mars_rotation, jupiter_rotation, saturn_rotation, urano_rotation, neptuno_rotation, sun_rotation
    pygame.init()
    display = (1366, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)

    earth_texture = load_texture("earth_texture.jpg")
    mars_texture = load_texture("mars_texture.png")
    saturn_ring_texture = load_texture("saturn_ring_texture.png")
    sun_texture = load_texture("sun_texture.jpg")
    jupiter_texture = load_texture("jupiter_texture.jpg")
    urano_texture = load_texture("urano_texture.jpg")
    neptuno_texture = load_texture("neptuno_texture.jpg")

    earth_orbit_radius = 2
    mars_orbit_radius = 4
    jupiter_orbit_radius = 6
    saturn_orbit_radius = 8
    urano_orbit_radius = 9
    neptuno_orbit_radius = 10

    background_texture = load_background_texture("galaxy_texture.jpg")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                handle_mouse_events(event)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Incrementar las rotaciones
        earth_rotation += 1
        mars_rotation += 0.5
        jupiter_rotation += 0.2
        saturn_rotation += 0.1
        urano_rotation += 0.05
        neptuno_rotation += 0.03
        sun_rotation += 0.1

        setup_light()
        draw_sun_with_light(sun_texture, sun_rotation)

        draw_planet(earth_orbit_radius, (1, 1, 1), 0.5, earth_texture, earth_rotation, draw_rings=False)
        draw_planet(mars_orbit_radius, (1, 1, 1), 0.3, mars_texture, mars_rotation, draw_rings=False)
        draw_planet(jupiter_orbit_radius, (1, 0.5, 0), 0.7, jupiter_texture, jupiter_rotation, draw_rings=False)
        draw_planet(saturn_orbit_radius, (1, 1, 0.7), 0.6, saturn_ring_texture, saturn_rotation, draw_rings=True, ring_texture=saturn_ring_texture)
        draw_planet(urano_orbit_radius, (0, 0.5, 0.5), 0.5, urano_texture, urano_rotation, draw_rings=False)
        draw_planet(neptuno_orbit_radius, (0, 0, 0.5), 0.5, neptuno_texture, neptuno_rotation, draw_rings=False)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()