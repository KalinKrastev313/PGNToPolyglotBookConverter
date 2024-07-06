import chess.pgn
from chess.polyglot import zobrist_hash
from polyglot_writer import Polyglot_Position, Polyglot_Move, Polyglot_Writer


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


def game_starts_from_starting_position(game):
    for header in list(game.headers):
        if header.upper() == 'FEN':
            if game.headers[header] != chess.STARTING_FEN:
                return False
    return True


def main(pgn_file_name, result_file_name):
    pgn = open(pgn_file_name)

    position_collector = PolyglotPositionsCollector()
    board = chess.Board()

    while True:
        game = chess.pgn.read_game(pgn)
        if not isinstance(game, chess.pgn.Game) or game is None:
            break

        if not game_starts_from_starting_position(game):
            continue

        board.reset()
        for move in game.mainline_moves():
            p_hash = zobrist_hash(board)
            p_move = Polyglot_Move.from_chess_move(board, move)
            # Below a single occurrence is considered to have weight 1
            p_position = Polyglot_Position(p_hash, p_move, 1, 0)
            position_collector.add_position(p_position)

            try:
                board.push(move)
            except Exception:
                print(game)

    Polyglot_Writer().write(polyglot_positions=position_collector.polyglot_positions,
                            file_name=result_file_name)


if __name__ == '__main__':
    pgn_file_name = 'black.pgn'
    result_file_name = 'black_repertoire.bin'
    main(pgn_file_name, result_file_name)
