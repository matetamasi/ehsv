legio_szorzo = 3
legio_ar = 2
harvester_kezdeti_ar = 5
# állás kiszámítása
from typing import List, Tuple, Dict
import pandas as pd
import math
import sys
from pathlib import Path

# térkép generálás
from PIL import Image, ImageDraw, ImageFont
import matplotlib.colors as mcolors


# print-ek átirányítása
class StringStream:
    def __init__(self):
        self.data = ""

    def write(self, s):
        self.data += s

    def flush(self):
        pass


# Nullával feltöltött stringgé alakítás, hogy az ABC sorrend a növekvő sorrend legyen
def zstr(x: int, zeroes: int = 2) -> str:
    return str(x).zfill(zeroes)


def valid_harvester(harvester_koord: str, jatekos: str) -> bool:
    return (
        harvester_koord in jatekosok[jatekos].mezok
        and mezok[harvester_koord].harvester == 0
    )


# A mező szomszédja-e B-nek
def szomszedos(A, B):
    if A.nev == "Z0" or B.nev == "Z0":
        return True
    if abs(A.X - B.X) <= 1 and abs(A.Y - B.Y) <= 1:
        if A.X - B.X == -1 and A.Y - B.Y == 1:
            return False
        if A.X - B.X == 1 and A.Y - B.Y == -1:
            return False
        else:
            print(str(A), "szomszédja", str(B))
            return True
    else:
        return False


class Jatekos:
    def __init__(self, nev, kezdomezo):
        self.nev = nev
        self.mezok: List[str] = [kezdomezo]
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

    def mezore_lepes(self, uj_mezok: list):
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
        ossz_fogyasztas = -sum([mezok[m].viz for m in self.mezok])

        if ossz_fogyasztas > self.viz:
            print("Túl sok a vízfogyasztás!")
            print(str(self.viz) + "volt, de" + str(ossz_fogyasztas) + " fogyott")
            elvesztett_mezok = [e for e in self.mezok if mezok[e].viz < 0]

            self.mezorol_lelepes(elvesztett_mezok)
            return True
        else:
            print("nincs baj a vizzel")
            print(str(self.viz) + "-ből" + str(ossz_fogyasztas) + " fogyott")
            self.viz -= ossz_fogyasztas
            return False

    def spice_termeles(self):
        print(f"\t{self.nev} termelése:")
        for mezo in self.mezok:
            self.spice = self.spice + mezok[mezo].spice
            print(
                "\t\ta "
                + mezo
                + " mezőn "
                + str(mezok[mezo].spice)
                + " darab spice-ot termelt"
            )

    def fegyver_vesztes(self):
        print("### Fegyverek ###")
        print("A játékos" + self.nev)
        print("pistol, lasgun, knife, legio")
        print(self.pistol)
        print(self.lasgun)
        print(self.crysknife)
        print(self.legio)
        szorzo = 1 - (0.1 * self.veresegek_szama + 0.2 * self.gyozelmek_szama)
        if szorzo < 0:
            szorzo = 0
        print("vesztések" + str(self.veresegek_szama))
        print("győzelmek" + str(self.gyozelmek_szama))
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
    def __init__(self, nev, X, Y, viz, spice, pistol, lasgun, crysknife, tipus):
        self.nev = nev
        self.X = X
        self.Y = Y
        self.viz = viz
        self.spice = spice
        self.pistol = pistol
        self.lasgun = lasgun
        self.crysknife = crysknife
        self.tipus = tipus
        self.harvester = 0
        self.birtokos: str = ""
        self.ralepne: List[str] = []

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
            print("### Harc ###" + str(self.nev))
            print("jatekos " + jatekosok[jatekos].nev)
            hadero = (
                self.pistol * jatekosok[jatekos].pistol
                + self.lasgun * jatekosok[jatekos].lasgun
                + self.crysknife * jatekosok[jatekos].crysknife
            )
            print("hadero: " + str(hadero))
            if self.nev not in jatekosok[jatekos].mezok:
                hadero = hadero + legio_szorzo * jatekosok[jatekos].legio
            haderok[jatekosok[jatekos].nev] = hadero

        max_hadero = max(haderok.values())
        max_jatekosok = [key for key, value in haderok.items() if value == max_hadero]
        gyoztes = 0
        if len(max_jatekosok) == 1:
            gyoztes = max_jatekosok[0]
        for jatekos in self.ralepne:
            if jatekos == gyoztes:
                if self.nev not in jatekosok[jatekos].mezok:
                    print(
                        jatekosok[jatekos].nev
                        + "új győzelmet kapott a "
                        + self.nev
                        + " mezőn"
                    )
                    jatekosok[jatekos].gyozelmek_szama = (
                        jatekosok[jatekos].gyozelmek_szama + 1
                    )
                jatekosok[jatekos].mezore_lepes([self.nev])
            else:
                if self.nev not in jatekosok[jatekos].mezok:
                    print(
                        jatekosok[jatekos].nev
                        + "új vereséget kapott a "
                        + self.nev
                        + " mezőn"
                    )
                    jatekosok[jatekos].veresegek_szama = (
                        jatekosok[jatekos].veresegek_szama + 1
                    )


