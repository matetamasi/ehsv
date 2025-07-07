legio_szorzo = 3
legio_ar = 2
harvester_kezdeti_ar = 5
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# a repo gyokerenek az eleresi utvonala:
root = Path(__file__).parent.parent

#körszám bekérés
kor = int(input("Hányadik kör következik?"))
kezd_terkep = "kezdo_terkep"+str(kor)+".csv"
veg_terkep = "kezdo_terkep"+str(kor+1)+".csv"
kezd_jatekos = "kezdo_jatekos"+str(kor)+".csv"
veg_jatekos = "kezdo_jatekos"+str(kor+1)+".csv"

# a 'resources' mappa eleresi utvonala:
resources = root / 'resources'
terkepadat = resources / "terkep_adatok_2.xlsx"
jatekallas = resources / "terkep_allas.xlsx" #játékállást tartalmazó excel
lepes_fajl = resources / "lepes.xlsx" #kör lépéseinek az excele
kezdo_jatekos_allas = resources / kezd_jatekos #kör kezdőállása
kezdo_terkep_allas = resources / kezd_terkep #kör harvesteri kezdetben
veg_jatekos_allas = resources / veg_jatekos #kör végállása
veg_terkep_allas = resources / veg_terkep #kör harvesterei végben
terkep_allas = pd.read_excel(terkepadat, sheet_name="adatok").fillna(0) #r után a térképes excel elérése
szinek = pd.read_excel(terkepadat, sheet_name="játékos színek") #r után a térképes excel elérése

def szomszedos(A,B):
    #A mező szomszédja-e B-nek
    if A.nev == "Z0" or B.nev == "Z0":
         #print(str(A.nev)+" vagy " + str(B.nev) + " nullmező")
        return True
    if abs(A.X-B.X)<=1 and abs(A.Y-B.Y)<=1:
        if A.X-B.X == -1 and A.Y-B.Y == 1:
            return False
        if A.X-B.X == 1 and A.Y-B.Y == -1:
            return False
        else:
            print(str(A)+" szomszédja"+str(B))
            return True
    else: 
        return False

