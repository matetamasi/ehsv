legio_szorzo = 3
import pandas as pd
import math
térképadat = r"../resources/terkep_adatok.xlsx"
játékállás = r"../resources/terkep allas.xlsx" #játékállást tartalmazó excel
lépés = r"../resources/lepes.xlsx" #kör lépéseinek az excele

def szomszedos(A,B):
    #A mező szomszédja-e B-nek
    if abs(A.X-B.X)<=1 and abs(A.Y-B.Y)<=1:
        if A.X-B.X == -1 and A.Y-B.Y == 1:
            return False
        if A.X-B.X == 1 and A.Y-B.Y == -1:
            return False
        else:
            return True
    else: 
        return False

class Jatekos:
    def __init__(self, nev, kezdomezo):
        self.nev = nev
        self.mezok = [kezdomezo]
        self.spice = 10
        self.viz = 10
        self.lasgun = 0
        self.crysknife = 0
        self.pistol = 0
        self.legio = 0
        self.gyozelmek_szama = 0
        self.veresegek_szama = 0
        self.telepitett_harvesterek = 0
    
    def mezore_lepes(self, uj_mezok = list):
        for mezo in uj_mezok:
            self.mezok.append(mezo)
            mezok[mezo].birtok = self.nev
    
    def mezorol_lelepes(self, mezok):
        for mezo in mezok:
            self.mezok.remove(mezo)
            mezok[mezo].birtok = None

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
        szorzo = 0.1 * self.veresegek_szama + 0.2 * self.gyozelmek_szama
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
        self.birtokos = None
        self.ralepne = []
        
    def havester_telepites(self):
        self.harvester = 1
        self.spice = self.spice * 2

    def lepesek_szetvalasztas(self):
        if len(self.ralepne) == 1 and not self.birtokos:
            self.ralepne[0].mezore_lepes([self.nev])
        elif len(self.ralepne) == 0 and self.birtokos or len(self.ralepne) > 1:
            if self.birtokos:
                self.ralepne.append(self.birtokos)
            self.harc()
        
    
    def harc(self):
        haderok = {}
        for jatekos in self.ralepne:
            print(jatekos.nev)
            hadero = self.pistol * jatekos.pistol + self.lasgun * jatekos.lasgun + self.crysknife * jatekos.crysknife
            if self.nev not in jatekos.mezok:
                hadero = hadero + legio_szorzo*jatekos.legio
            haderok[jatekos.nev] = hadero
        
        gyoztes = max(haderok, key=haderok.get)
        for jatekos in self.ralepne:
            if jatekos.nev == gyoztes:
                jatekos.mezore_lepes([self.nev])
                if self.nev not in jatekos.mezok:
                    jatekos.gyozelmek_szama = jatekos.gyozelmek_szama + 1
            else:
                if self.nev not in jatekos.mezok:
                    jatekos.veresegek_szama = jatekos.veresegek_szama + 1
        
""""""
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

"""
mezok[nevek[2]] = Mezo(nevek[2], 2,3, -4, 1, pistol=1, lasgun=3, crysknife=1)
mezok[nevek[2]].ralepne = [jatekos1, jatekos2]
mezok[nevek[2]].lepesek_szetvalasztas()
"""



### Szabi kódja ###

térkép = pd.read_excel(térképadat, sheet_name="adatok").fillna(0)
mezo_nevek=[]
for a in range(len(térkép)):
    mezo_nevek.append(térkép.loc[a, "Koordináta"])
mezok = {}
i=0
#térkép adatainak a beolvasása mezo classba
for mezo_nev in mezo_nevek:
    mezok[mezo_nev]=Mezo(str(mezo_nev), int(térkép.loc[i, "X"]), int(térkép.loc[i, "Y"]), int(térkép.loc[i, "víz szorzó"]), int(térkép.loc[i, "spice szorzó"]), str(térkép.loc[i, "pisztoly"]), str(térkép.loc[i, "lasgun"]), str(térkép.loc[i, "crysknife"]))
    i = i+1
#jatékosokat csinál
jatekosok = {}
kezdőmezők = ["C1","G1","K1","O1","Q3","Q7","O11","K15","G15","C11","A7","A3"]
for l in range(12):
    jatekosok[str(l+1)]=Jatekos(str(l), str(kezdőmezők[l]))
#mezo.ralepne dolgot tölti fel
j = 1
while j < 13:
    jatekos_lepes = pd.read_excel(lépés, sheet_name=str(j))
    lepesek = jatekos_lepes["rálép"]
    lepesek = lepesek.tolist()
    for lepes in lepesek:
        hibas_lepes = False
        for mezo in jatekosok[str(j)].mezok:
            if not szomszedos(mezok[mezo], mezok[lepes]):
                valid_lepes = True
            if hibas_lepes:
                lepesek.remove(lepes)
                print(str(j) + ". jatekos probalt lepni a " + lepes + " mezore, ami nem szomszedos egyik sajatjaval")

    for mezo in mezo_nevek:
        for k in range(len(lepesek)):
            if mezo == lepesek[k]:
                mezok[mezo].ralepne.append(str(j))
    lasgun = jatekos_lepes["lasgun"][0]
    crysknife = jatekos_lepes["crysknife"][0]
    pistol = jatekos_lepes["pisztoly"][0]
    legio = jatekos_lepes["légiók"][0]
    harvester_ár = 0
    if jatekos_lepes["harvester"][0]:
        harvester_ár = 5*pow(2, jatekosok[str(j)].telepitett_harvesterek + 1)
    ár = legio*3+crysknife+pistol+lasgun+harvester_ár
    if ár > jatekosok[str(j)].spice:
        print(str(j)+"elbaszta a költségvetést")
    else:
        jatekosok[str(j)].spice = jatekosok[str(j)].spice-ár
        jatekosok[str(j)].lasgun = jatekosok[str(j)].lasgun+lasgun
        jatekosok[str(j)].pistol = jatekosok[str(j)].pistol+pistol
        jatekosok[str(j)].crysknife = jatekosok[str(j)].crysknife+crysknife
        jatekosok[str(j)].legio=jatekosok[str(j)].legio+legio
        jatekosok[str(j)].telepitett_harvesterek = jatekosok[str(j)].telepitett_harvesterek + 1
        mezok[jatekos_lepes["harvester"][0]].harvester_telepites
    
    j = j+1

print(mezok["A1"].ralepne)







    
    
 