######### TÉRKÉP ###########
def terkep_gen(kor, kor_allapot, resources, terkep_mentes):
    # mezők paramétereinek a változói
    mezo_tipus = 1  # 1:sivatag 0: hegy, 2: ures
    fegyver_tipus = 2  # 0: pistol, 1:lasgun, 2:knife, 3: külső
    viz_szorzo = 10  # int
    spice_szorzo = 15  # int
    koordinata = "A69"  # string

    # adatfájlok, képelemek elérési útjainak a beolvasása

    crysknife_png = resources / "crysknife.png"
    lasgun_png = resources / "lasgun.png"
    pistol_png = resources / "pistol.png"
    hegy_png = resources / "hegy.png"
    sivatag_png = resources / "sivatag.png"
    ures_png = resources / "ures.png"
    grid_png = resources / "grid.png"
    font_path = resources / "Times-New-Roman.otf"  # rossz font, mert a jó szar
    jatekos_szimbolum = resources / "fremen_ikon.png"
    terkep_fajl = resources / "terkep_adatok_2.xlsx"  # teszt
    # jatek_allas = veg_terkep_allas  # az imént kiírt térképfájl alapján

    # pandas DF-ek, ezekben van az aktuális állás, illtve a térképen a jelölők
    jatekos_szinek = pd.read_excel(terkep_fajl, sheet_name="játékos színek")
    mezo_birtokos_DF = terkep_mentes
    terkep_DF = pd.read_excel(terkep_fajl, sheet_name="adatok").fillna(0)

    # üres háttér
    hex_map = Image.new("RGBA", (8944, 10098), (255, 255, 255, 0))
    # dune font
    dune_font = ImageFont.truetype(font_path, 80)

    # mezők generálása és térképre helyezése
    for i in range(len(terkep_DF)):
        # adatfájlokból a mező paramétereinek a kiolvasása
        mezo_nev = terkep_DF.loc[i, "mező"]
        harvester = mezo_birtokos_DF.loc[i, "Harvester"]
        fegyver_nev = terkep_DF.loc[i, "fegyver típus"]
        viz_szorzo = int(terkep_DF.loc[i, "víz szorzó"])
        spice_szorzo = int(terkep_DF.loc[i, "spice szorzó"])
        koordinata = terkep_DF.loc[i, "Koordináta"]
        X = terkep_DF.loc[i, "Xkoord"]
        Y = terkep_DF.loc[i, "Ykoord"]

        # mezo típus hozzárendelés az excelben levő nevek alapján
        if mezo_nev == "külső":
            mezo_tipus = 2
        elif (mezo_nev == "bázis") or (mezo_nev == "Hgs"):
            mezo_tipus = 0
        elif mezo_nev == "Svt":
            mezo_tipus = 1
        else:
            mezo_tipus = 2
            print(
                "Hiányzó mező típus: " + str(mezo_nev) + " a " + str(i + 2) + ". sorban"
            )
        # fegyver típus hozzárendelés az excelben levő nevek alapján
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
            print(
                "Hiányzó fegyver típus: "
                + str(fegyver_nev)
                + " a "
                + str(i + 2)
                + ". sorban"
            )

        # megfelelő háttér kiválasztása a mező háttere alapján
        if mezo_tipus == 0:
            hex_tile = Image.open(hegy_png).convert("RGBA")
        elif mezo_tipus == 1:
            hex_tile = Image.open(sivatag_png).convert("RGBA")
        else:
            hex_tile = Image.open(ures_png).convert("RGBA")

        # mező háttér alapján méret kiszedése
        hex_w, hex_h = hex_tile.size

        # koordinata felirat ráhelyezése a mezőre
        koord_img = Image.new("RGBA", (hex_w, hex_h), (255, 255, 255, 0))
        draw = ImageDraw.Draw(koord_img)
        number_text = koordinata
        koord_x, koord_y = (
            hex_w // 2,
            hex_h // 2 - 250,
        )  # itt játszani kell a hellyel, hogy hova kerüljön
        draw.text(
            (koord_x, koord_y), number_text, fill="black", font=dune_font, anchor="mm"
        )
        hex_tile = Image.alpha_composite(hex_tile, koord_img)

        # víz szorzó felirat ráhelyezése a mezőre
        viz_szorzo_img = Image.new("RGBA", (hex_w, hex_h), (255, 255, 255, 0))
        draw = ImageDraw.Draw(viz_szorzo_img)
        number_text = str(viz_szorzo)
        viz_x, viz_y = (
            hex_w // 2 - 230,
            hex_h // 2 + 100,
        )  # itt játszani kell a hellyel, hogy hova kerüljön
        draw.text(
            (viz_x, viz_y), number_text, fill="black", font=dune_font, anchor="mm"
        )
        rot_viz_szorzo = viz_szorzo_img.rotate(
            300, resample=Image.BICUBIC, center=(viz_x, viz_y)
        )
        hex_tile = Image.alpha_composite(hex_tile, rot_viz_szorzo)

        # spice szorzó
        spice_img = Image.new("RGBA", (hex_w, hex_h), (255, 255, 255, 0))
        draw = ImageDraw.Draw(spice_img)
        if harvester == 1:  # van-e harvester a mezőn
            number_text = str(spice_szorzo * 2)
            spice_szorzo_szin = "red"
        else:
            number_text = str(spice_szorzo)
            spice_szorzo_szin = "black"
        spice_x, spice_y = (
            hex_w // 2 + 240,
            hex_h // 2 + 60,
        )  # itt játszani kell a hellyel, hogy hova kerüljön
        draw.text(
            (spice_x, spice_y),
            number_text,
            fill=spice_szorzo_szin,
            font=dune_font,
            anchor="mm",
        )
        rot_spice_img = spice_img.rotate(
            60, resample=Image.BICUBIC, center=(spice_x, spice_y)
        )
        hex_tile = Image.alpha_composite(hex_tile, rot_spice_img)

        # birtokos jelző rárakás
        birtokos = str(mezo_birtokos_DF.loc[i, "Birtokos"])
        colors = mcolors.CSS4_COLORS  # Dictionary of color names
        # birtokos jelző fekete pixeleineka az átszínezése a szükséges színre
        if birtokos in jatekosok.keys():
            for i in range(len(jatekos_szinek)):
                if str(jatekos_szinek.loc[i, "Játékos"]) == str(birtokos):
                    szin = jatekos_szinek.loc[i, "Szín"]
            colors = mcolors.CSS4_COLORS
            colour_hex = mcolors.to_rgba(szin, alpha=1)
            colour_rgb = tuple(int(c * 255) for c in colour_hex)
            ikon = Image.open(jatekos_szimbolum).convert("RGBA")
            # chatgpt hagyatéka
            # Get pixel data
            data = ikon.getdata()
            # Create a new image with recolored pixels
            new_data = []
            for r, g, b, a in data:
                if (
                    a > 0 and r < 50 and g < 50 and b < 50
                ):  # Keep transparency, recolor only dark pixels
                    new_data.append(colour_rgb)
                else:
                    new_data.append((r, g, b, a))  # Keep other pixels unchanged
            ikon.putdata(new_data)
            max_size = (200, 200)
            ikon.thumbnail(max_size)
            ikon_x = (hex_w - ikon.width) // 2
            ikon_y = (hex_h - ikon.height) // 2
            hex_tile.paste(ikon, (ikon_x, ikon_y), ikon)

        # fegyver típus választása, itt minden fegyver képe más, ezért változnak a koordináták
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
        korrekcios_faktor = 0.855  # ahhoz kell, hogy ne legyenek rések a mezők között, ha csökken a szám közelebb kerülnek, ha nő akkor nő, felező módszerrel szépen meg lehet találni az ideális értéket
        tile_size = (int(tile_width), int(tile_height))
        tile_x = X * tile_height * korrekcios_faktor
        tile_y = Y * tile_width * korrekcios_faktor
        hex_map.paste(hex_tile, (int(tile_x), int(tile_y)), hex_tile)
    print("Türelem térképet terem!")
    hex_map.save(kor_allapot / f"{kor}terkep.png", format="PNG")