class Jatekos:
    def __init__(self, nev, kezdomezo):
        self.nev = nev
        self.mezok = [kezdomezo]
        self.spice = 100
        self.viz = 1
        self.lasgun = 0
        self.crysknife = 0
        self.pistol = 0
        self.legio = 0
        self.gyozelmek_szama = 0
        self.veresegek_szama = 0
        self.telepitett_harvesterek = 0
        self.vasarlasok = {}
    
    def mezore_lepes(self, uj_mezok = list):
        for mezo in uj_mezok:
            print(self.nev + " ralep a " + mezo + " mezore")
            self.mezok.append(mezo)
            mezok[mezo].birtokos = self.nev
    
    def mezorol_lelepes(self, elhagyott_mezok):
        for mezo in elhagyott_mezok:
            if mezo in self.mezok:
                self.mezok.remove(mezo)
                mezok[mezo].birtokos = 0

    def elfogy_e_viz(self):
        ossz_fogyasztas = 0
        for mezo in self.mezok:
            ossz_fogyasztas = ossz_fogyasztas - mezok[mezo].viz
        
        if ossz_fogyasztas > self.viz:
            print("Tul sok a viz fogyasztas")
            print(str(self.viz)+"-ből"+str(ossz_fogyasztas)+" fogyott")
            elvesztett_mezok = []
            for mezo in self.mezok:
                if mezok[mezo].viz < 0:
                    elvesztett_mezok.append(mezo)
            self.mezorol_lelepes(elvesztett_mezok)
            return True
        else:
            print("nincs baj a vizzel")
            print(str(self.viz)+"-ből"+str(ossz_fogyasztas)+" fogyott")
            self.viz = self.viz - ossz_fogyasztas 
            return False

    def spice_termeles(self):
        print(self.nev+" termelése")
        for mezo in self.mezok:
            self.spice = self.spice + mezok[mezo].spice
            print("a "+mezo+" mezőn "+str(mezok[mezo].spice)+" darad spiceot termelt")
    
    def fegyver_vesztes(self):
        print("##Fegyverek###")
        print("A játékos"+self.nev)
        print("pistol, lasgun, knife, legio")
        print(self.pistol)
        print(self.lasgun)
        print(self.crysknife)
        print(self.legio)
        szorzo = 1 - (0.1 * self.veresegek_szama + 0.2 * self.gyozelmek_szama)
        if szorzo < 0:
            szorzo = 0
        print("vesztések"+str(self.veresegek_szama))
        print("győzelmek"+str(self.gyozelmek_szama))
        self.pistol = math.ceil(self.pistol * szorzo)
        self.lasgun = math.ceil(self.lasgun * szorzo)
        self.crysknife = math.ceil(self.crysknife * szorzo)
        self.legio = math.ceil(self.legio * szorzo)
        print("pistol, lasgun, knife, legio")
        print(self.pistol)
        print(self.lasgun)
        print(self.crysknife)
        print(self.legio)
        



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
            print("### Harc ###"+str(self.nev))
            print("jatekos " + jatekosok[jatekos].nev)
            hadero = self.pistol * jatekosok[jatekos].pistol + self.lasgun * jatekosok[jatekos].lasgun + self.crysknife * jatekosok[jatekos].crysknife
            print("hadero: " + str(hadero))
            if self.nev not in jatekosok[jatekos].mezok:
                hadero = hadero + legio_szorzo*jatekosok[jatekos].legio
            haderok[jatekosok[jatekos].nev] = hadero
        
        max_hadero = max(haderok.values())
        max_jatekosok = [key for key, value in haderok.items() if  value == max_hadero]
        gyoztes = 0
        if len(max_jatekosok) == 1:
            gyoztes = max_jatekosok[0]
        for jatekos in self.ralepne:
            if jatekos == gyoztes:
                if self.nev not in jatekosok[jatekos].mezok:
                    print(jatekosok[jatekos].nev+"új győzelmet kapott a "+self.nev+" mezőn")
                    jatekosok[jatekos].gyozelmek_szama = jatekosok[jatekos].gyozelmek_szama + 1
                jatekosok[jatekos].mezore_lepes([self.nev])
            else:
                if self.nev not in jatekosok[jatekos].mezok:
                    print(jatekosok[jatekos].nev+"új vereséget kapott a "+self.nev+" mezőn")
                    jatekosok[jatekos].veresegek_szama = jatekosok[jatekos].veresegek_szama + 1

térkép = pd.read_excel(terkepadat, sheet_name="adatok").fillna(0)
mezo_nevek=[]

for a in range(len(térkép)):
    mezo_nevek.append(térkép.loc[a, "Koordináta"])
mezok = {}

#térkép adatainak a beolvasása mezo classba
i=0
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

#kezdeti jatékállást beolvas
kezdeti_allas = pd.read_csv(kezdo_jatekos_allas)
for i in range(1,13):
    jatekosok[str(i)].viz = kezdeti_allas.loc[i-1, "viz"]
    jatekosok[str(i)].spice = kezdeti_allas.loc[i-1, "spice"]
    jatekosok[str(i)].lasgun = kezdeti_allas.loc[i-1, "lasgun"]
    jatekosok[str(i)].pistol = kezdeti_allas.loc[i-1, "pisztoly"]
    jatekosok[str(i)].crysknife = kezdeti_allas.loc[i-1, "crysknife"]
    jatekosok[str(i)].legio = kezdeti_allas.loc[i-1, "legio"]
    jatekosok[str(i)].telepitett_harvesterek = kezdeti_allas.loc[i-1, "telepitesek"]
kiindulo_terkep = pd.read_csv(kezdo_terkep_allas)
print(kiindulo_terkep)
for j in range(len(kiindulo_terkep)):
    if kiindulo_terkep.loc[j, "Harvester"] == 1:
        print(kiindulo_terkep.loc[j, "Mezo_nev"]+"-en hozott harvester van")
        mezok[kiindulo_terkep.loc[j, "Mezo_nev"]].harvester_telepites()


for k in range(1,13):
    birtok = []
    for j in range(len(kiindulo_terkep)):
        if kiindulo_terkep.loc[j, "Birtokos"] == k:
            birtok.append(kiindulo_terkep.loc[j, "Mezo_nev"])
            mezok[kiindulo_terkep.loc[j, "Mezo_nev"]].birtokos = str(k) 
    jatekosok[str(k)].mezok = birtok

