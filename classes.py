
class Jatekos:
    def __init__(self, kezdomezo):
        self.mezok = [kezdomezo]
        self.spice = 10
        self.viz = 10
        self.lasgun = 0
        self.crysknife = 0
        self.pistol = 0
        self.legio = 0
    
    def mezore_lepes(self, mezok = list):
        for mezo in mezok:
            self.mezok.append(mezo)
    
    def mezorol_lelepes(self, mezok):
        for mezo in mezok:
            self.mezok.remove(mezo)

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
        



class Mezo:
    def __init__(self, nev, koordinata, viz, spice, fegyvertipus):
        self.nev = nev
        self.koordinata = koordinata
        self.viz = viz
        self.spice = spice
        self.fegyvertipus = fegyvertipus
        self.harvester = 0
        self.birtokos = 0
        self.ralepne = []
    def havester_telepites(self):
        self.harvester = 1
        self.spice = self.spice * 2

    def lepesek_szetvalasztas(self):
        if len(self.ralepne) == 1:
            self.ralepne[0].mezore_lepes([self.nev])
    
    def harc(self):
        pass
        

jatekos1 = Jatekos("A1")
jatekos1.spice = jatekos1.spice + 2
jatekos2 = Jatekos("B2")

mezok = {}
nevek = ["A1", "B2"]
mezok[nevek[0]] = Mezo("A1", [1,0], 7, 1, "k")
mezok[nevek[1]] = Mezo("B2", [2,3], -4, 1, "p")
jatekos1.mezore_lepes(["B2"])







    
    
 