######### TÉRKÉP VÉGE ###########


def init(args_kor: int | None, csak_terkep: bool = False) -> Tuple[
    Path,  # root
    Path,  # resources
    Path,  # output_dir
    StringStream,  # log
    int,  # kor
    Dict[str, Mezo],  # mezok
    Dict[str, Jatekos],  # jatekosok
]:
    print(f"DEBUG INIT: csak_terkep={csak_terkep}")
    print(f"DEBUG INIT: args_kor={args_kor}")
    sys.stdout = stringStream = StringStream()

    # a repo gyokerenek az eleresi utvonala:
    root = Path(__file__).parent.parent
    allapot = root / "allapot"

    # körszám kiszámítása
    kor = (
        (
            max(
                [
                    int(x.name)
                    for x in allapot.iterdir()
                    if x.is_dir() and x.name.isdigit()
                ]
                + [-1]  # Ha nincs elem, 0. kör jön
            )
            + (
                0 if csak_terkep else 1
            )  # csak térkép esetén a legnagyobb mappával dolgozunk, nem a kövivel
        )
        if args_kor == None
        else args_kor
    )
    print(f"DEBUG INIT: kor={kor}")

    elozo_kor_allapot = allapot / zstr(kor - 1)
    kor_allapot = allapot / zstr(kor)

    # a 'resources' mappa eleresi utvonala:
    resources = root / "resources"
    terkepadat = resources / "terkep_adatok_2.xlsx"

    # kör kezdőállása
    kezdo_jatekos_allas = (
        elozo_kor_allapot / "jatekos.csv"
        if kor > 0
        else resources / "kezdo_jatekos.csv"
    )
    kezdo_terkep_allas = (
        elozo_kor_allapot / "terkep.csv" if kor > 0 else resources / "kezdo_terkep.csv"
    )
    # térképes excel elérése
    terkep_allas = pd.read_excel(terkepadat, sheet_name="adatok").fillna(0)
    szinek = pd.read_excel(terkepadat, sheet_name="játékos színek")

    térkép = pd.read_excel(terkepadat, sheet_name="adatok").fillna(0)
    mezo_nevek: List[str] = []

    for a in range(len(térkép)):
        mezo_nevek.append(térkép.loc[a, "Koordináta"])
    mezok: Dict[str, Mezo] = {}

    # térkép adatainak a beolvasása mezo classba
    i = 0
    for mezo_nev in mezo_nevek:
        mezok[mezo_nev] = Mezo(
            str(mezo_nev),
            int(térkép.loc[i, "X"]),
            int(térkép.loc[i, "Y"]),
            int(térkép.loc[i, "víz szorzó"]),
            int(térkép.loc[i, "spice szorzó"]),
            int(térkép.loc[i, "pisztoly"]),
            int(térkép.loc[i, "lasgun"]),
            int(térkép.loc[i, "crysknife"]),
            str(térkép.loc[i, "mező"])
        )
        i = i + 1
    # nullelem a mezők között
    mezok["Z0"] = Mezo(
        "Z0", 100, 100, 0, 0, 0, 0, 0, "Svt"
    )  # TODO: ettől meg kellene szabadulni
    # jatékosokat csinál
    jatekosok: Dict[str, Jatekos] = {}
    kezdőmezők = [
        "C1",
        "G1",
        "K1",
        "O1",
        "Q3",
        "Q7",
        "O11",
        "K15",
        "G15",
        "C11",
        "A7",
        "A3",
    ]
    for l in range(1, 13):
        jatekosok[str(l)] = Jatekos(str(l), str(kezdőmezők[l - 1]))
        mezok[kezdőmezők[l - 1]].birtokos = str(l)

    # kezdeti jatékállást beolvas
    kezdeti_allas = pd.read_csv(kezdo_jatekos_allas)
    for i in range(1, 13):
        jatekosok[str(i)].viz = kezdeti_allas.loc[i - 1, "viz"]
        jatekosok[str(i)].spice = kezdeti_allas.loc[i - 1, "spice"]
        jatekosok[str(i)].lasgun = kezdeti_allas.loc[i - 1, "lasgun"]
        jatekosok[str(i)].pistol = kezdeti_allas.loc[i - 1, "pisztoly"]
        jatekosok[str(i)].crysknife = kezdeti_allas.loc[i - 1, "crysknife"]
        jatekosok[str(i)].legio = kezdeti_allas.loc[i - 1, "legio"]
        jatekosok[str(i)].telepitett_harvesterek = kezdeti_allas.loc[
            i - 1, "telepitesek"
        ]
    kiindulo_terkep = pd.read_csv(kezdo_terkep_allas)
    print(f"kiinduló térkép: {kiindulo_terkep}")
    for j in range(len(kiindulo_terkep)):
        if kiindulo_terkep.loc[j, "Harvester"] == 1:
            print(kiindulo_terkep.loc[j, "Mezo_nev"] + "-en hozott harvester van")
            mezok[kiindulo_terkep.loc[j, "Mezo_nev"]].harvester_telepites()

    for k in range(1, 13):
        birtok = []
        for j in range(len(kiindulo_terkep)):
            if kiindulo_terkep.loc[j, "Birtokos"] == k:
                birtok.append(kiindulo_terkep.loc[j, "Mezo_nev"])
                mezok[kiindulo_terkep.loc[j, "Mezo_nev"]].birtokos = str(k)
        jatekosok[str(k)].mezok = birtok

    return (root, resources, kor_allapot, stringStream, kor, mezok, jatekosok)


