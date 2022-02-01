import matplotlib.pyplot as plt
import numpy as np
from pendulum import DoublePendulum, Pendulum
from parameters import *
import random
import os
import shutil
from PIL import Image
from tqdm import trange


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
    if len(x) > 1:
        ax.scatter(x[1], y[1], s=S,    linewidths=2, edgecolor='black', color='orange', zorder=4)


# Main driver
# Simulation parameters
sim_length = 60    # Number of seconds to run each pendulum
FPS = 60           # Number of Frames to snap each second
dt = 1.0 / FPS     # Delta Time for updating pendulum
num_samples = 100  # How many double pendulum videos to create
num_digits = len(str(num_samples))
verbose = True     # If true, displays more info to console during runtime to show which states were used

# Pendulum parameters, Ranges indicate low/high to sample from when randomly initializing pendulums
r1 = r2 = 2.0               # Radius
angle1_range = [0, 2*PI]    # Initial angle between origin and first mass
angle2_range = [0, 2*PI]    # Initial angle between first mass and second mass

# Matplotlib Figure Specs
S = 1000     # Size of the pendulum mass markers in the plot
L = 5       # Line width of pendulum mass connectors

fig, ax = plt.subplots(1, figsize=(5, 5))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

# Create a list to store the data collected from each sample
# Rows will represent individual pendulum (axis=0)
# Columns will represent a timestep (axis=1)
# Resultant array will have shape (num_samples, num_frames)
dataset = list()

# Save snapshots of state as numpy files
for i in range(num_samples):

    # Double pendulum initialization
    a1 = random.uniform(angle1_range[0], angle1_range[1])
    # a2 = random.uniform(angle2_range[0], angle2_range[1])
    dp = Pendulum(a1, r1)

    # Create a directory to store this pendulums data
    k = 0
    index = str(i+k).zfill(num_digits)
    directory_name = os.path.join("Data", f"{index}")

    # While the directory name exists, and has files in it
    while os.path.isdir(directory_name) and len(os.listdir(directory_name)) == 0:
        # Try the next possible index
        index = str(i+k).zfill(num_digits)
        directory_name = os.path.join("Data", f"{index}")
        k += 1

    # Found a directory that is either empty or does not exist
    if not os.path.isdir(directory_name):
        # We create it only if it does not exits
        os.mkdir(directory_name)
    else:
        pass

    # Create an empty list which will store the state of the system at each time step
    pendulum_states = []

    num_frames = FPS*sim_length
    num_frames_digits = len(str(num_frames))
    for j in range(num_frames):
        # Grab state, Update state
        pos, state = dp.get_coord(), dp.get_state()
        pendulum_states.append(state)
        dp.update(dt)

        # save the state as numpy array

        # Plot current state and save image
        # plot(ax, pos)
        # fig.savefig("temp.png", dpi=15, facecolor='black')
        # im = Image.open("temp.png")
        # im_array = np.array(im)
        # np.save(os.path.join(directory_name, f"{j}".zfill(num_frames_digits)), im_array)

        # Clear the plot
        # ax.clear()

    dataset.append(pendulum_states)

# Convert the list into a numpy array
dataset = np.array(dataset)
print(f"Shape of resultant dataset: {dataset.shape}")

# Save the dataset
save = input("Would you like to save the state dataset? [Y/N]: ").lower()
if save == 'y':
    filename = input("Enter a filename: ")
    np.save(filename, dataset)

# Test loading one of the npy files and showing in matplotlib
# file = os.path.join(directory_name, f"{j}".zfill(num_frames_digits) + ".npy")
# im = np.load(file)
#
# plt.imshow(im)
# plt.show()