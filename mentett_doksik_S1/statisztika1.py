import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
meddig = int(input("Hány kör ment le eddig?"))+1 
root = Path(__file__).parent.parent
eles_teszt = root /'mentett_doksik'
jatek_allas_xlsx = root / "resources" / "terkep_allas.xlsx"
jatekos_szinek = pd.read_excel(jatek_allas_xlsx, sheet_name="játékos színek")
jatekos_szinek_dict = {}
for i in range(len(jatekos_szinek)):
    jatekos_szinek_dict[str(jatekos_szinek.loc[i, "Játékos"])] = jatekos_szinek.loc[i, "Szín"]


kör_df = {}
jatekos_eleresi_utak = []
for i in range(0,meddig):
    jatekos_nev = "kezdo_jatekos"+str(i)+".csv"
    eleresi_ut = eles_teszt / jatekos_nev
    df = pd.read_csv(eleresi_ut)
    kör_df[str(i)] = df
#nyersanyag értékek játékosokra
nyersanyag_dict = {}
kulcsok = ["viz","spice","lasgun","pisztoly","crysknife","legio","telepitesek"]
for nyersanyag in kulcsok:
    nyersanyag_df = pd.DataFrame({"nev":[1,2,3,4,5,6,7,8,9,10,11,12]})
    for i in range(0,meddig):
        nyersanyag_df[str(i)] = kör_df[str(i)][nyersanyag]
    nyersanyag_dict[nyersanyag] = nyersanyag_df
print(nyersanyag_dict)
"""
#nyersanyag statisztikak
for nyersanyag in nyersanyag_dict.keys():
    for korok in range(0,5):
        for jatekos in range(0,12):
            plt.plot(jatekos+1,nyersanyag_dict[nyersanyag].iloc[jatekos, korok+1],color=jatekos_szinek_dict[str(jatekos+1)])
    plt.savefig(str(nyersanyag)+".png")
    plt.show()
    plt.clf()
"""
for nyersanyag in nyersanyag_dict.keys():
    for jatekos in range(1, 13):
        y_values = nyersanyag_dict[nyersanyag].iloc[jatekos - 1, 1:meddig+1].values
        x_values = list(range(1, meddig + 1))

        plt.plot(
            x_values,
            y_values,
            color=jatekos_szinek_dict[str(jatekos)],
            marker='o',
            linestyle='-',
            label=f"Játékos {jatekos}" if nyersanyag == list(nyersanyag_dict.keys())[0] else ""
        )

    plt.xlabel("Körök")
    plt.ylabel(nyersanyag)
    plt.title(f"Nyersanyag Statisztika: {nyersanyag}")
    if nyersanyag == list(nyersanyag_dict.keys())[0]:
        plt.legend()
    mentes_nev = str(nyersanyag) + ".png"
    plt.savefig(eles_teszt / mentes_nev)
    plt.show()
    plt.clf()