### init eddig

# játék ciklusa


def gameloop(
    root: Path,
    resources: Path,
    kor_allapot: Path,
    mezok: Dict[str, Mezo],
    jatekosok: Dict[str, Jatekos],
    utolso_kor: bool,
    regen: bool = False,
):
    mezo_nevek: List[str] = list(mezok.keys())
    lepes_fajl = root / "lepes.xlsx" if not regen else kor_allapot / "lepes.xlsx"
    for jatekos in jatekosok.keys():
        jatekos_lepes = pd.read_excel(lepes_fajl, sheet_name=jatekos).fillna(0)
        lelepesek = jatekos_lepes["lelép"]
        for lelepes in lelepesek:
            if lelepes in jatekosok[jatekos].mezok and lelepes in mezok:
                print(f"{jatekosok[jatekos].nev} lelépett a(z) {lelepes} mezőről")
                jatekosok[jatekos].mezok.remove(lelepes)
                mezok[lelepes].birtokos = ""
        if jatekosok[jatekos].elfogy_e_viz():
            print("Elfogyott a viz, " + str(jatekos) + ". jatekos köre kihagyva")
            jatekosok[jatekos].viz = 0
            # TODO azért kell mert, ha elfogyott a víz akkor nem volt feltöltve a vásárlások dict ami gondot okoz, ezen kell szerintem majd vátoztatni, mert a vásárlás ettől még lefuthatna, de ekkora módosítást nem akarok csinálni playtest közben
            jatekosok[jatekos].vasarlasok["lasgun"] = 0
            jatekosok[jatekos].vasarlasok["pistol"] = 0
            jatekosok[jatekos].vasarlasok["crysknife"] = 0
            jatekosok[jatekos].vasarlasok["legio"] = 0
        else:
            lepesek = jatekos_lepes["rálép"].tolist()
            lepesek = ["Z0" if l == 0 else l for l in lepesek]
            print(str(jatekos) + ". jatekos lepesei")
            print(lepesek)

            # A lépések minden olyan eleme, amelyre a játékos mezőinek
            # van olyan eleme, hogy a két mező szomszédos
            lepesek = [
                l
                for l in lepesek
                if True
                in [  # bool-lista, játékos mezői minden elemére szomszédosság l-el
                    szomszedos(mezok[l], mezok[j_mezo])
                    for j_mezo in jatekosok[jatekos].mezok
                ]
            ]
            
            #ha a mező "külső" típussal rendelkezik akkor a lépések közül eltávolítjuk
            kulso_lepes = [] 
            for mezo in lepesek: 
                if mezok[mezo].tipus == "külső":
                    print(str(jatekos) + ". térképen kívül próbált lépni a: " + str(mezo) + " mezőre")
                    kulso_lepes.append(mezo)
            for mezo in kulso_lepes:
                lepesek.remove(mezo)

            lelepesek = jatekos_lepes["lelép"]

            for lepes in lepesek:
                if lepes in mezo_nevek:
                    mezok[lepes].ralepne.append(jatekos)

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

            harvester_koltseg = harvester_kezdeti_ar * pow(
                2, jatekosok[jatekos].telepitett_harvesterek
            )

            harvester_sikerult = False

            if (
                not jatekos_lepes["harvester"].empty
                and bool(pd.notna(jatekos_lepes["harvester"][0]))
                and jatekos_lepes["harvester"][0] != 0
                and jatekos_lepes["harvester"].iloc[0] != 0
            ):

                if valid_harvester(str(jatekos_lepes["harvester"][0]), jatekos):
                    print(
                        f"{jatekosok[jatekos].nev} harvestert telepítene {harvester_koltseg}-ért"
                    )
                    harvester_sikerult = True
                else:
                    print(str(jatekos) + " rossz helyre raknak harvestert")

            ár = legio * legio_ar + crysknife + pistol + lasgun

            if harvester_sikerult:
                ár += harvester_koltseg

            if ár > jatekosok[jatekos].spice:
                print(jatekos + "túlköltekezett!")
                print(f"{ár}-ba került volna, de csak {jatekosok[jatekos].spice} van")
                jatekosok[jatekos].vasarlasok["lasgun"] = 0
                jatekosok[jatekos].vasarlasok["pistol"] = 0
                jatekosok[jatekos].vasarlasok["crysknife"] = 0
                jatekosok[jatekos].vasarlasok["legio"] = 0
            else:
                print(f"{jatekosok[jatekos].nev} vásárol {ár}-ért.")
                jatekosok[jatekos].spice = jatekosok[jatekos].spice - ár
                jatekosok[jatekos].vasarlasok["lasgun"] = int(lasgun)
                jatekosok[jatekos].vasarlasok["pistol"] = int(pistol)
                jatekosok[jatekos].vasarlasok["crysknife"] = int(crysknife)
                jatekosok[jatekos].vasarlasok["legio"] = int(legio)

                if harvester_sikerult:
                    print(
                        str(jatekos_lepes["harvester"][0]) + " mezőre harvester került"
                    )
                    mezok[str(jatekos_lepes["harvester"][0])].harvester_telepites()
                    jatekosok[jatekos].telepitett_harvesterek += 1

            if not utolso_kor:
                print(f"### Spice termelés: ###")
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
        jatekosok[jatekos].lasgun = (
            jatekosok[jatekos].lasgun + jatekosok[jatekos].vasarlasok["lasgun"]
        )
        jatekosok[jatekos].crysknife = (
            jatekosok[jatekos].crysknife + jatekosok[jatekos].vasarlasok["crysknife"]
        )
        jatekosok[jatekos].pistol = (
            jatekosok[jatekos].pistol + jatekosok[jatekos].vasarlasok["pistol"]
        )
        jatekosok[jatekos].legio = (
            jatekosok[jatekos].legio + jatekosok[jatekos].vasarlasok["legio"]
        )
    if utolso_kor:
        print(f"### Utolsó körös spice termelés: ###")
        for jatekos in jatekosok.values():
            jatekos.spice_termeles()

    # játékállás printoutot csinál egy dataframebe majd csv-be
    fejlec = [
        "jatekos",
        "viz",
        "spice",
        "lasgun",
        "pisztoly",
        "crysknife",
        "legio",
        "telepitesek",
    ]
    jatekosallas_mentes = pd.DataFrame(columns=fejlec)
    for i in range(1, 13):
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

    terkep_mentes = pd.DataFrame(columns=["Mezo_nev", "Birtokos", "Harvester"])
    for mezo in mezo_nevek:
        uj_sor = []
        uj_sor.append(mezo)
        b = mezok[mezo].birtokos
        uj_sor.append(b if b != "" else "0")
        if mezok[mezo].harvester == 1:
            uj_sor.append(1)
        else:
            uj_sor.append(0)
        terkep_mentes.loc[len(terkep_mentes)] = uj_sor

    return (terkep_mentes, jatekosallas_mentes)


