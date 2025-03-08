#import stuff
import pygame
import numpy as np
from math import *

pygame.init()

#define colors
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
GREEN = (0,255,0)
PURPLE = (255,0,255)
YELLOW = (0,255,255)
COLORS = [BLUE, RED, BLACK, GREEN, PURPLE, YELLOW]


#set up display
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("CUBE")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#how big the cube is
scale = 100

#center position
circle_pos = [WIDTH/2,HEIGHT/2]

#how much the cube is rotated
angle_x = 0
angle_y = 0
angle_z = 0

#the change of angle per cycle
angle_change_x = 0.05
angle_change_y = 0.05
angle_change_z = 0.05

#define cube
points = []

#8 points in a cube, center 0,0,0
points.append(np.matrix([-1,-1,1]))
points.append(np.matrix([1,-1,1])) 
points.append(np.matrix([1,1,1])) 
points.append(np.matrix([-1,1,1])) 
points.append(np.matrix([-1,-1,-1])) 
points.append(np.matrix([1,-1,-1])) 
points.append(np.matrix([1,1,-1])) 
points.append(np.matrix([-1,1,-1])) 

#list of faces
faces = [[0,1,2,3], [4,5,6,7], [3,2,6,7], [0,1,5,4], [1,2,6,5], [0,4,7,3]]

#gets rid of the z direction, aka the 3rd value of a point
projection_matrix = np.matrix([
    [1,0,0],
    [0,1,0],
])

#sets up an 2 by len(points) i.e. 8 array to store the 2d projection of the cube
projected_points = [
    [n, n] for n in range(len(points))
]

#clock
clock = pygame.time.Clock()

#is a function to draw a line given the index of the point in a 2 by 8 array, the 0 is for the x value and the 1 is for the y value
def connect_points(i, j, points):
    pygame.draw.line(screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

#finds the index of the point with the highest z value given a list of points
def find_highest_point(points):
    z_coordinates = [p[2] for p in points]
    max_z = max(z_coordinates)
    index = z_coordinates.index(max_z)
    return index

#draws a face given 4 points in list
def draw_face(list, color, screen, projected_points):
    pygame.draw.polygon(screen, color, [projected_points[list[0]],projected_points[list[1]],projected_points[list[2]],projected_points[list[3]]])

#function cycle
while True:

    #fast speed means high frame rate
    clock.tick(60)

    #checks for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    #gets key press
    keys = pygame.key.get_pressed()

    #changes direction based on key press
    if keys[pygame.K_RIGHT]:
        angle_y += angle_change_y
    
    elif keys[pygame.K_LEFT]:
        angle_y -= angle_change_y

    elif keys[pygame.K_UP]:
        angle_x += angle_change_x

    elif keys[pygame.K_DOWN]:
        angle_x -= angle_change_x

    elif keys[pygame.K_a]:
        angle_z += angle_change_z

    elif keys[pygame.K_d]:
        angle_z -= angle_change_z

    if keys[pygame.K_w]:
        scale += 5
    elif keys[pygame.K_s]:
        scale -= 5

    #background
    screen.fill(WHITE)

    #define rotations arrays constantly with a changing angle
    rotation_z = np.matrix([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y),0, cos(angle_y)],
    ])

    rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(angle_x), -sin(angle_x)],
            [0, sin(angle_x), cos(angle_x)],
    ])

    rotated_points = []

    #iterates through every point one by one
    for point in points:

        #reshapes a point (prevents error)
        updated_point = point.reshape((3,1))

        #mutliplies the rotation matrices
        updated_point = np.dot(rotation_x, updated_point)
        updated_point = np.dot(rotation_y, updated_point)
        updated_point = np.dot(rotation_z, updated_point)

        #saves point for later when drawing faces
        rotated_points.append(updated_point)

        projected2d = np.dot(projection_matrix, updated_point)
        
        x = int(projected2d[0,0] * scale) + circle_pos[0]
        y = int(projected2d[1,0] * scale) + circle_pos[1]

        #list of all points used when drawing faces
        projected_points.append([x, y])
    
    highest_point = find_highest_point(rotated_points)

    #faces 1,2,3,4   5,6,7,8    4,3,7,8    1,2,5,6   2,3,6,7     1,5,8,4
    for i in range(len(faces)):
        if highest_point in faces[i]:
            draw_face(faces[i], COLORS[i], screen, projected_points)



    pygame.display.update()
    projected_points = []