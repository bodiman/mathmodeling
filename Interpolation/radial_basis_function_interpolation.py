import numpy as np
from scipy.spatial import Delaunay
from scipy.interpolate import Rbf

import matplotlib.pyplot as plt
import pandas as pd

# Generate some random data points
data = pd.read_csv("lakecoords.csv")
x = np.array(data["X"])
y = np.array(data["Y"])
z = np.array(data["Z"])

perimx = x[7:]
perimy = y[7:]
perimz = z[7:]



# Create a Rbf interpolator
interp = Rbf(x, y, z)

# Define the points where you want to interpolate


x_interp = np.linspace(0, 42, 42)
y_interp = np.linspace(0, 30, 30)
x_grid, y_grid = np.meshgrid(x_interp, y_interp)
x_interp, y_interp = (x_grid.flatten(), y_grid.flatten())

# Perform the interpolation
z_interp = interp(x_interp, y_interp).reshape(30, 42)

# print(z_interp.reshape(30, 40))

plt.matshow(z_interp)
plt.colorbar()
plt.scatter(perimx, perimy)
plt.show()
plt.show()

# # Now, z_interp contains the interpolated values at the specified points