def mentes(terkep_mentes, jatekosallas_mentes, kor_allapot, regen: bool = False):
    eredeti_lepes_fajl = res / "lepes.xlsx"  # kör lépéseinek az excele
    lepes_fajl = root / "lepes.xlsx" if not regen else kor_allapot / "lepes.xlsx"
    backup_lepes_fajl = kor_allapot / "lepes.xlsx"
    veg_jatekos_allas = kor_allapot / "jatekos.csv"  # kör végállása
    veg_terkep_allas = kor_allapot / "terkep.csv"  # kör harvesterei végben

    log_fajl = kor_allapot / ("log" + zstr(kor) + ".txt")
    # mappa létrehozása (csak amint elkezdenénk bele írni)
    kor_allapot.mkdir(exist_ok=True)

    jatekosallas_mentes.to_csv(veg_jatekos_allas, index=False)
    terkep_mentes.to_csv(veg_terkep_allas, index=False)

    # Lépés fájl elmentése és ürítése
    if not regen:
        backup_lepes_fajl.write_bytes(lepes_fajl.read_bytes())
        lepes_fajl.write_bytes(eredeti_lepes_fajl.read_bytes())

    # log kiírása és mentése
    log_fajl.write_text(stringStream.data)
    sys.stdout = sys.__stdout__
    print(stringStream.data)


