import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
t = np.arange(0.0, np.pi, 0.01)
s1 = np.cos(t) + np.sin(t)
s2 = 4*np.cos(t) + 4*np.sin(t)

fig, ax = plt.subplots()
ax.plot(t, s1)
ax.plot(t, s2)

ax.set(xlabel='Angle:$\\theta$', ylabel='Diameter:r',
       title=' ')
ax.grid()

fig.savefig("极坐标霍夫变换.jpg")
plt.show() 