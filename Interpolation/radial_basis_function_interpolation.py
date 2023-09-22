import numpy as np
from scipy.spatial import Delaunay
from scipy.interpolate import Rbf

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.path import Path

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

perimx = perimx.tolist()
perimy = perimy.tolist()
perimz = perimz.tolist()

perimx = perimx + perimx[0:1]
perimy = perimy + perimy[0:1]
perimz = perimz + perimz[0:1]

perimx = np.array(perimx)
perimy = np.array(perimy)
perimz = np.array(perimz)

gridx = np.array([[x for _ in range(30)] for x in range(42)]).flatten()
gridy = np.array([[29-y for y in range(30)] for _ in range(42)]).flatten()


polygon_path = Path(np.column_stack([perimx, perimy]))
mask = polygon_path.contains_points(np.column_stack([gridx, gridy]))
mask = np.rot90(mask.reshape(42, 30).astype(float))
z_final = z_interp * mask * 10

#export as csv:
df = pd.DataFrame(z_final)
df.to_csv("lakesurface.csv")


plt.matshow(z_final)
plt.colorbar()
plt.plot(perimx, perimy, linestyle='-', color='red', label='Lines')
plt.scatter(perimx, perimy)
plt.show()

# # Now, z_interp contains the interpolated values at the specified points

