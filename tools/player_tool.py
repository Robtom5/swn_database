#! /usr/bin/env python3
import argparse
import cmd
import math
from swn_database import SQLDatabaseLink

from swn_database.data import Planet, Coordinate, Connection, Character
from swn_database.converters import CharacterConverter, PlanetConverter, OpinionConverter

from swn_database.factories import CharacterFactory, OpinionFactory
import planetary_information as PI


class Phonebook(cmd.Cmd):
    prompt = "<phonebook> "

    def __init__(self,
                 sql_link: SQLDatabaseLink,
                 char_converter,
                 plan_converter,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.character = None
        self.sql_link = sql_link
        self.char_converter = char_converter
        self.plan_converter = plan_converter

    def do_contents(self, inp):
        '''prints the list of npcs who you have had direct contact with'''
        query = f"""
        SELECT name, surname
        FROM opinions AS o
            INNER JOIN characters AS c
            ON c.character_id = o.target_id
            WHERE o.character_id={self.character.ID}
        ORDER BY name, surname ASC
        """
        [print(f"{n} {s}") for n, s in self.sql_link.execute_read_query(query)]

    def do_lookup(self, inp):
        '''lookup an individual by name'''
        args = inp.split(' ')
        if len(args) < 2:
            print("Require name and surname")
        else:
            character = self.char_converter.load_by_name(name=args[0],
                                                         surname=args[1])
            if character:
                homeworld = self.plan_converter.get_planet_name(
                    character.homeworld)
                current_world = self.plan_converter.get_planet_name(
                    character.current_planet)
                if self.sql_link.execute_read_query(f"""SELECT opinion
                    FROM opinions
                    WHERE character_id={self.character.ID}
                    AND target_id={character.ID}"""):
                    known_to_player = True
                else:
                    known_to_player = False
                divider = "-" * 10
                print(divider)
                print(
                    f"{character.name} {character.surname}")
                print(divider)
                print(f"Age: {character.age}")
                print(f"Job: {character.role}")
                print(f"Homeworld: {homeworld}")
                if known_to_player:
                    print(f"Current Location: {current_world}")
                    if character.description:
                        print(divider)
                        print(character.description
                              .replace('\\n', '\n')
                              .replace('\\t', '\t'))
                print(divider)
            else:
                print(f"Could not find: {inp}")

    def complete_lookup(self, text, line, begidx, endidx):
        available_characters = self.char_converter.available_names()

        if len(line.split(' ')) <= 2:
            return [i[0] for i in available_characters
                    if self.matches(i[0], text)]
        else:
            matching_surnames = [s for a, s in available_characters
                                 if a.startswith(line.split(' ')[1])]

            return [i for i in matching_surnames if self.matches(i, text)]

    def do_quit(self, inp):
        '''Exit current menu option'''
        return True

    do_EOF = do_quit

    def matches(self, first_string, second_string):
        return first_string.lower().startswith(second_string.lower().strip())


class PlanetLog(cmd.Cmd):
    prompt = "<planets> "

    def __init__(self, sql_link, planet_converter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_link = sql_link
        self.planet_converter = planet_converter

    def do_info(self, inp):
        '''Gets information for a planet'''
        planet = self.planet_converter.load_by_name(inp)
        if planet:
            divider = "-" * 10
            print(divider)
            print(f"{planet.coordinates}" + " - " + planet.name)
            print(divider)
            print("Atmosphere: " + PI.ATMOSPHERES.get(planet.atmosphere, "UNKNOWN"))
            print("Temperature: " + PI.TEMPERATURES.get(planet.temperature, "UNKNOWN"))
            print("Biosphere: " + PI.BIOSPHERES.get(planet.biosphere, "UNKNOWN"))
            print("Population: " + PI.POPULATIONS.get(planet.population, "UNKNOWN"))
            print("Tech Level: " + PI.TECHLEVEL.get(planet.tl, "UNKNOWN"))
            print(divider)
            print(planet.description.replace('\\n', '\n')
                  if planet.description is not None else "")
            print(divider)
            self.connected(planet)
            print(divider)
        else:
            print(f"Could not find: {inp}")

    def complete_info(self, text, line, begindx, endindx):
        planets = [p[0] for p in self.planet_converter.available_planets()]
        return [p for p in planets if self.matches(p, text)]

    def do_quit(self, inp):
        '''Exit current menu option'''
        return True

    do_EOF = do_quit

    def matches(self, first_string, second_string):
        return first_string.lower().startswith(second_string.lower().strip())

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


class PlayerTools(cmd.Cmd):
    prompt = "<menu> "

    def __init__(self, sql_link, player_character_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_link = sql_link

        self.char_factory = CharacterFactory
        self.char_converter = CharacterConverter(sql_link, self.char_factory)
        self.character_id = player_character_id
        self.character = None

        self.planet_converter = PlanetConverter(sql_link)
        self.planet_log = PlanetLog(self.sql_link, self.planet_converter)
        self.phonebook = Phonebook(
            self.sql_link, self.char_converter, self.planet_converter)

    def connect(self):
        self.sql_link.connect()
        character = self.char_converter.load_by_id(self.character_id)

        if character:
            if not character.isPC:
                raise Exception("Attempting to log in as non-player character." +
                                f" ID: {self.character_id}")
            self.character = character
            self.phonebook.character = character
        else:
            raise Exception("Unable to load character from database")

    def cmdloop(self):
        if self.character:
            super().cmdloop(
                intro=f"Welcome {self.character.name} {self.character.surname}")
        else:
            raise Exception(
                "Unable to start commandloop without character loaded")

    def do_planets(self, inp):
        self.planet_log.cmdloop()

    def do_phonebook(self, inp):
        self.phonebook.cmdloop()

    def do_quit(self, inp):
        '''Exit'''
        return True

    do_EOF = do_quit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Tool for players to query database for information')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--alex', dest='player',
                       action="store_const", const=12, help='login as Alex')
    group.add_argument('-i', '--ivan', dest='player',
                       action="store_const", const=13, help='login as Ivan')
    group.add_argument('-n', '--nate', dest='player',
                       action="store_const", const=10, help='login as Nate')
    group.add_argument('-b', '--becky', dest='player',
                       action="store_const", const=11, help='login as Becky')

    args = parser.parse_args()

    link = SQLDatabaseLink("./system.db")
    try:
        tool_prompt = PlayerTools(link, args.player)
        tool_prompt.connect()
        tool_prompt.cmdloop()
    finally:
        link.close()
