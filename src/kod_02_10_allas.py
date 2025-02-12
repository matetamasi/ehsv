legio_szorzo = 3
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# a repo gyokerenek az eleresi utvonala:
root = Path(__file__).parent.parent
# a 'resources' mappa eleresi utvonala:
resources = root / 'resources'
terkepadat = resources / "terkep_adatok.xlsx"
jatekallas = resources / "terkep_allas.xlsx" #játékállást tartalmazó excel
lepes = resources / "lepes.xlsx" #kör lépéseinek az excele

terkep_allas = pd.read_excel(jatekallas, sheet_name="térkép").fillna(0) #r után a térképes excel elérése
szinek = pd.read_excel(jatekallas, sheet_name="játékos színek") #r után a térképes excel elérése


def szomszedos(A,B):
    #A mező szomszédja-e B-nek
    if abs(A.X-B.X)<=1 and abs(A.Y-B.Y)<=1:
        if A.X-B.X == -1 and A.Y-B.Y == 1:
            return False
        if A.X-B.X == 1 and A.Y-B.Y == -1:
            return False
        else:
            #print(str(A)+" szomszédja"+str(B))
            return True
    #if A == "Z0" or B == "Z0":
    #    print(str(A)+" vagy" + str(B) + " nullmező")
    #    return True
    else: 
        return False

class Jatekos:
    def __init__(self, nev, kezdomezo):
        self.nev = nev
        self.mezok = [kezdomezo]
        self.spice = 100
        self.viz = 100
        self.lasgun = 0
        self.crysknife = 0
        self.pistol = 0
        self.legio = 0
        self.gyozelmek_szama = 0
        self.veresegek_szama = 0
        self.telepitett_harvesterek = 0
    
    def mezore_lepes(self, uj_mezok = list):
        for mezo in uj_mezok:
            print(self.nev + " ralep a " + mezo + " mezore")
            self.mezok.append(mezo)
            mezok[mezo].birtokos = self.nev
    
    def mezorol_lelepes(self, mezok):
        for mezo in mezok:
            self.mezok.remove(mezo)
            mezok[mezo].birtokos = None

    def elfogy_e_viz(self):
        ossz_fogyasztas = 0
        for mezo in self.mezok:
            ossz_fogyasztas = ossz_fogyasztas - mezok[mezo].viz
        
        if ossz_fogyasztas > self.viz:
            print("Tul sok a viz fogyasztas")
            elvesztett_mezok = []
            for mezo in self.mezok:
                if mezok[mezo].viz < 0:
                    elvesztett_mezok.append(mezo)
            self.mezorol_lelepes(elvesztett_mezok)
        else:
            print("nincs baj a vizzel")

    def spice_termeles(self):
        for mezo in self.mezok:
            self.spice = self.spice + mezok[mezo].spice
    
    def fegyver_vesztes(self):
        szorzo = 1 - (0.1 * self.veresegek_szama + 0.2 * self.gyozelmek_szama)
        if szorzo < 0:
            szorzo = 0
        self.pistol = math.ceil(self.pistol * szorzo)
        self.lasgun = math.ceil(self.lasgun * szorzo)
        self.crysknife = math.ceil(self.crysknife * szorzo)
        self.legio = math.ceil(self.legio * szorzo)
        



class Mezo:
    def __init__(self, nev, X, Y, viz, spice, pistol, lasgun, crysknife):
        self.nev = nev
        self.X = X
        self.Y = Y
        self.viz = viz
        self.spice = spice
        self.pistol = pistol
        self.lasgun = lasgun
        self.crysknife = crysknife
        self.harvester = 0
        self.birtokos = 0
        self.ralepne = []
        
    def harvester_telepites(self):
        self.harvester = 1
        self.spice = self.spice * 2

    def lepesek_szetvalasztas(self):
        if len(self.ralepne) == 1 and not self.birtokos:
            jatekosok[self.ralepne[0]].mezore_lepes([self.nev])
        elif (len(self.ralepne) == 1 and self.birtokos) or len(self.ralepne) > 1:
            if self.birtokos:
                self.ralepne.append(self.birtokos)
            self.harc()
        
    
    def harc(self):
        haderok = {}
        for jatekos in self.ralepne:
            print("### Harc ###")
            print("jatekos " + jatekosok[jatekos].nev)
            hadero = self.pistol * jatekosok[jatekos].pistol + self.lasgun * jatekosok[jatekos].lasgun + self.crysknife * jatekosok[jatekos].crysknife
            print("hadero: " + str(hadero))
            if self.nev not in jatekosok[jatekos].mezok:
                hadero = hadero + legio_szorzo*jatekosok[jatekos].legio
            haderok[jatekosok[jatekos].nev] = hadero
        
        #Dontetlent lekezelni!!!
        gyoztes = max(haderok, key=haderok.get)
        for jatekos in self.ralepne:
            if jatekos == gyoztes:
                jatekosok[jatekos].mezore_lepes([self.nev])
                if self.nev not in jatekosok[jatekos].mezok:
                    jatekosok[jatekos].gyozelmek_szama = jatekosok[jatekos].gyozelmek_szama + 1
            else:
                if self.nev not in jatekosok[jatekos].mezok:
                    jatekosok[jatekos].veresegek_szama = jatekosok[jatekos].veresegek_szama + 1
        
