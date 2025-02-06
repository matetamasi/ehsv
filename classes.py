class Jatekos:
    def __init__(self, kezdomezo):
        self.mezo = [kezdomezo]
        self.spice = 10
        self.viz = 10
        self.lasgun = 0
        self.crysknife = 0
        self.pistol = 0
        self.legio = 0
    
    def mezore_lepes(self, mezok = list):
        for mezo in mezok:
            print("Jatekos ralepett a " + mezo + " mezore")


class Mezo:
    def __init__(self, nev, koordinata, viz, spice, fegyvertipus):
        self.nev = nev
        self.koordinata = koordinata
        self.viz = viz
        self.spice = spice
        self.fegyvertipus = fegyvertipus
        self.harvester = 0
        self.birtokos = 0

    
    
 