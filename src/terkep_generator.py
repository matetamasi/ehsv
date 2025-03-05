from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from pathlib import Path

mezo_tipus = 1 #1:sivatag 0: hegy, 2: ures
fegyver_tipus = 2 #0: pistol, 1:lasgun, 2:knife, 3: külső
viz_szorzo = 10 #int
spice_szorzo = 15 #int
koordinata = "A69" #string

root = Path(__file__).parent.parent

resources = root / 'resources'
crysknife_png = resources / "crysknife.png"
lasgun_png = resources / "lasgun.png"
pistol_png = resources / "pistol.png"
hegy_png = resources / "hegy.png"
sivatag_png = resources / "sivatag.png"
ures_png = resources / "ures.png"
grid_png = resources / "grid.png"
font_path = resources / "Dune_Rise.otf"
terkep_fajl = resources / "terkep_adatok_2.xlsx"

#dune font
dune_font = ImageFont.truetype(font_path, 80)
#üres háttér
terkep_DF = pd.read_excel(terkep_fajl, sheet_name="adatok").fillna(0)
hex_map = Image.new("RGBA", (8944, 10098), (255, 255, 255, 0))
#mezők generálása és térképre helyezése
for i in range(len(terkep_DF)):
    mezo_nev = terkep_DF.loc[i, "mező"]
    fegyver_nev = terkep_DF.loc[i, "fegyver típus"]
    viz_szorzo = int(terkep_DF.loc[i, "víz szorzó"])
    spice_szorzo = int(terkep_DF.loc[i, "spice szorzó"])
    koordinata = terkep_DF.loc[i, "Koordináta"]
    X = terkep_DF.loc[i, "Xkoord"]
    Y = terkep_DF.loc[i, "Ykoord"]

    #mezo típus  
    if mezo_nev == "külső":
        mezo_tipus = 2
    elif (mezo_nev == "bázis") or (mezo_nev == "Hgs"):
        mezo_tipus = 0
    elif (mezo_nev == "Svt"):
        mezo_tipus = 1
    else: 
        print("Hiányzó mező típus: "+str(mezo_nev)+" a "+str(i+2)+". sorban")
    #fegyver típus
    if fegyver_nev == 0:
        fegyver_tipus = 3
    elif fegyver_nev == "Maula Pistol":
        fegyver_tipus = 0
    elif fegyver_nev == "Crysknife":
        fegyver_tipus = 2
    elif fegyver_nev == "Lasgun":
        fegyver_tipus = 2
    else: 
        print("Hiányzó fegyver típus: "+str(fegyver_nev)+" a "+str(i+2)+". sorban")
    if mezo_tipus == 0:
        hex_tile = Image.open(hegy_png).convert("RGBA")
    elif mezo_tipus == 1:
        hex_tile = Image.open(sivatag_png).convert("RGBA")
    else: 
        hex_tile = Image.open(ures_png).convert("RGBA")
    hex_w, hex_h = hex_tile.size

    #koordinata
    koord_img = Image.new("RGBA", (hex_w, hex_h), (255, 255, 255, 0)) 
    draw = ImageDraw.Draw(koord_img)
    number_text = koordinata
    koord_x, koord_y = hex_w // 2 , hex_h // 2 -250
    draw.text((koord_x, koord_y), number_text, fill="black", font=dune_font, anchor="mm")
    hex_tile = Image.alpha_composite(hex_tile, koord_img)

    #víz szorzó
    viz_szorzo_img = Image.new("RGBA", (hex_w, hex_h), (255, 255, 255, 0))  
    draw = ImageDraw.Draw(viz_szorzo_img)
    number_text = str(viz_szorzo)
    viz_x, viz_y = hex_w // 2 -230, hex_h // 2 +100
    draw.text((viz_x, viz_y), number_text, fill="black", font=dune_font, anchor="mm")
    rot_viz_szorzo = viz_szorzo_img.rotate(300, resample=Image.BICUBIC, center=(viz_x, viz_y)) 
    hex_tile = Image.alpha_composite(hex_tile, rot_viz_szorzo)

    #spice szorzó
    spice_img = Image.new("RGBA", (hex_w, hex_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(spice_img)
    number_text = str(spice_szorzo)
    spice_x, spice_y = hex_w // 2 +240, hex_h // 2 +60
    draw.text((spice_x, spice_y), number_text, fill="black", font=dune_font, anchor="mm")
    rot_spice_img = spice_img.rotate(60, resample=Image.BICUBIC, center=(spice_x, spice_y))
    hex_tile = Image.alpha_composite(hex_tile, rot_spice_img)

    #fegyver típus választása
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
    korrekcios_faktor = 0.855 #ahhoz kell, hogy ne legyenek rések a mezők között
    tile_size = (int(tile_width), int(tile_height))
    tile_x = X*tile_height*korrekcios_faktor
    tile_y = Y*tile_width*korrekcios_faktor
    hex_map.paste(hex_tile, (int(tile_x), int(tile_y)), hex_tile)
print("Türelem térképet terem!")
hex_map.show() 
