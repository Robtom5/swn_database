#! /usr/bin/env python3
import cmd
from swn_database import SQLDatabaseLink
from swn_database.data import Character, Opinion
from swn_database.converters import PlanetConverter


class CharacterEditor(cmd.Cmd):
    prompt = '-> '

    def __init__(self,
                 sql_link,
                 char_converter,
                 plan_converter,
                 op_converter,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.link = sql_link
        self.char_converter = char_converter
        self.plan_converter = plan_converter
        self.op_converter = op_converter

    def cmdloop(self, character: Character, intro=None):
        self.selected_char = character
        super().cmdloop(intro=intro)

    def do_homeworld(self, inp):
        ''' Sets the characters homeworld '''
        planet_name = inp.split(' ')[0]
        planet = self.plan_converter.load_by_name(planet_name)
        if planet:
            self.selected_char.homeworld = planet.ID
            if self.selected_char.current_planet is None:
                self.selected_char.current_planet = planet.ID

    def complete_homeworld(self, text, line, beginindx, endindx):
        planets = [p[0] for p in self.plan_converter.available_planets()]
        return [p for p in planets if self.matches(p, text)]

    def do_location(self, inp):
        '''Set the current planet for the character'''
        planet_name = inp.split(' ')[0]
        planet = self.plan_converter.load_by_name(planet_name)
        if planet:
            self.selected_char.current_planet = planet.ID
        else:
            self.selected_char.current_planet = None

    complete_location = complete_homeworld

    def do_age(self, inp):
        args = inp.split(' ')
        if len(args[0]) < 1:
            print(self.selected_char.age)
        else:
            try:
                age = int(args[0])
                self.selected_char.age = age
            except ValueError:
                print("Unable to parse age")

    def do_description(self, inp):
        desc = inp.strip()
        if desc:
            self.selected_char.description = desc
        else:
            print(self.selected_char.description)

    def do_notes(self, inp):
        notes = inp.strip()
        if notes:
            self.selected_char.notes = notes
        else:
            print(self.selected_char.notes)
        pass

    def do_role(self, inp):
        args = inp.split(' ')
        if len(args[0]) < 1:
            print(self.selected_char.role)
        else:
            role = ' '.join(args[0:])
            self.selected_char.role = role

    def do_trustworthiness(self, inp):
        args = inp.split(' ')
        if len(args[0]) < 1:
            print(self.selected_char.trustworthiness)
        else:
            trustworthiness = int(args[0])
            self.selected_char.trustworthiness = trustworthiness

    def do_EOF(self, inp):
        '''Exit the tool'''
        return self.do_quit(inp)

    def do_quit(self, inp):
        '''Exit without saving'''
        confirm = input('Quit without saving? y/n: ')
        if (confirm.lower().strip() == 'y'):
            return True

    def do_knows(self, inp):
        '''
        usage: knows name surname opinion
        '''
        args = inp.split(' ')
        if len(args) < 3:
            print("Requires name and surname and opinion")
        else:
            name = args[0]
            surname = args[1]
            opinion = args[2]
            same_name = (name == self.selected_char.name and
                         surname == self.selected_char.surname)
            if not same_name:
                target = self.char_converter.load_by_name(name, surname)
                self.op_converter.modify_opinion(
                    self.selected_char,
                    target,
                    opinion)
                if not target.isPC:
                    self.op_converter.modify_opinion(
                        target,
                        self.selected_char,
                        opinion)
            else:
                print("ERROR: Can't have an opinion of self")

    def complete_knows(self, text, line, begidx, endidx):
        available_characters = self.char_converter.available_names()

        if len(line.split(' ')) <= 2:
            return [i[0] for i in available_characters
                    if self.matches(i[0], text)]
        else:
            matching_surnames = [s for a, s in available_characters
                                 if a.startswith(line.split(' ')[1])]

            return [i for i in matching_surnames if self.matches(i, text)]

    def do_save(self, inp):
        '''Saves the currently open character'''
        print("Saving character")
        self.char_converter.update_character(self.selected_char)
        return True

    def do_info(self, inp):
        '''Prints the current characters information'''
        self.info(self.selected_char)

    def info(self, character):
        homeworld = self.plan_converter.get_planet_name(
            character.homeworld)
        current_world = self.plan_converter.get_planet_name(
            character.current_planet)
        divider = "-" * 10
        print(divider)
        print(f"{character.name} {character.surname}{' *' if character.isPC else ''}")
        print(divider)
        print(f"Age: {character.age}")
        print(f"Job: {character.role}")
        print(f"Homeworld: {homeworld}")
        print(f"Current Location: {current_world}")
        print(divider)
        print(f"Trustworthiness: {character.trustworthiness}")
        print(f"Desire: {character.desire}")
        print(divider)
        if character.description:
            print(character.description
                  .replace('\\n', '\n')
                  .replace('\\t', '\t'))
            print(divider)
        if character.notes:
            print(character.notes
                  .replace('\\n', '\n')
                  .replace('\\t', '\t'))
            print(divider)
        [print(f"{n} {s} - {Opinion.parse(o)} ({o})")
         for n, s, o in self.connections(character)]
        print(divider)

    def connections(self, character):
        query = f"""
        SELECT name, surname, opinion
        FROM {self.op_converter.table_name} AS o
            INNER JOIN {self.char_converter.table_name} AS c
            ON c.character_id = o.target_id
            WHERE o.character_id={character.ID}
        """
        return self.link.execute_read_query(query)

    def matches(self, first_string, second_string):
        return first_string.lower().startswith(second_string.lower().strip())


if __name__ == "__main__":
    print("Unable to open editor directly, please start character_manager instead.")
