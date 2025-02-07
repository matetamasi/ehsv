## Tudnivalók

Légyszi a kódban ne legyenek ékezetes változónevek, fájlnevek ne tartalmazzanak ékezetet, space-t, vagy bármit ezek közül: #%&{}\\<>*?/$!'":@+`|=

Fájl elérési útvonalat lehetőleg unix jelöléssel adj meg, és akkor nem kell minden elé \\-t tenni. Pl: `C:/Users/bohoc/Documents/ehsv`

## Telepítés

### A repo klónozása:

VSCode-ban: 

- ctrl+shift+e > Clone Repository > https://github.com/domahet/ehsv.git

Parancssorból: 

```console
$ cd path/to/folder/
$ git clone https://github.com/domahet/ehsv.git
$ cd ehsv/
```

### venv inicializálása (opcionális, de ajánlott)

Ezt a PyCharm megcsinálja neked ingyen, a VSCode nem hiszem.

```console
$ python -m venv .venv/
$ .venv/Scripts/activate #ezt minden sessionben
```

### Csomagok telepítése

```console
$ pip install -r requirements.txt
```