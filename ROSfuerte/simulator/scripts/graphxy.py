import numpy as np
import matplotlib.pyplot as plt

#chemin demande
x1 = [0.0, 2.0, 4.0, 4.0, 6.0, 4.0, 4.0, 2.0, 2.0, 4.0, 4.0, 0.0, 0.0, 0.0, -2.0, -4.0, -6.0, -6.0, 0.0] #jusqu'avant iota
y1 = [0.0, 0.0, 0.0, -4.0, -4.0, -4.0, -6.0, -6.0, -8.0, -8.0, -10.0, -10.0, -8.0, -6.0,-6.0, -6.0, -6.0, 0.0, 0.0]

#chemin simulation
x = []
mon_fichier_x = open("tracex.txt", "r")
for line in mon_fichier_x.readlines():
    x.append(float(line))

mon_fichier_x.close()

y = []
mon_fichier_y = open("tracey.txt", "r")
for line in mon_fichier_y.readlines():
    y.append(float(line))

mon_fichier_y.close()

z = []
mon_fichier_z = open("tracez.txt", "r")
for line in mon_fichier_z.readlines():
    z.append(float(line))

mon_fichier_z.close()


time = range(0, len(z))


maxi = max (len(x1), len(y1))
x1 = x1[:maxi]
y1 = y1[:maxi]
axes = plt.gca()
axes.set_xlim([-8.0, 10.0])
axes.set_ylim([-12.0, 2.0])
plt.plot(x, y, x1, y1)
plt.show()

plt.plot(time, z)
plt.show()


