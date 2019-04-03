import numpy as np
import numpy.random
import matplotlib.pyplot as plt

# Generate some test data
x = np.random.randn(500)
y = np.random.randn(500)

heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)

print(heatmap.shape)
print(xedges)
print(yedges)
surf = plt.pcolormesh(xedges, yedges, heatmap)
plt.axis('image')
plt.colorbar(surf, shrink=0.75, aspect=5)
plt.savefig('test.svg', format='svg')
plt.show()

