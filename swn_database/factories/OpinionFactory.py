#! /usr/bin/env python3
from ..data import Opinion
from .Factory import Factory


class OpinionFactory(Factory):
    @staticmethod
    def create(serialized_data: tuple):
        char_id = serialized_data[0]
        targ_id = serialized_data[1]
        opinion = serialized_data[2]
        return Opinion(character_id=char_id,
                       target_id=targ_id,
                       opinion=opinion)
