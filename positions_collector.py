from polyglot_writer import Polyglot_Position


class PolyglotPositionsCollector:
    def __init__(self, polyglot_positions: list[Polyglot_Position] = None):
        self.polyglot_positions = polyglot_positions

    @property
    def polyglot_positions(self):
        return self._polyglot_positions

    @polyglot_positions.setter
    def polyglot_positions(self, value: list[Polyglot_Position]):
        if value and isinstance(value, list):
            cleaned_list = [item for item in value if isinstance(item, Polyglot_Position)]
            if len(cleaned_list) > 0:
                self._polyglot_positions = value
        self._polyglot_positions = []

    def _increase_position_weight(self, position_index: int, step=1):
        self._polyglot_positions[position_index].weight += step

    def _get_position_index_if_in_the_list(self, position: Polyglot_Position):
        """
        This method checks if the hash of a polyglot position and the move from it match with already saved one.
        Note that Polyglot positions have weight and learn attributes.
        The intention is this method to identify matching chess situations and then another method to alternate their weights.
        """

        for i in range(len(self._polyglot_positions)):
            observed_position = self._polyglot_positions[i]
            if observed_position.polyglot_move == position.polyglot_move and observed_position.zobrist_hash == position.zobrist_hash:
                return i
        return None

    def add_position(self, position: Polyglot_Position):
        if isinstance(position, Polyglot_Position):
            existing_position_index = self._get_position_index_if_in_the_list(position)
            if existing_position_index is not None:
                self._increase_position_weight(existing_position_index)
            else:
                self._polyglot_positions.append(position)