###############################################################################
"""                                                                           #
Ez a fajl a tavalyi implementaciomat tartalmazza. Minden magyar nyelvu        #
komment azota kerult bele. Hasznos lehet a ./classes.py kialakitasahoz, ha    # 
nem abszolut nullarol akarunk indulni.                                        #
"""                                                                           #
###############################################################################
import pickle

"""
`moves`-kent hivatkozok a kodban arra a (meg nem letezo) dictionary-re, ami a 
jatekosok adott korben levo donteseit tartalmazza. Az volt az elkepzeles, hogy
ezt egy dedikalt script fogja beolvasni JSON/dictionary formaban. A strukturaja 
a kovetkezo:

{
    1:{
        wants:[I11, K2...]
        purchases: {
            weapons: [10, 2, 5, 0]
            harvester: [K1, L4]
        }
        leaves: []
    },
    2:...
    .
    .
    .
}
"""

weapon_types = {"crk":[1,1,3], "mpt":[3,1,1], "lsg":[1,3,1]}

class Game:
    """
    Singleton kontroller osztaly, ami a jatek lebonyolitasaert es a klonbozo
    osztalyok egymassal valo kommunikaciojaert felelos. 
    """
    def __init__(self):
        # a palya mezoinek egydimenzios listaja
        # az egyes mezok felelossege, hogy tudjak, hogy kik az o szomszedai
        self.fields: list[Fields] = None
        self.teams: list[Team] = None
    
        
    def conquest_moves(moves: dict) -> None:
        """
        vegrehajtaja azokat a lepeseket, amikkel a csapatok mezokre lepnek, 
        csataval egyutt
        """
        teams = (self.teams[int(i)] for i in moves)
        for team in teams:
            for field in moves[team]["wants"]:
                field = self.get_field(field)
                neighbor = any([field.is_neighbour(f) for f in team.fields])
                
                if not neighbor:
                    # ha rossz az adat es nem szomszedos mezot akarnak tamadni,
                    # akkor kihagyja az iteraciobol. ezt lehet erdemesebb
                    # error-handlinggel kezelni, mert igy csak siman nem tudunk
                    # a hibarol
                    continue

                uncontested = not field.is_contested(moves) and field.owner == None
                if uncontested:
                    print("{field.id} -> {team.num}, harc nélkül")
                    field.new_owner(team)
                    team.add_field(field)
                elif field.is_contested(moves):
                    contestants = [t for t in moves if field.id in t["wants"]]
                    if field.owner != None:
                        contestants.append(field.owner)
                    winner = combat_winner(field, contestants)
                    self.combat_aftermath(field, contestants, winner)

    def purchase_moves(moves: dict) -> None:
        """
        vegrehajta azokat a lepeseket, amikkel a csapatok vasarolnak
        """
        teams = (self.teams[int(i)] for i in moves)
        for team in teams:
            cost = team.next_harvester_cost() \
                + sum([weapon_types[w] for w in moves[team]["purchases"]["weapons"]]) \
                + moves[team]["purchases"]["weapons"][3]
            if team.spice < cost:
                pass

            team.purchase(moves[team]["purchases"]["weapons"], moves[team]["purchases"]["harvester"])

    def desert_moves(moves: dict) -> None:
        """
        vegrehajtja azokat a lepeseket, amikkel csapatunk elhagynak mezoket
        """
        teams = (self.teams[int(i)] for i in moves)
        for team in teams:
            for field in moves[team]["leaves"]:
                field = get_field(field)
                if field in team.fields:
                    team.remove_field(field)
                    field.owner = None

    def end_of_turn() -> None:
        for team in self.teams:
            team.comulate_water()
            team.comulate_spice()
            pass
            

    def combat_aftermath(field: Field, teams: list[Team], winner: Team) -> None:
        """
        a csata kimeneteletol fuggoen atadja a gyoztesnek a mezot, es levonja
        mindenkitol a megfelelo mennyisegu fegyvert
        """
        field.owner = None
        for team in teams:
            if team == winner:
                team.lose_weapons(True)
                field.owner = team
                if field not in team.fields:
                    team.add_field(field)
            else:
                team.lose_weapons(False)
                if field in team.fields:
                    team.remove_field(field)

    def get_field(id):
        """
        vesszater egy mezovel a dictionaryben szereplo id-je alapjan
        """
        pass

    def combat_winner(field: Field, teams: list[Team]) -> Team | None:
        """
        A csapatok harci ereje alapjan kiszamolja, hogy ki lenne a gyoztes es visszater vele.
        Ha tobb gyoztes is van, akkor None-al ter vissza.
        """
        team_CPs = sorted(
                [(team, self.calculate_combat_power(field, team)) for team in teams],\
                key=lambda x:x[1], reverse=True
            )
        CPs = [cp[1] for cp in CPs]
        if CPs.count(max(CPs)) > 1:
            return None
        else:
            return team_CPs[0][0]

    def load_data(self) -> None:
        pass

    def save_data(self) -> None:
        pass

    def calculate_combat_power(field: Field, team: Team) -> int:
        """
        Kiszamolja, hogy egy adott csapat mekkora harci erovel rendelkezik az
        adott mezon.
        """
        pass


class Field:
    def __init__(self, id, weapon_type, water, spice) -> None:
        self.id = id
        self.weapons = tuple(weapon_type)
        self.water = water
        self.spice = spice
        self.owner = None
        self.harvester = False
        self.neighbours = []

    def get_spice(self) -> int:
        """
        harvester jelenletetol fuggoen kiszamolja, hogy mennyi spice-t termel
        """
        return self.spice * [1, 2][self.harvester] 

    def new_owner(self, team: Team | None) -> None:
        self.owner = team

    def is_neighbour(self, field) -> bool:
        return field in self.neighbours
    
    def is_contested(self, moves: dict) -> bool:
        """
        ellenorzi, hogy lesz-e csata ezen a mezon
        """
        count = 0
        for team in moves:
            if self.id in team["wants"]:
                count += 1
        return count > 1

class Team:
    def __init__(self, num) -> None:
        # a csapat azonositoja, amivel a JSON-ban hivatkozunk ra
        self.num = num
        self.fields: list[Field] = None
        # 4-elemu lista, ami a csapat jelenlegi fegyvereinek szamat tarolja tipus szerint
        self.weapons = [0,0,0,0]
        self.spice = 10
        self.water = 7
        self.harvesters_built = 0

    def next_harvester_cost(self) -> int:
        return 10 * 2**self.harvesters_built

    def comulate_water(self) -> None:
        self.water += sum([f.water for f in self.fields])

    def comulate_spice(self) -> None:
        """
        hozzaadja a csapat spice mennyisegehez az osszes birtokolt mezo altal
        eloallitott spice-t
        """
        self.spice += sum([f.get_spice() for f in self.fields])

    def purchase(weapons: list[int], harvester: list[str]) -> None:
        pass

    def add_field(self, field) -> None:
        self.fields.append(field)

    def remove_field(self, field) -> None:
        self.fields.remove(field)

    def lose_weapons(won: bool) -> None:
        """
        a csata kimeneteletol fuggo mennyisegu fegyvert vesz el a csapattol
        """
        pass

    def print_stats(self) -> None:
        pass