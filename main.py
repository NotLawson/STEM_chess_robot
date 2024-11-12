import robot
import chess
import chess.engine

fishy = chess.engine.SimpleEngine.popen_uci("stockfish-10-win\Windows\stockfish_10_x64.exe")

print("Welcome to the Chess Robot")
port = input("Enter your COM port (e.g. COM3): ")
if port == "":
    port = "COM3"

arm = robot.Arm(port)
arm.home()

device = 1

board = chess.Board()

print("Game beginning...")
# Game
while True:
    # white turn (player)
    if board.turn == chess.WHITE and board.is_checkmate() == False and board.is_stalemate() == False:
        while True:
            move = input("Enter move (fromSquare:toSquare): ")
            move = move.split(":")
            try:
                from_square = move[0]
                to_square = move[1]
                move = chess.Move.from_uci(from_square+to_square)
                legal = chess.LegalMoveGenerator(board)
                if move in legal:
                    break
                else:
                    print("illegal move, try again!")
            except:
                print("Invalid input, must be like 'a1:a3'")
        board.push(move)
        if board.is_check():
            print("Check!")

    # black turn (robot)
    elif board.turn == chess.BLACK and board.is_checkmate() == False and board.is_stalemate() == False:
        print("Black is thinking...")
        result = fishy.play(board, limit=chess.engine.Limit(2.0))
        move = result.move
        if move == None: break
        cap = board.is_capture(move)
        board.push(move)
        
        move = move.uci()
        from_square = move[0]+move[1]
        to_square = move[2]+move[3]
        print("Black plays", move)
        if cap:
            arm.murder(to_square)
        arm.move_square(from_square, to_square)
        if board.is_check():
            print("Check!")
    else:
        break

out = board.outcome()

if out.termination == 1:
    win = out.winner
    print("Winner is", str(win))
else:
    print("Draw!")

