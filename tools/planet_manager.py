#! /usr/bin/env python3
import cmd
import math
from swn_database.data import Planet, Coordinate, Connection
from swn_database import SQLDatabaseLink
from swn_database.converters import PlanetConverter, ConnectionConverter


class Converters():
    def __init__(self, link):
        self.planet = PlanetConverter(link)
        self.connection = ConnectionConverter(link)


ATMOSPHERES = dict(
    [(2, "Corrosive"),
     (3, "Inert, useless for respiration."),
     (4, "Airless/Thin")] +
    [(n, "Breathable") for n in range(5, 10)] +
    [(10, "Thick, requires a pressure mask."),
     (11, "Invasive"),
     (12, "Corrosive & Invasive")])

TEMPERATURES = dict(
    [(2, "Frozen, surface locked in perpetual ice. Atmosphere frozen into solid oxygen and lakes of liquid helium."),
     (3, "Cold, surface dominated by glaciers and tundra.")] +
    [(n, "Variable Cold") for n in range(4, 6)] +
    [(n, "Temperate") for n in range(6, 9)] +
    [(n, "Variable Warm") for n in range(9, 11)] +
    [(11, "Warm, surface predominantly tropical/desert with hotter areas."),
     (12, "Burning, surface inhospitable to human life with vacc suit or equivalent.")])

BIOSPHERES = dict(
    [(2, "Remnant, only the wreckage of a ruined biosphere remains."),
     (3, "Microbial, litte more that microbial life and the occasional slime mold exists.")] +
    [(n, "No native biosphere present.") for n in range(3, 6)] +
    [(n, "Human-Miscible") for n in range(6, 9)] +
    [(n, "Immiscible") for n in range(9, 11)] +
    [(11, "Hybrid"),
     (12, "Engineered")])

POPULATIONS = dict(
    [(2, "Failed Colony"),
     (3, "Outpost, few hundred to few thousand inhabitants")] +
    [(n, "Fewer than a million inhabitants") for n in range(4, 6)] +
    [(n, "Several million inhabitants") for n in range(6, 9)] +
    [(n, "Hundreds of millions of inhabitants") for n in range(9, 11)] +
    [(11, "Billions of inhabitants"),
     (12, "Alien inhabitants")])

TECHLEVEL = dict(
    [(2, "0, Neolithic-level technology"),
     (3, "1, Medieval technology")] +
    [(n, "2, Early Industrial Age technology") for n in range(4, 6)] +
    [(n, "4, Modern postech") for n in range(6, 9)] +
    [(n, "3, Early 21st century equivalent technology") for n in range(9, 11)] +
    [(11, "4+, Postech with specialities"),
     (12, "5, Pretech with surviving infrastructure")])


