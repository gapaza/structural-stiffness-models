import pymesh
import numpy as np
import time
from tqdm import tqdm

def generateNC(sel, sidenum):
    # Generate a vector of equally spaced notch values
    notchvec = np.linspace(0, 1, sidenum)

    # Initialize an empty list to store nodal coordinates
    NC = []

    # Nested loops to generate all combinations of notch values
    for i in range(sidenum):
        for j in range(sidenum):
            # Append the current combination to the NC list
            NC.append([notchvec[i], notchvec[j]])

    # Convert NC list to a NumPy array for easier manipulation
    NC = np.array(NC)

    # Scale the nodal coordinates by the unit cell size
    NC = sel * NC

    return NC

if __name__ == "__main__":

    sidenum = 3
    num_vars = 30
    radius = 0.1
    sidelen = 1

    NC = generateNC(sidelen, sidenum)
    CA = [
        [1, 2], # [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9],
        # [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9],
        # [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9],
        # [4, 5], [4, 6], [4, 7], [4, 8], [4, 9],
        # [5, 6], [5, 7], [5, 8], [5, 9],
        # [6, 7], [6, 8], [6, 9],
        # [7, 8], [7, 9],
        # [8, 9]
    ]  # Connectivity array

    print(NC)


    curr_time = time.time()
    global_mesh = None
    for truss_member in tqdm(CA):
        node1 = NC[truss_member[0] - 1]
        node2 = NC[truss_member[1] - 1]
        x1, y1 = node1
        x2, y2 = node2
        z1, z2 = 0.0, 0.0
        p1 = np.array([x1, y1, z1])
        p2 = np.array([x2, y2, z2])

        truss_mesh = pymesh.generate_cylinder(p1, p2, radius, radius, num_segments=32)
        if global_mesh is None:
            global_mesh = truss_mesh
        else:
            global_mesh = pymesh.boolean(global_mesh, truss_mesh, operation="union")
    print('Time taken:', time.time() - curr_time)


    print(global_mesh.volume)








