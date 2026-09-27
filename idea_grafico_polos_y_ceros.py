import numpy as np
import matplotlib.pyplot as plt

np.random.seed(5)
x_poles = np.random.normal(0,1,25)
y_poles = np.random.normal(0,1,25)

np.random.seed(7)
x_zeroes = np.random.normal(0,1,25)
y_zeroes = np.random.normal(0,1,25)

fig, ax = plt.subplots()

ax.axhline(y=0, color="black", linewidth=0.8)
ax.axvline(x=0, color="black", linewidth=0.8)
ax.scatter(x_poles, y_poles, marker="x")
ax.scatter(x_zeroes, y_zeroes, marker="o" )

plt.show()

