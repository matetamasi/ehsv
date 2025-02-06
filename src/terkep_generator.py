import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import math as math
térkép = pd.read_excel(r"../src/terkep_allas.xlsx", sheet_name="térkép") #r után a térképes excel elérése
színek = pd.read_excel(r"../src/terkep_allas.xlsx", sheet_name="játékos színek") #r után a térképes excel elérése

fig, ax = plt.subplots()
sor = térkép.shape[0]
for i in range(sor):
    X = térkép.loc[i, "X"]
    Y = térkép.loc[i, "Y"]
    koordináta = térkép.loc[i, "Koordináta"]
    felirat = térkép.loc[i, "Kié?"]
    harvester = térkép.loc[i, "Harvester?"]
    szín = színek.loc[színek["Játékos"] == felirat, "Szín"]
    if not szín.empty:
        color = szín.values[0] 
    else:
        color = 'gray'
    hexagon = patches.RegularPolygon((1.5*X, math.sqrt(3)*Y), numVertices=6, radius=1, orientation=math.pi/6, edgecolor='black', facecolor=color)
    ax.text(1.5*X, math.sqrt(3)*Y, felirat, ha='center', va='center', fontsize=6, color='black')
    ax.text(1.5*X, math.sqrt(3)*Y+0.5, koordináta, ha='center', va='center', fontsize=6, color='black')
    if harvester == 1:
        ax.text(1.5*X, math.sqrt(3)*Y-0.5, "van", ha='center', va='center', fontsize=6, color='red')
    ax.add_patch(hexagon)

ax.set_xlim(0.5, 26.5)
ax.set_ylim(-22, 8)
ax.set_aspect('equal')
plt.show()
