#! /usr/bin/env python3
import cmd
import math
from swn_database.data import Planet, Coordinate, Connection
from swn_database import SQLDatabaseLink
from swn_database.converters import PlanetConverter, ConnectionConverter
from planetary_information import *

class Converters():
    def __init__(self, link):
        self.planet = PlanetConverter(link)
        self.connection = ConnectionConverter(link)

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

    def do_quit(self, inp):
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

    def complete_update(self, text, line, begindx, endindx):
        if begindx < 8:
            planets = [p[0]
                       for p in self.converters.planet.available_planets()]
            return [p for p in planets if p.startswith(text.strip())]
        else:
            return []

    def do_description(self, inp):
        ''' Set the description for the planet'''
        args = inp.split(' ')
        name = args[0]
        description = ' '.join(args[1:])
        self.converters.planet.update(name=name, desc=description)
        self.link.commit()

    def complete_description(self, text, line, begindx, endindx):
        if len(line.split(' ')) <= 2:
            return self.complete_info(text, line, begindx, endindx)
        else:
            return []

    def do_notes(self, inp):
        ''' Set the description for the planet'''
        args = inp.split(' ')
        name = args[0]
        notes = ' '.join(args[1:])
        self.converters.planet.update(name=name, notes=notes)
        self.link.commit()

    complete_notes = complete_description

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
        print(planet.notes.replace('\\n', '\n')
              if planet.notes is not None else "")
        print(divider)
        self.connected(planet)
        print(divider)

    def complete_info(self, text, line, begindx, endindx):
        planets = [p[0] for p in self.converters.planet.available_planets()]
        return [p for p in planets if self.matches(p, text)]

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
                even_column = (coordinate.x % 2 == 0)
                moving_up = (coordinate.y - planet.coordinates.y < 0)
                if moving_up ^ even_column:
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
            confirm = input(
                f'{name} found at hex {planet.coordinates}. Are you sure you wish to delete? Y/N ')
            if (confirm.lower().strip() == 'y'):
                self.link.planet.delete(planet)
        else:
            print(f"No planet found for provided name: {name}")

    complete_delete = complete_info

    def do_list(self, inp):
        '''
        usage: list [planets/conns]
        Prints the available planets, connections
        '''
        if (inp == 'planets'):
            [print(f"{f'{p.coordinates}':<3} - " + p.name)
             for p in self.converters.planet.load_all('name')]
        elif (inp == 'conns'):
            [print(f"{c.start_hex} -> {c.end_hex}")
             for c in self.converters.connection.load_all()]

    def do_EOF(self, inp):
        '''Exit the tool'''
        return self.do_quit(inp)

    def do_query(self, arg):
        ''' Executes the provided SQL query on the database. '''
        print(self.link.execute_read_query(arg))

    def parse(self, arg_list):
        args = dict()
        for pair in arg_list:
            arg, val = pair.split("=")
            args[arg] = val

        return args

    def matches(self, first_string, second_string):
        return first_string.lower().startswith(second_string.lower().strip())


if __name__ == "__main__":
    link = SQLDatabaseLink("./system.db")
    manager_prompt = PlanetManagerPrompt(link)
    manager_prompt.cmdloop()
    link.close()