#játék ciklusa
for jatekos in jatekosok.keys():
    jatekos_lepes = pd.read_excel(lepes_fajl, sheet_name=jatekos).fillna(0)
    lelepesek = jatekos_lepes["lelép"]
    for mezo in mezo_nevek:
        for k in range(len(lelepesek)):
            if mezo == lelepesek[k] and mezo in jatekosok[jatekos].mezok:
                print(jatekosok[jatekos].nev)
                print(mezo+"-ről lelépett")
                jatekosok[jatekos].mezok.remove(mezo)
                mezok[mezo].birtokos = 0
    if jatekosok[jatekos].elfogy_e_viz(): 
        print("Elfogyott a viz, " + str(jatekos) + ". jatekos köre kihagyva")
        jatekosok[jatekos].viz = 0
        #TODO azért kell mert, ha elfogyott a víz akkor nem volt feltöltve a vásárlások dict ami gondot okoz, ezen kell szerintem majd vátoztatni, mert a vásárlás ettől még lefuthatna, de ekkora módosítást nem akarok csinálni playtest közben
        jatekosok[jatekos].vasarlasok["lasgun"] = 0
        jatekosok[jatekos].vasarlasok["pistol"] = 0
        jatekosok[jatekos].vasarlasok["crysknife"] = 0
        jatekosok[jatekos].vasarlasok["legio"]= 0
    else:
        #jatekos_lepes = pd.read_excel(lepes_fajl, sheet_name=jatekos).fillna(0)
        lepesek = jatekos_lepes["rálép"]
        lepesek = lepesek.tolist()
        for i in range(len(lepesek)):
            if lepesek[i] == 0: #hogy lépés ne lehessen üres, mert akkor nem működik kulcsnak
                lepesek[i] = "Z0"
        print(str(jatekos)+". jatekos lepesei")
        print(lepesek)
        ervenytelen_lepesek = []
        for lepes in lepesek: 
            valid_lepes = False
            for mezo in jatekosok[jatekos].mezok:
                if szomszedos(mezok[mezo], mezok[lepes]): 
                    valid_lepes = True
                if mezo == lepes:
                    valid_lepes = False
            if not valid_lepes:
                ervenytelen_lepesek.append(lepes)
                print(jatekos + ". jatekos probalt lepni a " + lepes + " mezore, ami nem szomszedos egyik sajatjaval")
        for lepes in ervenytelen_lepesek:
            lepesek.remove(lepes)
        

        lelepesek = jatekos_lepes["lelép"]
        for mezo in mezo_nevek:
            for k in range(len(lepesek)):
                if mezo == lepesek[k]:
                    mezok[mezo].ralepne.append(jatekos)
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
            if jatekos_lepes["harvester"].iloc[0] != 0:
                harvester_ár = harvester_kezdeti_ar*pow(2, jatekosok[jatekos].telepitett_harvesterek)
                print(jatekosok[jatekos].nev)
                print("telepítene"+str(harvester_ár)+"-ért harvestert")
        ár = legio*legio_ar+crysknife+pistol+lasgun+harvester_ár
        
        if ár > jatekosok[jatekos].spice:
            print(jatekos+"elbaszta a költségvetést")
            print(ár)
            print(jatekosok[jatekos].spice)
            jatekosok[jatekos].vasarlasok["lasgun"] = 0
            jatekosok[jatekos].vasarlasok["pistol"] = 0
            jatekosok[jatekos].vasarlasok["crysknife"] = 0
            jatekosok[jatekos].vasarlasok["legio"]= 0
            jatekosok[jatekos].spice_termeles() 
        else:
            print(jatekosok[jatekos].nev)
            jatekosok[jatekos].spice = jatekosok[jatekos].spice-ár
            jatekosok[jatekos].vasarlasok["lasgun"] = int(lasgun)
            jatekosok[jatekos].vasarlasok["pistol"] = int(pistol)
            jatekosok[jatekos].vasarlasok["crysknife"] = int(crysknife)
            jatekosok[jatekos].vasarlasok["legio"]=int(legio)
            if (not jatekos_lepes["harvester"].empty) and pd.notna(jatekos_lepes["harvester"][0]) and jatekos_lepes["harvester"][0] != 0:
                if jatekos_lepes["harvester"][0] in jatekosok[jatekos].mezok:
                    print(str(jatekos_lepes["harvester"][0]) + " mezore harvester kerult")
                    mezok[jatekos_lepes["harvester"][0]].harvester_telepites()
                    jatekosok[jatekos].telepitett_harvesterek = int(jatekosok[jatekos].telepitett_harvesterek + 1)
                else:
                    print(str(jatekos)+" rossz helyre raknak harvestert")
            jatekosok[jatekos].spice_termeles() 