hasznalat = """

A program használata: python {path} <körszám> <további argumentumok>
A kör száma és az argumentumlista kihagyható, ezesetben \
a {root}/allapot mappában található legutóbbi körből kiindulva a \
{root}/lepes.xlsx fájlba beírt lépések hajtódnak végre.

lehetséges argumentumok:
    4 : soron következő helyett 4. kör végrehajtása (tetszőleges másik számmal is használható)
    utolso : Kör lejátszása utolsó körként. Ezesetben a spice termelés a kör legvégén történik.
    csak-lepes : csak a lépést végrehajtása, térképgenerálás nélkül
    csak-terkep : csak a térkép generálása a legutóbbi (vagy a megadott) körhöz
    regen : A {root}/allapot-ban lévő összes kör újrajátszása az azokban található lepes.xlsx-ek alapján (ezesetben \"utolso\"-n kívül más argumentum nem adható meg)
""".format(
    path=Path(__file__).name, root=str(Path(__file__).parent.parent)
)


def parse_argv(argv: List[str]):
    valid_args = ["csak-lepes", "csak-terkep", "utolso", "regen"]
    allapot = Path(__file__).parent.parent / "allapot"
    kor: int | None = None
    for arg_index in range(1, len(argv)):
        if argv[arg_index].isdigit():
            if kor != None:  # Már van megadva körszám
                print(
                    f"Hibás argumentum: {argv[arg_index]}!\n"
                    + f"Már a {kor} körszámot is megadtad."
                    + " Csak egy kör sorszámát add meg!"
                )
                print(hasznalat)
                exit()
            else:
                kor = int(argv[arg_index])
                if kor < 0:
                    print("Nullánál kisebb körszám nem lehetséges!")
                    print(hasznalat)
                    exit()
                maxkor = (
                    max(
                        [
                            int(x.name)
                            for x in allapot.iterdir()
                            if x.is_dir() and x.name.isdigit()
                        ]
                        + [-1]
                    )
                    + 1
                )

                if kor > maxkor:
                    print(
                        f"A(z) {kor}. kör nem játszható le, mert a(z) {kor-1}. adatai nem találhatók!"
                    )
                    print(hasznalat)
                    exit()
        elif argv[arg_index] in valid_args:
            valid_args.remove(argv[arg_index])
        else:
            print(f"Hibás argumentum: {argv[arg_index]}!")
            print(hasznalat)
            exit()

    csak_lepes = "csak-lepes" in argv
    csak_terkep = "csak-terkep" in argv
    utolso = "utolso" in argv
    regen = "regen" in argv
    if regen:
        sys.stdout = sys.__stdout__
        igen = input(
            'Vigyázz, destruktív folyamat!!!\nKészíts másolatot az "allapot" mappáról.\nLemásoltad?\n>> '
        )
        if igen.lower() != "igen":
            print(
                'A program leáll. A folytatáshoz készíts egy másolatot, majd írd be, hogy "igen".',
                file=sys.__stdout__,
            )
            exit()
    if (kor != None and regen) or ((csak_lepes or csak_terkep) and regen):
        print(
            'Újragenerálás és más argumentum egyszerre nem lehetséges (leszámítva az "utolso"-t)!'
        )
        print(hasznalat)
        exit()
    if csak_lepes and csak_terkep:
        print("Csak térkép és csak lépés egyszerre nem lehetséges!")
        print(hasznalat)
        exit()
    if csak_terkep and utolso:
        print(
            "Csak térkép és utolsó kör egyszerre nem lehetséges, mert ezek nincsenek hatással egymásra."
            + "A térképgenerálás már meglévő adatokból dolgozik, így nem számít, hogy utolsó kör van-e."
            + "Ha az utolsó kör lépése már lement, és csak térképet szeretnél generálni, ezt a"
            + f"\n\npython {Path(__file__).name} csak-terkep\n\nparanccsal teheted."
        )
        print(hasznalat)
        exit()
    return (kor, utolso, regen, csak_lepes, csak_terkep)


