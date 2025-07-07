legio_szorzo = 3
legio_ar = 2
harvester_kezdeti_ar = 5
legio_ar = 2
harvester_kezdeti_ar = 5
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import matplotlib.colors as mcolors
from PIL import Image, ImageDraw, ImageFont
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
terkepadat = resources / "terkep_adatok.xlsx"
jatekallas = resources / "terkep_allas.xlsx" #játékállást tartalmazó excel
lepes_fajl = resources / "lepes.xlsx" #kör lépéseinek az excele
kezdo_jatekos_allas = resources / kezd_jatekos #kör kezdőállása
kezdo_terkep_allas = resources / kezd_terkep #kör harvesteri kezdetben
veg_jatekos_allas = resources / veg_jatekos #kör végállása
veg_terkep_allas = resources / veg_terkep #kör harvesterei végben
terkep_allas = pd.read_excel(jatekallas, sheet_name="térkép").fillna(0) #r után a térképes excel elérése
szinek = pd.read_excel(jatekallas, sheet_name="játékos színek") #r után a térképes excel elérése

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
            print("nincs baj a vizzel")
            print(str(self.viz)+"-ből"+str(ossz_fogyasztas)+" fogyott")
            self.viz = self.viz - ossz_fogyasztas 
            return False

    def spice_termeles(self):
        print(self.nev+" termelése")
        print(self.nev+" termelése")
        for mezo in self.mezok:
            self.spice = self.spice + mezok[mezo].spice
            print("a "+mezo+" mezőn "+str(mezok[mezo].spice)+" darad spiceot termelt")
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
                    print(jatekosok[jatekos].nev+"új győzelmet kapott a "+self.nev+" mezőn")
                    jatekosok[jatekos].gyozelmek_szama = jatekosok[jatekos].gyozelmek_szama + 1
                jatekosok[jatekos].mezore_lepes([self.nev])
            else:
                if self.nev not in jatekosok[jatekos].mezok:
                    print(jatekosok[jatekos].nev+"új vereséget kapott a "+self.nev+" mezőn")
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
print(kiindulo_terkep)
for j in range(len(kiindulo_terkep)):
    if kiindulo_terkep.loc[j, "Harvester"] == 1:
        print(kiindulo_terkep.loc[j, "Mezo_nev"]+"-en hozott harvester van")
        mezok[kiindulo_terkep.loc[j, "Mezo_nev"]].harvester_telepites()
        print(kiindulo_terkep.loc[j, "Mezo_nev"]+"-en hozott harvester van")
        mezok[kiindulo_terkep.loc[j, "Mezo_nev"]].harvester_telepites()


