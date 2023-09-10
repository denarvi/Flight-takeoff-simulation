import numpy as np
from math import *
import os
if os.environ.get('DISPLAY') is None:
    import matplotlib

    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# this function gets called every time a new frame should be generated.


def animate_takeoff(frame_number):
    global tx, ty, tz, beta, alpha, gamma
# increasing Alpha makes it go up in a circle - | 
# Increasing beta makes the body turn upside down
# Increasing gamma makes it take a turn

# The following 3 blocks are meant to showcase the plane accelerating
# on the runaway.
    if frame_number < 10:
        x = 0
        y = 2.5
        z = 0
    elif(frame_number >=10 and frame_number <= 20):
        x = 0
        y = 4
        z = 0
    elif(frame_number > 20 and frame_number <= 30):
        x = 0
        y = 6
        z = 0
# The following block shows the plane ascending. It ascends to about 7.5 degrees.
# before stabilising at that angle and continuing its elevation.
    elif (frame_number > 30 and frame_number <= 45):
        x = 0
        y = 7
        z = 8
        #alpha+= pi/360
    elif (frame_number > 45 and frame_number <= 60):
        x = 0
        y = 7
        z = 4
        #alpha-= pi/180
# The plane then tilts down to its neutral position while moving along the runway.
    elif (frame_number >60 and frame_number <= 80):
        x = 0
        y = 8
        z = 0
        #alpha-=pi/480
# First right turn
    elif (frame_number >80 and frame_number <= 100):
        #print("now", frame_number)
        #print(alpha)
        x = -2
        y = 6
        z = 0 
        gamma -= pi/40 #right is minus
        #beta += pi/240 #tilting the plane by about 15 degrees
# Flying in that direction for some time.
    elif(frame_number > 100 and frame_number <= 130):
        x = -5
        y = 0
        z = 0
        #beta -= pi/360
# Second right turn
    elif(frame_number > 130 and frame_number <= 150):
        x = -2
        y = -6
        z = 0
        #beta += pi/240
        gamma -= pi/40
    elif(frame_number > 150 and frame_number <= 180):
        y = -10
        z = 0
        x = 0
        #beta -= pi/360
# Third right turn
    elif(frame_number > 180 and frame_number <= 200):
        y = -9.75
        x = 2
        z = 0
        gamma -= pi/40
        #beta += pi/240
    elif(frame_number > 200 and frame_number <= 230):
        x = 5
        y = 0
        z = 0
        #beta -= pi/360
# fourth right turn
    elif(frame_number > 230 and frame_number <= 250):
        x = 2
        y = 6
        z = 0
        gamma -= pi/40
        #beta += pi/240
    elif(frame_number > 250 and frame_number <= 280):
        y = 6
        x = 0
        z = 0
        #beta -= pi/360
# The next 4 blocks simulate the landing of the plane. 
    elif(frame_number >280 and frame_number <= 290):
        y = 7.5
        z = -8
        x = 0
        alpha-= pi/180
    elif(frame_number >290 and frame_number <= 300):
        y = 7.5
        z = -5
        x = 0
        alpha+= pi/180
    elif(frame_number >300 and frame_number <= 310):
        y = 7.5
        z = -5
        x = 0
    elif(frame_number >310 and frame_number <= 325):
        x =0
        y = 4
        z =0
        

    # Move camera along runway
    tx += x
    ty += y

    # Increase altitude
    tz -= z
    bet = np.array(
        [[np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]])
    alp = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
    ])
    gam = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])
    
    # apply rotation matrix to 3D points
    rotation_matrix = alp @ bet @ gam
    
    # apply projection matrix to rotated 3D points
    f = 0.002
    focus = np.array([
        [f, 0, 0],
        [0, f, 0],
        [0, 0, 1]
    ])
    camera = np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz]
     ])
    projection_matrix =  focus @ rotation_matrix @ camera
    
    pr=[]
    pc=[]
    for pts in pts3:
        point = pts.copy()
        point.append(1)
        point = np.array(point)
        point = point[:, np.newaxis]
        point = projection_matrix @ point
        point[2] = point[2] if point[2][0] > 0 else 0.0001
        pr += [ (point[0]) / (point[2]) ]
        pc += [ (point[1]) / (point[2]) ]

    plt.cla()
    plt.gca().set_xlim([-0.002,0.002])
    plt.gca().set_ylim([-0.002,0.002])
    line, = plt.plot(pr, pc, 'k',  linestyle="", marker=".", markersize=2)

    
    return line,



# load in 3d point cloud
with open("airport.pts", "r") as f:
    pts3 = [ [ float(x) for x in l.split(" ") ] for l in f.readlines() ]

# initialize intrinsic and extrinsic parameters
f = 0.002  # focal length
(tx, ty, tz) = (0, 0, -5)
(alpha, beta, gamma) = (-pi/2, 0, 0)


# create animation!
fig, ax = plt.subplots()
frame_count = 325
ani = animation.FuncAnimation(fig, animate_takeoff, frames=range(frame_count))

ani.save('takeoff.mp4', writer='ffmpeg')

