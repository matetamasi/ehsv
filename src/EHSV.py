###############################################################################
"""                                                                           #
Ez a fajl a tavalyi implementaciomat tartalmazza. Minden magyar nyelvu        #
komment azota kerult bele. Hasznos lehet a ./classes.py kialakitasahoz, ha    # 
nem abszolut nullarol akarunk indulni.                                        #
"""                                                                           #
###############################################################################
import pickle

"""JSON structure
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

class Map:
    def __init__(self):
        self.fields: list[Fields] = None
        self.teams: list[Team] = None
    
        
    def conquest_moves(moves: dict) -> None:
        teams = (self.teams[int(i)] for i in moves)
        for team in teams:
            for field in moves[team]["wants"]:
                field = get_field(field)
                neighbor = any([field.is_neighbour(f) for f in team.fields])
                
                if not neighbor:
                    pass

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
        teams = (self.teams[int(i)] for i in moves)
        for team in teams:
            cost = team.harvester_cost() + sum([weapon_types[w] for w in moves[team]["purchases"]["weapons"]]) + moves[team]["purchases"]["weapons"][3]
            if team.spice < cost:
                pass

            team.purchase(moves[team]["purchases"]["weapons"], moves[team]["purchases"]["harvester"])

    def desert_moves(moves: dict) -> None:
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
            

                    

    def combat_aftermath(field: Field, teams: list[Team], winner: Team) -> None:
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
        pass

    def combat_winner(field: Field, teams: list[Team]) -> Team | None:
        team_CPs = sorted([(team, self.calculate_combat_power(field, team) for team in teams)],
                      key=lambda x:x[1], reverse=True)
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
        pass


class Field:
    def __init__(self, id, weapon_type, water, spice) -> None:
        self.id = id
        self.weapons = weapon_type
        self.water = water
        self.spice = spice
        self.owner = None
        self.harvester = False
        self.neighbours = []

    def new_owner(self, Team) -> None:
        pass

    def is_neighbour(self, field) -> bool:
        return field in self.neighbours
    
    def is_contested(self, moves: dict) -> bool:
        count = 0
        for team in moves:
            if self.id in team["wants"]:
                count += 1
        return count > 1

class Team:
    def __init__(self, num) -> None:
        self.num = num
        self.fields: list[Field] = None
        self.weapons = [0,0,0,0]
        self.spice = 10
        self.water = 7
        self.harvesters_built = 0

    def harvester_cost(self) -> int:
        return 10 * 2**self.harvesters_built

    def comulate_water(self) -> None:
        self.water = sum([f.water for f in self.fields])

    def comulate_spice(self) -> None:
        self.spice = sum([f.spice for f in self.fields])

    def purchase(weapons: list[int], harvester: list[str]) -> None:
        pass

    def add_field(self, field) -> None:
        self.fields.append(field)

    def remove_field(self, field) -> None:
        self.fields.remove(field)

    def lose_weapons(won: bool) -> None:
        pass

    def print_stats(self) -> None:
        pass