class PlanetManagerPrompt(cmd.Cmd):
    intro = "Welcome to the planet manager"
    prompt = '> '

    def __init__(self, sql_link, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.link = sql_link
        self.converters = Converters(sql_link)
        self.do_connect_database()
        self.initialize()

    def do_connect_database(self, inp=None):
        '''Connect to the database'''
        self.link.connect()

    def initialize(self):
        print("Initializing tables")
        self.link.execute_query(self.converters.planet.create_table_query)
        self.link.execute_query(self.converters.connection.create_table_query)

    def do_reset(self, inp):
        '''Reset the database back to it's factory settings'''
        confirm = input('Are you sure? This will wipe the database. Y/N: ')
        if (confirm.lower().strip() == 'y'):
            print("Wiping existing tables")
            self.link.execute_query(f"DROP TABLE {self.converters.planet.table_name}", suppress=True)
            self.link.execute_query(f"DROP TABLE {self.converters.connection.table_name}", suppress=True)
            print("Creating new tables")
            self.link.execute_query(self.converters.planet.create_table_query)
            self.link.execute_query(
                self.converters.connection.create_table_query)
        else:
            print("Reset aborted")

    def do_exit(self, inp):
        '''Exit the tool'''
        print("Closing database connection")
        self.link.close()
        print("Quitting planet manager")
        return True

    def do_add(self, inp):
        '''
        usage: add name coordinates [tl=0] [bio=1] [atmos=2] [temp=3] [pop=4]

        Adds a new planet to the database at the specified coordinate and name
        '''
        try:
            args = inp.split(' ')
            name = args[0]
            coords = Coordinate.from_hex(args[1])
            optionals = self.parse(args[2:])
            self.converters.planet.add(name=name, coords=coords, **optionals)
            self.link.commit()
        except Exception as e:
            print("Error padding new planet: ", e)

    def do_update(self, inp):
        '''
        usage: update name [tl=0] [bio=1] [atmos=2] [temp=3] [pop=4]

        updates the named planets fields with new values
        '''
        try:
            args = inp.split(' ')
            name = args[0]
            optionals = self.parse(args[1:])
            self.converters.planet.update(name=name, **optionals)
            self.link.commit()
        except Exception as e:
            print("Error updating planet: ", e)

    def do_description(self, inp):
        ''' Set the description for the planet'''
        args = inp.split(' ')
        name = args[0]
        description = ' '.join(args[1:])
        self.converters.planet.update(name=name, desc=description)
        self.link.commit()

    def do_connect(self, inp):
        '''
        usage: connect hex1 hex2

        creates a bidirectional connection between two listed hexes
        '''
        try:
            args = inp.split(' ')
            hex1 = args[0].upper()
            hex2 = args[1].upper()
            self.converters.connection.add(hex1, hex2)
            self.converters.connection.add(hex2, hex1)
            self.link.commit()
        except Exception as e:
            print("Error connecting hexes: ", e)

    def do_info(self, inp):
        '''Gets information for a planet'''
        planet = self.converters.planet.load_by_name(inp)
        divider = "-" * 10
        print(divider)
        print(f"{planet.coordinates}" + " - " + planet.name)
        print(divider)
        print("Atmosphere: " + ATMOSPHERES.get(planet.atmosphere, "UNKNOWN"))
        print("Temperature: " + TEMPERATURES.get(planet.temperature, "UNKNOWN"))
        print("Biosphere: " + BIOSPHERES.get(planet.biosphere, "UNKNOWN"))
        print("Population: " + POPULATIONS.get(planet.population, "UNKNOWN"))
        print("Tech Level: " + TECHLEVEL.get(planet.tl, "UNKNOWN"))
        print(divider)
        print(planet.description.replace('\\n', '\n')
              if planet.description is not None else "")
        print(divider)
        self.connected(planet)
        print(divider)

    def connected(self, planet):
        if planet:
            linked = link.execute_read_query(f"""
                SELECT name, coordinate FROM planets
                WHERE coordinate IN (
                    SELECT
                        end_hex
                    FROM
                        planetary_connections
                    WHERE
                        start_hex='{planet.coordinates}'
                )
                """)
            if linked:
                print(f"{planet.name} connects to:")
                print(f"{'Name':<16}Distance")
            for name, coord in linked:
                coordinate = Coordinate.from_hex(coord)
                steps_to_column = abs(coordinate.x - planet.coordinates.x)
                steps_to_row = abs(coordinate.y - planet.coordinates.y)
                if (coordinate.y - planet.coordinates.y < 0) ^ (coordinate.x % 2 == 0):
                    saved_steps_from_columns = math.floor(
                        (steps_to_column + 1) / 2)
                else:
                    saved_steps_from_columns = math.floor(steps_to_column / 2)

                steps_to_row = max(0, steps_to_row - saved_steps_from_columns)

                distance = steps_to_column + steps_to_row
                print(f"{name:<16}{distance}")

    def do_delete(self, name):
        '''
        usage: delete planet_name
        deletes the planet from the database
        '''
        if self.link.planet.check_exists(name):
            planet = self.link.planet.load_by_name(name)
            confirm = input(f'{name} found at hex {planet.coordinates}. Are you sure you wish to delete? Y/N ')
            if (confirm.lower().strip() == 'y'):
                self.link.planet.delete(planet)
        else:
            print(f"No planet found for provided name: {name}")

    def do_list(self, inp):
        '''
        usage: list [planets/conns]
        Prints the available planets, connections
        '''
        if (inp == 'planets'):
            [print(f"{f'{p.coordinates}':<3} - " + p.name) for p in self.converters.planet.load_all('name')]
        elif (inp == 'conns'):
            [print(f"{c.start_hex} -> {c.end_hex}") for c in self.converters.connection.load_all()]

    def do_EOF(self, inp):
        '''Exit the tool'''
        return self.do_exit(inp)

    def do_query(self, arg):
        ''' Executes the provided SQL query on the database. '''
        print(self.link.execute_read_query(arg))

    def parse(self, arg_list):
        args = dict()
        for pair in arg_list:
            arg, val = pair.split("=")
            args[arg] = val

        return args


if __name__ == "__main__":
    link = SQLDatabaseLink("./system.db")
    manager_prompt = PlanetManagerPrompt(link)
    manager_prompt.cmdloop()
    link.close()
