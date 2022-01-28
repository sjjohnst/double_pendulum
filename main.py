import matplotlib.pyplot as plt
import numpy as np
from pendulum import DoublePendulum
from parameters import *
import random
import os
import shutil
from PIL import Image


# Plot the Double Pendulum state (coords) onto matplotlib axis
def plot(ax, coords):
    x, y = coords

    ax.set_xlim(-r1*2 - r1/4, r1*2 + r1/4)
    ax.set_ylim(-r1*2 - r1/4, r1*2 + r1/4)
    ax.axis("off")

    # ax.plot([0, x[0]], [0, y[0]], color='green', linewidth=L, zorder=0)
    # ax.plot(x, y, color='orange', linewidth=L, zorder=1)

    # ax.scatter(0,    0,    s=S/10, linewidths=2, edgecolor='black', color='white',  zorder=2)
    ax.scatter(x[0], y[0], s=S,    linewidths=2, edgecolor='black', color='green',  zorder=3)
    ax.scatter(x[1], y[1], s=S,    linewidths=2, edgecolor='black', color='orange', zorder=4)


# Main driver
# Simulation parameters
sim_length = 40  # Number of seconds to run each pendulum
FPS = 60        # Number of Frames to snap each second
dt = 1.0 / FPS   # Delta Time for updating pendulum
num_samples = 1  # How many double pendulum videos to initialize
num_digits = len(str(num_samples))

# Pendulum parameters, Ranges indicate low/high to sample from when randomly initializing pendulums
r1 = r2 = 2.0               # Radius
angle1_range = [0, 2*PI]    # Initial angle between origin and first mass
angle2_range = [0, 2*PI]    # Initial angle between first mass and second mass

# Matplotlib Figure Specs
S = 1000     # Size of the pendulum mass markers
L = 5       # Line width of pendulum mass connectors

fig, ax = plt.subplots(1, figsize=(5, 5))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

a1 = random.uniform(angle1_range[0], angle1_range[1])
a2 = random.uniform(angle2_range[0], angle2_range[1])
dp = DoublePendulum(a1, a2, r1, r2)

# plot(ax, dp.get_coord())
# fig.savefig("test.png", dpi=15, facecolor='black')
# im = Image.open("test.png")
# im_array = np.array(im)
# print(im_array.shape)

for i in range(num_samples):

    a1 = random.uniform(angle1_range[0], angle1_range[1])
    a2 = random.uniform(angle2_range[0], angle2_range[1])
    dp = DoublePendulum(a1, a2, r1, r2)

    index = str(i).zfill(num_digits)
    directory_name = os.path.join("Data", f"{index}")
    if not os.path.isdir(directory_name):
        # make the directory
        os.mkdir(directory_name)
    else:
        # Folder already exists, clear its data
        shutil.rmtree(directory_name)
        os.mkdir(directory_name)

    num_frames = FPS*sim_length
    num_frames_digits = len(str(num_frames))
    for j in range(num_frames):

        # Plot current state and save image
        plot(ax, dp.get_coord())
        fig.savefig("temp.png", dpi=15, facecolor='black')
        im = Image.open("temp.png")
        im_array = np.array(im)
        np.save(os.path.join(directory_name, f"{j}".zfill(num_frames_digits)), im_array)

        # Clear the plot
        ax.clear()

        # Update state
        dp.update(dt)


# Test loading one of the npy files and showing in matplotlib

file = os.path.join(directory_name, f"{j}".zfill(num_frames_digits) + ".npy")
im = np.load(file)

plt.imshow(im)
plt.show()