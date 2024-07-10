from unittest import TestCase

import chess

from polyglot_writer import Polyglot_Position, Polyglot_Move
from chess.polyglot import zobrist_hash
from positions_collector import PolyglotPositionsCollector


class EngineTest(TestCase):
    class PolyglotPositionTest(Polyglot_Position):
        def __eq__(self, other):
            return self.zobrist_hash == other.zobrist_hash and \
                   self.polyglot_move == other.polyglot_move and \
                   self.weight == other.weight and \
                   self.learn == other.learn

    def setUp(self):
        self.init_zobrist_hash = zobrist_hash(chess.Board())
        self.p_move_1 = Polyglot_Move.from_chess_move(chess.Board(), chess.Move.from_uci('e2e4'))
        self.p_position_1 = self.PolyglotPositionTest(self.init_zobrist_hash, self.p_move_1, 1, 0)
        self.p_move_2 = Polyglot_Move.from_chess_move(chess.Board(), chess.Move.from_uci('d2d4'))
        self.p_position_2 = self.PolyglotPositionTest(self.init_zobrist_hash, self.p_move_2, 2, 0)

    def test_polyglot_positions_setter_when_all_positions_are_right_type(self):
        position_list = [self.p_position_1, self.p_position_2]
        self._test_polyglot_positions_setter(passed_positions_list=position_list,
                                             expected_positions_list=position_list)

    def test_polyglot_positions_setter_when_some_positions_are_right_type(self):
        not_a_p_position = 3
        position_list = [self.p_position_1, not_a_p_position]
        self._test_polyglot_positions_setter(passed_positions_list=position_list,
                                             expected_positions_list=[self.p_position_1])

    def test_polyglot_positions_setter_when_no_position_list_passed(self):
        not_a_position_list = {'a': 3}
        self._test_polyglot_positions_setter(passed_positions_list=not_a_position_list,
                                             expected_positions_list=[])

    def _test_polyglot_positions_setter(self, passed_positions_list, expected_positions_list):
        collector = PolyglotPositionsCollector(passed_positions_list)
        self.assertEqual(collector.polyglot_positions, expected_positions_list)

    def test_increase_position_weight(self):
        collector = PolyglotPositionsCollector([self.p_position_1, self.p_position_2])
        collector._increase_position_weight(position_index=1)
        self.assertEqual(collector.polyglot_positions, [self.p_position_1, Polyglot_Position(self.init_zobrist_hash, self.p_move_2, 3, 0)])

    def test_get_position_index_when_position_in_the_list(self):
        self._test_get_position_index_if_in_the_list(p_position=Polyglot_Position(self.init_zobrist_hash, self.p_move_2, 50, 0),
                                                     collector=PolyglotPositionsCollector([self.p_position_1, self.p_position_2]),
                                                     expected_result=1)

    def test_get_position_index_when_position_not_in_the_list(self):
        other_zobrist_hash = zobrist_hash(chess.Board(fen='rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2'))
        self._test_get_position_index_if_in_the_list(p_position=Polyglot_Position(other_zobrist_hash, self.p_move_2, 50, 0),
                                                     collector=PolyglotPositionsCollector([self.p_position_1, self.p_position_2]),
                                                     expected_result=None)
        other_p_move = Polyglot_Move.from_chess_move(chess.Board(), chess.Move.from_uci('c2c4'))
        self._test_get_position_index_if_in_the_list(p_position=Polyglot_Position(self.init_zobrist_hash, other_p_move, 50, 0),
                                                     collector=PolyglotPositionsCollector([self.p_position_1, self.p_position_2]),
                                                     expected_result=None)

    def _test_get_position_index_if_in_the_list(self, p_position, collector, expected_result):
        found_index = collector._get_position_index_if_in_the_list(p_position)
        self.assertEqual(found_index, expected_result)

    def test_add_position_not_in_the_list(self):
        self._test_add_position(position=self.p_position_2,
                                collector=PolyglotPositionsCollector([self.p_position_1]),
                                expected=[self.p_position_1, self.p_position_2])

    def test_add_position_already_in_the_list(self):
        self._test_add_position(position=self.p_position_1,
                                collector=PolyglotPositionsCollector([self.p_position_1]),
                                expected=[Polyglot_Position(self.init_zobrist_hash, self.p_move_1, 2, 0)])

    def test_add_position_of_the_wrong_type(self):
        self._test_add_position(position=3,  # not a Polyglot position
                                collector=PolyglotPositionsCollector([self.p_position_1]),
                                expected=[self.p_position_1])

    def _test_add_position(self, position: Polyglot_Position, collector: PolyglotPositionsCollector, expected: list):
        collector.add_position(position)
        self.assertEqual(collector.polyglot_positions, expected)


