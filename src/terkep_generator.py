import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import math as math

"""                                                                           
Muszaj relativ eleresi utvonalat hasznalni, hogy mindenki gepen mukodjon a
program a kod valtoztatasa nelkul. Ehhez ez a pathlib-es megoldas aranylag
egyszeru, ami mukodik windowson es linuxon is. Erre akkor is szukseg van,
ha nem cel hogy linuxon is fusson.

A pathlib.Path beimportalasa utan a `Path(__file__)` kifejezes a futtatott fajl
abszolut utvonalaval ter vissza, ahonnan konnyen el lehet erni a tobbi fajlt
relativ modon. A `<utvonal>.parent` property-vel a szulo utvonalat kapjuk meg,
a 'gyermek' nevu gyermeket pedig a `<utvonal> / 'gyermek'` szintaxissal erjuk el.

Pelda az en fajlrendszeremet hasznalva:

> print(Path(__file__))
/home/doma/repos/ehsv/src/terkep_generator.py
> print(Path(__file__).parent)
/home/doma/repos/ehsv/src/
> print(Path(__file__).parent.parent())
/home/doma/repos/ehsv/
> print(Path(__file__).parent.parent / 'resources')
/home/doma/repos/ehsv/resources/
"""

from pathlib import Path


# a repo gyokerenek az eleresi utvonala:
root = Path(__file__).parent.parent

# a 'resources' mappa eleresi utvonala:
resources = root / 'resources'

terkep = pd.read_excel(resources / "terkep_allas.xlsx", sheet_name="térkép")
szinek = pd.read_excel(resources / "terkep_allas.xlsx", sheet_name="játékos színek")

fig, ax = plt.subplots()
sor = terkep.shape[0]
for i in range(sor):
    X = terkep.loc[i, "X"]
    Y = terkep.loc[i, "Y"]
    koordinata = terkep.loc[i, "Koordináta"]
    felirat = terkep.loc[i, "Kié?"]
    harvester = terkep.loc[i, "Harvester?"]
    szin = szinek.loc[szinek["Játékos"] == felirat, "Szín"]
    if not szin.empty:
        color = szin.values[0] 
    else:
        color = 'gray'
    hexagon = patches.RegularPolygon((1.5*X, math.sqrt(3)*Y), numVertices=6, radius=1, orientation=math.pi/6, edgecolor='black', facecolor=color)
    ax.text(1.5*X, math.sqrt(3)*Y, felirat, ha='center', va='center', fontsize=6, color='black')
    ax.text(1.5*X, math.sqrt(3)*Y+0.5, koordinata, ha='center', va='center', fontsize=6, color='black')
    if harvester == 1:
        ax.text(1.5*X, math.sqrt(3)*Y-0.5, "van", ha='center', va='center', fontsize=6, color='red')
    ax.add_patch(hexagon)

ax.set_xlim(0.5, 26.5)
ax.set_ylim(-22, 8)
ax.set_aspect('equal')
plt.show()
