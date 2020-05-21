#! /usr/bin/env python3

class Opinion():
    MIN_OPINION = 0
    MAX_OPINION = 100

    def __init__(
            self,
            character_id: int,
            target_id: int,
            opinion: int):
        self._character_id = character_id
        self._target_id = target_id
        self._opinion = opinion

    @property
    def character_id(self):
        return self._character_id

    @property
    def target_id(self):
        return self._target_id

    @property
    def opinion(self):
        return self._opinion

    def update_opinion(self, value, isAbsolute=True):
        if isAbsolute:
            self._opinion = value
        else:
            self._opinion += value

        # Ensure that the opinion is within bounds
        self._opinion = sorted(self.MIN_OPINION,
                               self.opinion,
                               self.MAX_OPINION)[1]

    @staticmethod
    def parse(opinion):
        opinion_range = Opinion.MAX_OPINION - Opinion.MIN_OPINION

        negative_threshold = Opinion.MIN_OPINION + 0.2*opinion_range

        neutral_threshold = Opinion.MIN_OPINION + 0.4*opinion_range
        positive_threshold = Opinion.MIN_OPINION + 0.6*opinion_range
        friendly_threshold = Opinion.MIN_OPINION + 0.8*opinion_range
        if opinion <= negative_threshold:
            return "Hostile"
        elif opinion <= neutral_threshold:
            return "Unfriendly"
        elif opinion <= positive_threshold:
            return "Neutral"
        elif opinion <= friendly_threshold:
            return "Friendly"
        else:
            return "Allies"