"""
jatekos1 = Jatekos("1", "A1")
jatekos1.spice = jatekos1.spice + 2
jatekos2 = Jatekos("2", "B2")

mezok = {}
nevek = ["A1", "B2", "D4"]
mezok[nevek[0]] = Mezo("A1", 1, 0, 7, 1, pistol=1, lasgun=3, crysknife=1)
mezok[nevek[1]] = Mezo("B2", 2,3, -4, 1, pistol=1, lasgun=3, crysknife=1)
jatekos1.mezore_lepes(["B2"])

jatekos1.pistol = 1
jatekos1.crysknife = 1
jatekos1.lasgun = 1
jatekos1.legio = 1

jatekos2.pistol = 2
jatekos2.crysknife = 1
jatekos2.lasgun = 1


mezok[nevek[2]] = Mezo(nevek[2], 2,3, -4, 1, pistol=1, lasgun=3, crysknife=1)
mezok[nevek[2]].ralepne = [jatekos1, jatekos2]
mezok[nevek[2]].lepesek_szetvalasztas()
"""



### Szabi kódja ###

#Init

térkép = pd.read_excel(terkepadat, sheet_name="adatok").fillna(0)
mezo_nevek=[]

for a in range(len(térkép)):
    mezo_nevek.append(térkép.loc[a, "Koordináta"])
mezok = {}
i=0
#térkép adatainak a beolvasása mezo classba
for mezo_nev in mezo_nevek:
    mezok[mezo_nev]=Mezo(str(mezo_nev), int(térkép.loc[i, "X"]), int(térkép.loc[i, "Y"]), int(térkép.loc[i, "víz szorzó"]), int(térkép.loc[i, "spice szorzó"]), int(térkép.loc[i, "pisztoly"]), int(térkép.loc[i, "lasgun"]), int(térkép.loc[i, "crysknife"]))
    i = i+1
#nullelem a mezők között
mezok["Z0"] = Mezo("Z0", 100, 100, 0, 0, 0, 0, 0)
#jatékosokat csinál
jatekosok = {}
kezdőmezők = ["C1","G1","K1","O1","Q3","Q7","O11","K15","G15","C11","A7","A3"]
for l in range(1,13):
    jatekosok[str(l)]=Jatekos(str(l), str(kezdőmezők[l-1]))
    mezok[kezdőmezők[l-1]].birtokos = str(l)
