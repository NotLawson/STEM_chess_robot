from __main__ import game
import chess 

class Human(game.Player):
    def __init__(self):
        super().__init__(name="Human")

    def move(self, board):
        while True:
            move = input("Enter move (fromSquare:toSquare): ")
            move = move.split(":")
            try:
                from_square = move[0]
                to_square = move[1]
                move = chess.Move.from_uci(from_square+to_square)
                legal = chess.LegalMoveGenerator(board)
                if move in legal:
                    return move
                else:
                    print("illegal move, try again!")
            except:
                print("Invalid input, must be like 'a1:a3'")