for k in range(1,13):
    birtok = []
    for j in range(len(kiindulo_terkep)):
        if kiindulo_terkep.loc[j, "Birtokos"] == k:
            birtok.append(kiindulo_terkep.loc[j, "Mezo_nev"])
            mezok[kiindulo_terkep.loc[j, "Mezo_nev"]].birtokos = str(k) 
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
        #TODO azért kell mert, ha elfogyott a víz akkor nem volt feltöltve a vásárlások dict ami gondot okoz, ezen kell szerintem majd vátoztatni, mert a vásárlás ettől még lefuthatna, de ekkora módosítást nem akarok csinálni playtest közben
        jatekosok[jatekos].vasarlasok["lasgun"] = 0
        jatekosok[jatekos].vasarlasok["pistol"] = 0
        jatekosok[jatekos].vasarlasok["crysknife"] = 0
        jatekosok[jatekos].vasarlasok["legio"]= 0
    else:
        #jatekos_lepes = pd.read_excel(lepes_fajl, sheet_name=jatekos).fillna(0)
        #jatekos_lepes = pd.read_excel(lepes_fajl, sheet_name=jatekos).fillna(0)
        lepesek = jatekos_lepes["rálép"]
        lepesek = lepesek.tolist()
        for i in range(len(lepesek)):
            if lepesek[i] == 0: #hogy lépés ne lehessen üres, mert akkor nem működik kulcsnak
                lepesek[i] = "Z0"
        for i in range(len(lepesek)):
            if lepesek[i] == 0: #hogy lépés ne lehessen üres, mert akkor nem működik kulcsnak
                lepesek[i] = "Z0"
        print(str(jatekos)+". jatekos lepesei")
        print(lepesek)
        ervenytelen_lepesek = []
        for lepes in lepesek: 
        for lepes in lepesek: 
            valid_lepes = False
            for mezo in jatekosok[jatekos].mezok:
                if szomszedos(mezok[mezo], mezok[lepes]): 
                    valid_lepes = True
                if mezo == lepes:
                    valid_lepes = False
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
            print(ár)
            print(jatekosok[jatekos].spice)
            jatekosok[jatekos].vasarlasok["lasgun"] = 0
            jatekosok[jatekos].vasarlasok["pistol"] = 0
            jatekosok[jatekos].vasarlasok["crysknife"] = 0
            jatekosok[jatekos].vasarlasok["legio"]= 0
            jatekosok[jatekos].spice_termeles() 
        else:
            print(jatekosok[jatekos].nev)
            print(jatekosok[jatekos].nev)
            jatekosok[jatekos].spice = jatekosok[jatekos].spice-ár
            jatekosok[jatekos].vasarlasok["lasgun"] = int(lasgun)
            jatekosok[jatekos].vasarlasok["pistol"] = int(pistol)
            jatekosok[jatekos].vasarlasok["crysknife"] = int(crysknife)
            jatekosok[jatekos].vasarlasok["legio"]=int(legio)
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
    print("##Vasarlasok##")
    print(jatekosok[jatekos].vasarlasok)
    jatekosok[jatekos].lasgun = jatekosok[jatekos].lasgun + jatekosok[jatekos].vasarlasok["lasgun"]
    jatekosok[jatekos].crysknife = jatekosok[jatekos].crysknife + jatekosok[jatekos].vasarlasok["crysknife"]
    jatekosok[jatekos].pistol = jatekosok[jatekos].pistol + jatekosok[jatekos].vasarlasok["pistol"]
    jatekosok[jatekos].legio = jatekosok[jatekos].legio + jatekosok[jatekos].vasarlasok["legio"] 

###Térkép
"""
fig, ax = plt.subplots()
sor = terkep_allas.shape[0]
#print(terkep_allas)
for i in range(sor):
    X = terkep_allas.loc[i, "X"]
    Y = terkep_allas.loc[i, "Y"]
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
ax.set_xlim(0.5, 26.5)
ax.set_ylim(-22, 8)
ax.set_aspect('equal')
plt.show()
"""
#input("Nyomj Entert, hogy a következő körbe lépj")

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

#körszám bekérés
kor = input("Hányadik kör következik?")
allas = "kezdo_terkep"+str(kor)+".csv"

#mezők paramétereinek a változói
mezo_tipus = 1 #1:sivatag 0: hegy, 2: ures
fegyver_tipus = 2 #0: pistol, 1:lasgun, 2:knife, 3: külső
viz_szorzo = 10 #int
spice_szorzo = 15 #int
koordinata = "A69" #string

root = Path(__file__).parent.parent

#adatfájlok, képelemek elérési útjainak a beolvasása

resources = root / 'resources'
crysknife_png = resources / "crysknife.png"
lasgun_png = resources / "lasgun.png"
pistol_png = resources / "pistol.png"
hegy_png = resources / "hegy.png"
sivatag_png = resources / "sivatag.png"
ures_png = resources / "ures.png"
grid_png = resources / "grid.png"
font_path = resources / "Times-New-Roman.otf" #rossz font, mert a jó szar
jatekos_szimbolum = resources / "fremen_ikon.png"
terkep_fajl = resources / "terkep_adatok_2.xlsx" #teszt
jatek_allas = resources / allas #itt szerk
jatek_allas_xlsx =  resources / "terkep_allas.xlsx"

#pandas DF-ek, ezekben van az aktuális állás, illtve a térképen a jelölők
jatekos_szinek = pd.read_excel(jatek_allas_xlsx, sheet_name="játékos színek")
mezo_birtokos_DF = pd.read_csv(jatek_allas)
terkep_DF = pd.read_excel(terkep_fajl, sheet_name="adatok").fillna(0)