for mezonev in mezok.keys():
    mezok[mezonev].lepesek_szetvalasztas()

    mezok[mezonev].ralepne = []

for jatekos in jatekosok.keys():
    jatekosok[jatekos].fegyver_vesztes()
    jatekosok[jatekos].gyozelmek_szama = 0
    jatekosok[jatekos].veresegek_szama = 0
    print("##Vasarlasok##")
    print(jatekosok[jatekos].vasarlasok)
    jatekosok[jatekos].lasgun = jatekosok[jatekos].lasgun + jatekosok[jatekos].vasarlasok["lasgun"]
    jatekosok[jatekos].crysknife = jatekosok[jatekos].crysknife + jatekosok[jatekos].vasarlasok["crysknife"]
    jatekosok[jatekos].pistol = jatekosok[jatekos].pistol + jatekosok[jatekos].vasarlasok["pistol"]
    jatekosok[jatekos].legio = jatekosok[jatekos].legio + jatekosok[jatekos].vasarlasok["legio"] 
"""
###Térkép

fig, ax = plt.subplots()
sor = terkep_allas.shape[0]
#print(terkep_allas)
for i in range(sor):
    X = terkep_allas.loc[i, "Xkoord"]
    Y = terkep_allas.loc[i, "Ykoord"]
    koordináta = terkep_allas.loc[i, "Koordináta"]
    felirat = mezok[str(koordináta)].birtokos
    harvester = mezok[str(koordináta)].harvester
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
for i in range(1,13): #játékos nyersanyagok kiírása, később véletlen megcsináltam mégegyszer
    jatekos_nyersanyagok.append(jatekosok[str(i)].nev)
    jatekos_nyersanyagok.append(jatekosok[str(i)].spice)
    jatekos_nyersanyagok.append(jatekosok[str(i)].viz)
    jatekos_nyersanyagok.append(jatekosok[str(i)].lasgun)
    jatekos_nyersanyagok.append(jatekosok[str(i)].crysknife)
    jatekos_nyersanyagok.append(jatekosok[str(i)].pistol)
    jatekos_nyersanyagok.append(jatekosok[str(i)].legio)
    printout.loc[len(printout)] = jatekos_nyersanyagok
    jatekos_nyersanyagok = []
print("A nyersanyagok")
print(printout)
ax.set_xlim(-2, 26)
ax.set_ylim(-1, 29)
ax.set_aspect('equal')
plt.show()
"""
#játékállás printoutot csinál egy dataframebe majd csv-be
fejlec = ["jatekos", "viz", "spice", "lasgun", "pisztoly", "crysknife", "legio", "telepitesek"]
jatekosallas_mentes = pd.DataFrame(columns=fejlec)
for i in range(1,13):
    uj_sor = []
    uj_sor.append(str(i))
    uj_sor.append(jatekosok[str(i)].viz)
    uj_sor.append(jatekosok[str(i)].spice)
    uj_sor.append(jatekosok[str(i)].lasgun)
    uj_sor.append(jatekosok[str(i)].pistol)
    uj_sor.append(jatekosok[str(i)].crysknife)
    uj_sor.append(jatekosok[str(i)].legio)
    uj_sor.append(jatekosok[str(i)].telepitett_harvesterek)
    jatekosallas_mentes.loc[len(jatekosallas_mentes)] = uj_sor

terkep_mentes = pd.DataFrame(columns=["Mezo_nev","Birtokos","Harvester"])
for mezo in mezo_nevek:
    uj_sor = []
    uj_sor.append(mezo)
    uj_sor.append(mezok[mezo].birtokos)
    if mezok[mezo].harvester == 1:
        uj_sor.append(1)
    else: 
        uj_sor.append(0)
    terkep_mentes.loc[len(terkep_mentes)] = uj_sor

jatekosallas_mentes.to_csv(veg_jatekos_allas, index=False)
terkep_mentes.to_csv(veg_terkep_allas, index=False)
