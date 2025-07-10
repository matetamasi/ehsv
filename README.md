# Dűne - stratégiai vetélkedő

A repó tartalma a dűne tematikájú stratégiai játék kiértékelését, játékállás számontartását,
illetve a fordulók közti térképgenerálást teszi lehetővé. A játék táborokban első sorban egész hetes
vetélkedőként működhet, mivel a lépések adminisztrációja (átvezetés akcióvezető lapról számítógépre) időigényes.
A játék előkészítéséről, szabályairól részletesebben a [játék dokumentumok](./jatek_dokumentumok/) mappában olvashatsz.

## Tudnivalók fejlesztéshez

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