#üres háttér
hex_map = Image.new("RGBA", (8944, 10098), (255, 255, 255, 0))
#dune font
dune_font = ImageFont.truetype(font_path, 80)

#mezők generálása és térképre helyezése
for i in range(len(terkep_DF)):
    #adatfájlokból a mező paramétereinek a kiolvasása
    mezo_nev = terkep_DF.loc[i, "mező"]
    harvester = mezo_birtokos_DF.loc[i, "Harvester"]
    fegyver_nev = terkep_DF.loc[i, "fegyver típus"]
    viz_szorzo = int(terkep_DF.loc[i, "víz szorzó"])
    spice_szorzo = int(terkep_DF.loc[i, "spice szorzó"])
    koordinata = terkep_DF.loc[i, "Koordináta"]
    X = terkep_DF.loc[i, "Xkoord"]
    Y = terkep_DF.loc[i, "Ykoord"]

    #mezo típus hozzárendelés az excelben levő nevek alapján 
    if mezo_nev == "külső":
        mezo_tipus = 2
    elif (mezo_nev == "bázis") or (mezo_nev == "Hgs"):
        mezo_tipus = 0
    elif (mezo_nev == "Svt"):
        mezo_tipus = 1
    else: 
        mezo_tipus = 2
        print("Hiányzó mező típus: "+str(mezo_nev)+" a "+str(i+2)+". sorban")
    #fegyver típus hozzárendelés az excelben levő nevek alapján
    if fegyver_nev == 0:
        fegyver_tipus = 3
    elif fegyver_nev == "Maula Pistol":
        fegyver_tipus = 0
    elif fegyver_nev == "Crysknife":
        fegyver_tipus = 2
    elif fegyver_nev == "Lasgun":
        fegyver_tipus = 1
    else: 
        fegyver_tipus = 1
        print("Hiányzó fegyver típus: "+str(fegyver_nev)+" a "+str(i+2)+". sorban")
    
    #megfelelő háttér kiválasztása a mező háttere alapján
    if mezo_tipus == 0:
        hex_tile = Image.open(hegy_png).convert("RGBA")
    elif mezo_tipus == 1:
        hex_tile = Image.open(sivatag_png).convert("RGBA")
    else: 
        hex_tile = Image.open(ures_png).convert("RGBA")
    
    #mező háttér alapján méret kiszedése
    hex_w, hex_h = hex_tile.size

    #koordinata felirat ráhelyezése a mezőre
    koord_img = Image.new("RGBA", (hex_w, hex_h), (255, 255, 255, 0)) 
    draw = ImageDraw.Draw(koord_img)
    number_text = koordinata
    koord_x, koord_y = hex_w // 2 , hex_h // 2 -250 #itt játszani kell a hellyel, hogy hova kerüljön
    draw.text((koord_x, koord_y), number_text, fill="black", font=dune_font, anchor="mm")
    hex_tile = Image.alpha_composite(hex_tile, koord_img)

    #víz szorzó felirat ráhelyezése a mezőre
    viz_szorzo_img = Image.new("RGBA", (hex_w, hex_h), (255, 255, 255, 0))  
    draw = ImageDraw.Draw(viz_szorzo_img)
    number_text = str(viz_szorzo)
    viz_x, viz_y = hex_w // 2 -230, hex_h // 2 +100 #itt játszani kell a hellyel, hogy hova kerüljön
    draw.text((viz_x, viz_y), number_text, fill="black", font=dune_font, anchor="mm")
    rot_viz_szorzo = viz_szorzo_img.rotate(300, resample=Image.BICUBIC, center=(viz_x, viz_y)) 
    hex_tile = Image.alpha_composite(hex_tile, rot_viz_szorzo)

    #spice szorzó
    spice_img = Image.new("RGBA", (hex_w, hex_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(spice_img)
    if harvester == 1: #van-e harvester a mezőn
        number_text = str(spice_szorzo*2)
        spice_szorzo_szin = "red"
    else:
        number_text = str(spice_szorzo)
        spice_szorzo_szin = "black"
    spice_x, spice_y = hex_w // 2 +240, hex_h // 2 +60 #itt játszani kell a hellyel, hogy hova kerüljön
    draw.text((spice_x, spice_y), number_text, fill=spice_szorzo_szin, font=dune_font, anchor="mm")
    rot_spice_img = spice_img.rotate(60, resample=Image.BICUBIC, center=(spice_x, spice_y))
    hex_tile = Image.alpha_composite(hex_tile, rot_spice_img)
    
    #birtokos jelző rárakás
    birtokos = mezo_birtokos_DF.loc[i, "Birtokos"]
    colors = mcolors.CSS4_COLORS  # Dictionary of color names
    #print(colors.keys())  # Lists available colors
    #birtokos jelző fekete pixeleineka az átszínezése a szükséges színre
    if birtokos != 0:
        for i in range(len(jatekos_szinek)):
            if jatekos_szinek.loc[i, "Játékos"] == birtokos:
                szin = jatekos_szinek.loc[i, "Szín"]
        colors = mcolors.CSS4_COLORS
        colour_hex = mcolors.to_rgba(szin, alpha=1)
        colour_rgb = tuple(int(c * 255) for c in colour_hex)
        ikon = Image.open(jatekos_szimbolum).convert("RGBA")
        #chatgpt hagyatéka
        # Get pixel data
        data = ikon.getdata()
        # Create a new image with recolored pixels
        new_data = []
        for r, g, b, a in data:
            if a > 0 and r < 50 and g < 50 and b < 50:  # Keep transparency, recolor only dark pixels
                new_data.append(colour_rgb)  
            else:
                new_data.append((r, g, b, a))  # Keep other pixels unchanged
        ikon.putdata(new_data)
        max_size = (200, 200)
        ikon.thumbnail(max_size)
        ikon_x = (hex_w - ikon.width) // 2
        ikon_y = (hex_h - ikon.height) // 2
        hex_tile.paste(ikon, (ikon_x, ikon_y), ikon)


    #fegyver típus választása, itt minden fegyver képe más, ezért változnak a koordináták
    if fegyver_tipus == 0:
        symbol = Image.open(pistol_png).convert("RGBA")
        max_size = (167, 85) 
        symbol.thumbnail(max_size)
        symbol_x = (hex_w - symbol.width) // 2
        symbol_y = (hex_h - symbol.height) // 2 + 230
        hex_tile.paste(symbol, (symbol_x, symbol_y), symbol)
    if fegyver_tipus == 1:
        symbol = Image.open(lasgun_png).convert("RGBA")
        max_size = (195, 87) 
        symbol.thumbnail(max_size)
        symbol_x = (hex_w - symbol.width) // 2
        symbol_y = (hex_h - symbol.height) // 2 + 230
        hex_tile.paste(symbol, (symbol_x, symbol_y), symbol)
    if fegyver_tipus == 2:
        symbol = Image.open(crysknife_png).convert("RGBA")
        max_size = (200, 69) 
        symbol.thumbnail(max_size)
        symbol_x = (hex_w - symbol.width) // 2
        symbol_y = (hex_h - symbol.height) // 2 + 230
        hex_tile.paste(symbol, (symbol_x, symbol_y), symbol)
    mezo = ImageDraw.Draw(hex_tile)
    tile_height = 594
    tile_width = 688
    korrekcios_faktor = 0.855 #ahhoz kell, hogy ne legyenek rések a mezők között, ha csökken a szám közelebb kerülnek, ha nő akkor nő, felező módszerrel szépen meg lehet találni az ideális értéket
    tile_size = (int(tile_width), int(tile_height))
    tile_x = X*tile_height*korrekcios_faktor
    tile_y = Y*tile_width*korrekcios_faktor
    hex_map.paste(hex_tile, (int(tile_x), int(tile_y)), hex_tile)
print("Türelem térképet terem!")
hex_map.show() 
hex_map.save(root / "output_map.png", format="PNG")
