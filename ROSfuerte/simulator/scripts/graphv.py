#vitesses demandees
vx = []
mon_fichier_vx = open("tracevx.txt", "r")
for line in mon_fichier_vx.readlines():
    vx.append(float(line)*1000)

mon_fichier_vx.close()

vy = []
mon_fichier_vy = open("tracevy.txt", "r")
for line in mon_fichier_vy.readlines():
    vy.append(float(line)*1000)

mon_fichier_vy.close()

vz = []
mon_fichier_vz = open("tracevz.txt", "r")
for line in mon_fichier_vz.readlines():
    vz.append(float(line)*1000)

mon_fichier_vz.close()

#vitesses simulees
sim_vx = []
mon_fichier_simvx = open("trace_simvx.txt", "r")
for line in mon_fichier_simvx.readlines():
    sim_vx.append(float(line))

mon_fichier_vx.close()

sim_vy = []
mon_fichier_simvy = open("trace_simvy.txt", "r")
for line in mon_fichier_simvy.readlines():
    sim_vy.append(float(line))

mon_fichier_vy.close()

sim_vz = []
mon_fichier_simvz = open("trace_simvz.txt", "r")
for line in mon_fichier_simvz.readlines():
    sim_vz.append(float(line))

mon_fichier_vz.close()


time_v = range(0, len(vx))

plt.plot(time_v, vx, "c", label = "vitesse x demandee")
plt.plot(time_v, sim_vx, "b", label = "vitesse x sim")
plt.xlabel("temps")
plt.ylabel("vitesse")
plt.legend(loc = 3)
plt.show()

plt.plot(time_v, vy, 'm', label = "vitesse y demandee")
plt.plot(time_v, sim_vy, 'r', label = "vitesse y sim")
plt.xlabel("temps")
plt.ylabel("vitesse")
plt.legend(loc = 3)
plt.show()

plt.plot(time_v, vz, 'y', label = "vitesse z demandee")
plt.plot(time_v, sim_vz, 'g', label = "vitesse z sim")
plt.xlabel("temps")
plt.ylabel("vitesse")
plt.legend(loc = 3)
plt.show()
