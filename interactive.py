import pygame
import numpy as np
import math
from math import sin, cos
pygame.init()

WIDTH, HEIGHT = 1800, 1200
WHITE = (255, 255, 255)
GREEN = (0,255,0)
BLACK = (0,0,0)

pygame.display.set_caption("4D Tesseract Double Rotation")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

scale = 0
points_4d = [np.matrix([[x], [y], [z], [w]]) for x in (-1, 1) for y in (-1, 1)
             for z in (-1, 1) for w in (-1, 1)]
scale = 400
# Rotation matrices
def rotate_4d_yw_xz(point, angle):
    rot = np.matrix([
        [cos(angle), 0, -sin(angle), 0],
        [0, cos(angle), 0, -sin(angle)],
        [sin(angle), 0, cos(angle), 0],
        [0, sin(angle), 0, cos(angle)]

    ])
    return rot @ point
def rotate_4d_zw(point, angle): # i named this function way too early but its fine
    # Rotate in ZW + Xy plane
    rot = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, cos(angle), -sin(angle)],
    [0, 0, sin(angle), cos(angle)]
    ])
    return rot @ point
    #note to self: @ symbol is just matmul or dot
def rotate_4d_zw_xy(point, angle): # i named this function way too early but its fine
    # Rotate in ZW + Xy plane
    rot = np.matrix([
    [cos(angle), -sin(angle), 0, 0],
    [sin(angle), cos(angle), 0, 0],
    [0, 0, cos(angle), -sin(angle)],
    [0, 0, sin(angle), cos(angle)]
    ])
    return rot @ point
def rotate_4d_xw(point, angle):
    rot = np.matrix([
        [cos(angle), 0, 0, -sin(angle)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [sin(angle), 0, 0, cos(angle)]

    ])
    return rot @ point
def rotate_4d_xw_yz(point, angle):
    rot = np.matrix([
        [cos(angle), 0, 0, -sin(angle)],
        [0, cos(angle), -sin(angle), 0],
        [0, sin(angle), cos(angle), 0],
        [sin(angle), 0, 0, cos(angle)]

    ])
    return rot @ point
def rotate_4d_yw(point, angle):
    rot = np.matrix([
        [1, 0, 0, 0],
        [0, cos(angle), 0, -sin(angle)],
        [0, 0, 1, 0],
        [0, sin(angle), 0, cos(angle)]

    ])
    return rot @ point
def rotate_4d_yw_xz(point, angle):
    rot = np.matrix([
        [cos(angle), 0, -sin(angle), 0],
        [0, cos(angle), 0, -sin(angle)],
        [sin(angle), 0, cos(angle), 0],
        [0, sin(angle), 0, cos(angle)]

    ])
    return rot @ point
def rotate_4d_yz(point, angle):
    rot = np.matrix([
        [1, 0, 0, 0],
        [0, cos(angle), -sin(angle), 0],
        [0, sin(angle), cos(angle), 0],
        [0, 0, 0, 1]
    ])
    return rot @ point
def rotate_4d_xz(point, angle):
    rot = np.matrix([
        [cos(angle), 0, -sin(angle), 0],
        [0,          1, 0,           0],
        [sin(angle), 0,  cos(angle), 0],
        [0,          0, 0,           1]
    ])
    return rot @ point
def rotate_3d_y(point, angle):
    # initial y rotation
    rot = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])
    return rot @ point

def rotate_3d_x(point, angle):
    # initial x rotation
    rot = np.matrix([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])
    return rot @ point
# Actual edge logic
def generate_edges(points): 
    edges = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            diff = np.abs(points[i] - points[j]).flatten()
            if np.count_nonzero(diff) == 1 and np.all((diff == 2) | (diff == 0)):
                edges.append((i, j))
    return edges

# projection from 4D down to 2D
def project_point(point4d, angle3d_x=0.8, angle3d_y=0.6):
    # 4D to 3D
    distance = 3
    
    w = 1 / (distance - point4d[3, 0]) if distance - point4d[3, 0] != 0 else 1
    #w = 1
    projection_3d = np.matrix([
        [w, 0, 0, 0],
        [0, w, 0, 0],
        [0, 0, w, 0],
    ])
    point3d = projection_3d @ point4d

    # rotate at beginning cause it looks better
    point3d = rotate_3d_y(point3d, angle3d_y)
    point3d = rotate_3d_x(point3d, angle3d_x)

    # 3d to 2d
    projection_2d = np.matrix([
        [1, 0, 0],
        [0, 1, 0]
    ])
    point2d = projection_2d @ point3d
    return point2d

# connect points logic
def connect_points(i, j, points):
    pygame.draw.line(screen, GREEN, points[i], points[j], scale//100)

angle_zw = 0
angle_xw = 0
angle_yw = 0
angle_zw_xy = 0
angle_yz = 0
angle_yw_xz = 0
angle_xw_yz = 0
angle_xz = 0
edges = generate_edges(points_4d)
while True:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    keys = pygame.key.get_pressed()
    # the interactive part
    if keys[pygame.K_d]:
        if not (keys[pygame.K_q]):
            angle_zw +=0.02
        else:
            angle_zw_xy += 0.02

    if keys[pygame.K_a]:
        if not (keys[pygame.K_q]):
            angle_zw -=0.02
        else:
            angle_zw_xy-=0.02
    if keys[pygame.K_w]:
        if not (keys[pygame.K_q]):
            angle_xw +=0.02
        else:
            angle_xw_yz+=0.02
    if keys[pygame.K_s]:
        if not (keys[pygame.K_q]):
            angle_xw -=0.02
        else:
            angle_xw_yz-=0.02
    if keys[pygame.K_DOWN]:
        angle_yz +=0.02
    if keys[pygame.K_UP]:
        angle_yz -=0.02
    if keys[pygame.K_LEFT]:
        angle_xz +=0.02
    if keys[pygame.K_RIGHT]:
        angle_xz -=0.02
    if keys[pygame.K_z]:
        if not keys[pygame.K_q]:
            angle_yw += 0.02
        else:
            angle_yw_xz += 0.02
    if keys[pygame.K_c]:
        if not keys[pygame.K_q]:
            angle_yw -= 0.02
        else:
            angle_yw_xz -= 0.02
    projected_points = []
    # brace yourself for this messy code
    for point in points_4d:
        rotated4d = rotate_4d_zw(point, angle_zw)
        rotated4d = rotate_4d_xw(rotated4d, angle_xw)
        rotated4d = rotate_4d_yw(rotated4d, angle_yw)
        rotated4d = rotate_4d_zw_xy(rotated4d, angle_zw_xy)
        rotated4d = rotate_4d_yz(rotated4d, angle_yz)
        rotated4d = rotate_4d_yw_xz(rotated4d, angle_yw_xz)
        rotated4d = rotate_4d_xw_yz(rotated4d, angle_xw_yz)
        rotated4d = rotate_4d_xz(rotated4d, angle_xz)
        projected2d = project_point(rotated4d)
        x = int(projected2d[0, 0] * scale) + WIDTH // 2
        y = int(projected2d[1, 0] * scale) + HEIGHT // 2
        projected_points.append((x, y))
        pygame.draw.circle(screen, GREEN, (x, y), scale//50)

    # Edge connection
    for i,j in edges:
        connect_points(i, j, projected_points)

    
    pygame.display.update()