(args_kor, utolso, regen, csak_lepes, csak_terkep) = parse_argv(sys.argv)
if regen:
    root = Path(__file__).parent.parent
    allapot = root / "allapot"
    kor_index = max(  # hanyadik a legutóbbi kör allapot-ban
        [int(x.name) for x in allapot.iterdir() if x.is_dir() and x.name.isdigit()]
        + [-1]
    )
    if kor_index < 0:
        print("Még nincs lefuttatot kör, nincs mit újragenerálni!")
        exit()
    for k in range(0, kor_index + 1):
        (root, res, kor_all, stringStream, kor, mezok, jatekosok) = init(k)
        (terkep_m, jatekos_m) = gameloop(
            root,
            res,
            kor_all,
            mezok,
            jatekosok,
            utolso_kor=(utolso and k == kor_index),
            regen=True,
        )
        mentes(terkep_m, jatekos_m, kor_all, regen=True)
        terkep_gen(kor, kor_all, res, terkep_m)
else:
    (root, res, kor_all, stringStream, kor, mezok, jatekosok) = init(
        args_kor, csak_terkep
    )
    print(f"kor: {kor}", file=sys.__stdout__)
    if not csak_terkep:
        (terkep_m, jatekos_m) = gameloop(root, res, kor_all, mezok, jatekosok, utolso)
        mentes(terkep_m, jatekos_m, kor_all)
    sys.stdout = sys.__stdout__
    if not csak_lepes:
        # Ha csak térképet generálunk, a terkep_m üres
        terkep_m = pd.read_csv(kor_all / "terkep.csv")
        terkep_gen(kor, kor_all, res, terkep_m)