print(szomszedos(mezok["C1"],mezok["D3"]))
#Jatek menet
for turn in range(1,11):
    print(str(turn) + ". Kör")

    #mezo.ralepne dolgot tölti fel
    j = 1
    while j < 13:
        jatekos_lepes = pd.read_excel(lepes, sheet_name=str(j)).fillna(0)
        lepesek = jatekos_lepes["rálép"]
        lepesek = lepesek.tolist()
        if lepesek == [0]: #hogy lépés ne lehessen üres, mert akkor nem működik kulcsnak
            lepesek = ["Z0"]
        for lepes in lepesek: #ha van egy rossz lépés utána enged rossz lépést csinálni TODO
            print(lepes)
            valid_lepes = False
            for mezo in jatekosok[str(j)].mezok:
                if szomszedos(mezok[mezo], mezok[lepes]): 
                    valid_lepes = True
            if not valid_lepes:
                lepesek.remove(lepes)
                print(str(j) + ". jatekos probalt lepni a " + lepes + " mezore, ami nem szomszedos egyik sajatjaval")
        lelepesek = jatekos_lepes["lelép"]
        for mezo in mezo_nevek:
            for k in range(len(lepesek)):
                if mezo == lepesek[k]:
                    mezok[mezo].ralepne.append(str(j))
            for k in range(len(lelepesek)):
                if mezo == lelepesek[k]:
                    jatekosok[str(j)].mezok.remove(mezo)
                    mezok[mezo].birtokos = 0 
        lasgun = 0
        if not jatekos_lepes["lasgun"].empty:
            lasgun = jatekos_lepes["lasgun"][0]

        crysknife = 0
        if not jatekos_lepes["crysknife"].empty:
            crysknife = jatekos_lepes["crysknife"][0]
            
        pistol = 0
        if not jatekos_lepes["pisztoly"].empty:
            pistol = jatekos_lepes["pisztoly"][0]

        legio = 0
        if not jatekos_lepes["légiók"].empty:
            legio = jatekos_lepes["légiók"][0]
        harvester_ár = 0
        if not jatekos_lepes["harvester"].empty:
            harvester_ár = 5*pow(2, jatekosok[str(j)].telepitett_harvesterek + 1)
        ár = legio*3+crysknife+pistol+lasgun+harvester_ár
        
        #FEGYVEREK CSAK KOVETKEZO KORBEN! TODO
        if ár > jatekosok[str(j)].spice:
            print(str(j)+"elbaszta a költségvetést")
        else:
            jatekosok[str(j)].spice = jatekosok[str(j)].spice-ár
            jatekosok[str(j)].lasgun = int(jatekosok[str(j)].lasgun+lasgun)
            jatekosok[str(j)].pistol = int(jatekosok[str(j)].pistol+pistol)
            jatekosok[str(j)].crysknife = int(jatekosok[str(j)].crysknife+crysknife)
            jatekosok[str(j)].legio=int(jatekosok[str(j)].legio+legio)
            jatekosok[str(j)].telepitett_harvesterek = int(jatekosok[str(j)].telepitett_harvesterek + 1)
            if (not jatekos_lepes["harvester"].empty) and pd.notna(jatekos_lepes["harvester"][0]) and jatekos_lepes["harvester"][0] != 0:
                print(str(jatekos_lepes["harvester"][0]) + " mezore harvester kerult")
                mezok[jatekos_lepes["harvester"][0]].harvester_telepites()
        
        j = j+1
    
    for mezonev in mezok.keys():
        mezok[mezonev].lepesek_szetvalasztas()

        mezok[mezonev].ralepne = []
    
    for jatekos in jatekosok.keys():
        jatekosok[jatekos].gyozelmek_szama = 0
        jatekosok[jatekos].veresegek_szama = 0
    
    print("Jatekos allas")
    print(mezok["A1"].ralepne)
    print(jatekosok["1"].mezok)
    print(jatekosok["1"].spice)
    print(mezok["C2"].harvester)

    ###Térkép

    fig, ax = plt.subplots()
    sor = terkep_allas.shape[0]
    #print(terkep_allas)
    for i in range(sor):
        X = terkep_allas.loc[i, "X"]
        Y = terkep_allas.loc[i, "Y"]
        #print(X)
        #print(Y)
        koordináta = terkep_allas.loc[i, "Koordináta"]
        felirat = mezok[str(koordináta)].birtokos
        harvester = mezok[str(koordináta)].harvester
        #print("###")
        #print(harvester)
        #print(type(harvester))
        szín = szinek.loc[szinek["Játékos"] == int(felirat), "Szín"]
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
    jatekos_nyersanyagok = []
    printout = pd.DataFrame(columns=["név","spice","viz", "lasgun", "crysknife", "pistol", "legio"])
    for i in range(1,13): #játékos nyersanyagok kiírása
        jatekos_nyersanyagok.append(jatekosok[str(i)].nev)
        jatekos_nyersanyagok.append(jatekosok[str(i)].spice)
        jatekos_nyersanyagok.append(jatekosok[str(i)].viz)
        jatekos_nyersanyagok.append(jatekosok[str(i)].lasgun)
        jatekos_nyersanyagok.append(jatekosok[str(i)].crysknife)
        jatekos_nyersanyagok.append(jatekosok[str(i)].pistol)
        jatekos_nyersanyagok.append(jatekosok[str(i)].legio)
        printout.loc[len(printout)] = jatekos_nyersanyagok
        print(jatekos_nyersanyagok)
        jatekos_nyersanyagok = []
    print("A nyersanyagok")
    print(printout)
    ax.set_xlim(0.5, 26.5)
    ax.set_ylim(-22, 8)
    ax.set_aspect('equal')
    plt.show()
    input("Nyomj Entert, hogy a következő körbe lépj")









    
    
 