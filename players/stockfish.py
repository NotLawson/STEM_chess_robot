from __main__ import game
import chess
import chess.engine
import os

folder = os.path.dirname(os.path.abspath(__file__))

class Stockfish(game.Player):
    def __init__(self, name: str = "Stockfish", engine_path: str = folder + "\stockfish-10-win\Windows\stockfish_10_x64.exe", think_time: float = 2.0):
        super().__init__(name)
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.think_time = think_time

    def move(self, board: chess.Board) -> chess.Move:
        result = self.engine.play(board, limit=chess.engine.Limit(self.think_time))
        return result.move
 