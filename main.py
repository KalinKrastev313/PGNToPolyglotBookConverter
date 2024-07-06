import chess.pgn
from chess.polyglot import zobrist_hash
from polyglot_writer import Polyglot_Position, Polyglot_Move, Polyglot_Writer
from positions_collector import PolyglotPositionsCollector


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
