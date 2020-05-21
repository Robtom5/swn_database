#! /usr/bin/env python3
import cmd
from swn_database import SQLDatabaseLink
from swn_database.converters import CharacterConverter, PlanetConverter, OpinionConverter
from character_editor import CharacterEditor
from swn_database.factories import CharacterFactory, OpinionFactory


class CharacterManager(cmd.Cmd):
    intro = "Welcome to the CharacterManager"
    prompt = '> '

    def __init__(self, sql_link, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.link = sql_link
        self.char_factory = CharacterFactory
        self.op_factory = OpinionFactory
        self.plan_converter = PlanetConverter(sql_link)
        self.op_converter = OpinionConverter(link=sql_link,
                                             opinion_factory=self.op_factory)
        self.char_converter = CharacterConverter(sql_link, self.char_factory)
        self.editor = CharacterEditor(
            sql_link=sql_link,
            char_converter=self.char_converter,
            plan_converter=self.plan_converter,
            op_converter=self.op_converter)
        self.link.connect()

    _CREATE_OPTIONS = ["npc", "pc"]

    def do_create(self, inp):
        '''
        USAGE: create npc/pc name surname
        '''
        args = inp.split(' ')

        name = args[1]
        surname = args[2]
        if args[0] == "npc":
            # Create an npc in the database then pass it's object to the editor prompt
            new_char = self.char_converter.create_character(
                name, surname, False)
            intro = f"Now editing: {name} {surname}"
            self.editor.cmdloop(character=new_char,
                                intro=intro)
            # then update the database with new char
        elif args[0] == "pc":
            new_char = self.char_converter.create_character(
                name, surname, True)
            self.editor.cmdloop(character=new_char,
                                intro=f"Now editing: {name} {surname}")
        else:
            print("ERROR: Please specify either 'npc' or 'pc'")

    def complete_create(self, text, line, begidx, endidx):
        if begidx <= 8:
            return [i for i in self._CREATE_OPTIONS
                    if i.startswith(text.strip())]
        else:
            return []

    def do_edit(self, inp):
        '''usage: edit name surname'''
        args = inp.split(' ')
        if len(args) < 2:
            print("Requires name and surname")
        else:
            character = self.char_converter.load_by_name(
                name=args[0],
                surname=args[1])
            if character:
                self.editor.cmdloop(character=character,
                                    intro=f"Now editing: {args[0]} {args[1]}")
            else:
                print("ERROR: Unable to load character")

    def complete_edit(self, text, line, begidx, endidx):
        available_characters = self.char_converter.available_names()

        if len(line.split(' ')) <= 2:
            return [i[0] for i in available_characters
                    if self.matches(i[0], text)]
        else:
            matching_surnames = [s for a, s in available_characters
                                 if a.startswith(line.split(' ')[1])]

            return [i for i in matching_surnames if self.matches(i, text)]

    def do_quit(self, inp):
        '''Exit without saving'''
        return True

    def do_info(self, inp):
        args = inp.split(' ')
        if len(args) < 2:
            print("Requires name and surname")
        else:
            character = self.char_converter.load_by_name(
                name=args[0],
                surname=args[1])
            if character:
                self.editor.info(character)
            else:
                print("ERROR: Unable to load character")

    complete_info = complete_edit

    def do_names(self, inp):
        [print(f"{n} {s}") for n, s in self.char_converter.available_names()]

    def do_query(self, arg):
        ''' Executes the provided SQL query on the database. '''
        print(self.link.execute_read_query(arg))

    def do_info_all(self, inp):
        '''Print all, dont use'''
        def print_entry(n, s):
            self.do_info(f"{n} {s}")
            print("")
        [print_entry(n, s) for n, s in self.char_converter.available_names()]

    do_EOF = do_quit

    def matches(self, first_string, second_string):
        return first_string.lower().startswith(second_string.lower().strip())


if __name__ == "__main__":
    link = SQLDatabaseLink("./system.db")
    try:
        manager_prompt = CharacterManager(link)
        manager_prompt.cmdloop()
    finally:
        link.close()
