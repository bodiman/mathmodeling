import numpy as np
from scipy.spatial import Delaunay
from scipy.interpolate import NearestNDInterpolator

import matplotlib.pyplot as plt

# Generate some random data points
x = np.array([12, 14, 19, 30])
y = np.array([17, 27, 11, 15])
z = np.array([63, 1, 91, 32])

# Create a Delaunay triangulation
tri = Delaunay(np.column_stack((x, y)))

# Create a NearestNDInterpolator
interp = NearestNDInterpolator(tri, z)

# Define the points where you want to interpolate
x_interp = np.linspace(0, 40, 40)
y_interp = np.linspace(0, 30, 30)
x_grid, y_grid = np.meshgrid(x_interp, y_interp)
points_to_interpolate = np.column_stack((x_grid.flatten(), y_grid.flatten()))

# Perform the interpolation
z_interp = interp(points_to_interpolate).reshape(30, 40)

# print(z_interp.reshape(30, 40))
plt.matshow(z_interp, cmap=plt.cm.viridis)
plt.colorbar()
plt.show()

# Now, z_interp contains the interpolated values at the specified points

