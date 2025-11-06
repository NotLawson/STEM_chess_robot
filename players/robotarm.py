import chess
import chess.engine
import uarm, os

folder = os.path.dirname(os.path.abspath(__file__))

# Settings
ARM_PORT: str = "COM9"  # default COM port for the robot arm
ARM_HOVER_HEIGHT: int = 50
ARM_GRAB_HEIGHT: int = 8

class Arm:
    def __init__(self, port):
        self.swift = uarm.SwiftAPI(port=port)
        self.home()

    def home(self):
        self.swift.reset(wait=True, speed=10000000)

    def move(self, x=False, y=False, z=False, speed=1000000):
        if x: self.swift.set_position(x=x, speed=speed)
        if y: self.swift.set_position(y=y)
        if z: self.swift.set_position(z=z)
        self.swift.flush_cmd(wait_stop=True)

    def grab(self):
        self.swift.set_pump(True)
        self.swift.flush_cmd(wait_stop=True)
    def release(self):
        self.swift.set_pump(False)
        self.swift.flush_cmd(wait_stop=True)

if True:
    from __main__ import game
    class RobotArm(game.Player):
        def __init__(self, name: str = "RobotArm", engine_path: str = folder + "\stockfish-10-win\Windows\stockfish_10_x64.exe", think_time: float = 2.0, arm: Arm | None = None):
            super().__init__(name)
            self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
            self.think_time = think_time
            if arm == None:
                self.arm = Arm(ARM_PORT)
            else:
                self.arm = arm

        def move(self, board: chess.Board) -> chess.Move:
            result = self.engine.play(board, limit=chess.engine.Limit(self.think_time))
            
            # Execute move with robot arm
            move = result.move.uci()
            from_square = move[:2]
            to_square = move[2:][:2] # ignore the possibility of promotion: the arm doesn't do anything special for that

            self.arm.home()

            if board.is_capture(result.move):
                # if it's a capture, first remove the captured piece
                captured_square = to_square
                captured_coords = get_coords(captured_square)
                self.arm.move(x=captured_coords[0], y=captured_coords[1], z=ARM_HOVER_HEIGHT)
                self.arm.move(z=ARM_GRAB_HEIGHT)
                self.arm.grab()
                self.arm.move(z=ARM_HOVER_HEIGHT)
                # move to "captured pieces" area
                self.arm.move(x=200, y=-215, z=ARM_HOVER_HEIGHT)
                self.arm.move(z=ARM_GRAB_HEIGHT)
                self.arm.release()
                self.arm.move(z=ARM_HOVER_HEIGHT)
            
            if board.is_castling(result.move):
                # handle castling: move the rook as well
                if to_square == "g1":  # white kingside
                    rook_from = "h1"
                    rook_to = "f1"
                elif to_square == "c1":  # white queenside
                    rook_from = "a1"
                    rook_to = "d1"
                elif to_square == "g8":  # black kingside
                    rook_from = "h8"
                    rook_to = "f8"
                elif to_square == "c8":  # black queenside
                    rook_from = "a8"
                    rook_to = "d8"

                # move the king
                from_coords = get_coords(from_square)
                self.arm.move(x=from_coords[0], y=from_coords[1], z=ARM_HOVER_HEIGHT)
                self.arm.move(z=ARM_GRAB_HEIGHT)
                self.arm.grab()
                self.arm.move(z=ARM_HOVER_HEIGHT)

                to_coords = get_coords(to_square)
                self.arm.move(x=to_coords[0], y=to_coords[1], z=ARM_HOVER_HEIGHT)
                self.arm.move(z=ARM_GRAB_HEIGHT)
                self.arm.release()
                self.arm.move(z=ARM_HOVER_HEIGHT)

                # move the rook
                from_coords = get_coords(rook_from)
                self.arm.move(x=from_coords[0], y=from_coords[1], z=ARM_HOVER_HEIGHT)
                self.arm.move(z=ARM_GRAB_HEIGHT)
                self.arm.grab()
                self.arm.move(z=ARM_HOVER_HEIGHT)

                to_coords = get_coords(rook_to)
                self.arm.move(x=to_coords[0], y=to_coords[1], z=ARM_HOVER_HEIGHT)
                self.arm.move(z=ARM_GRAB_HEIGHT)
                self.arm.release()
                self.arm.move(z=ARM_HOVER_HEIGHT)

                self.arm.home()
                return result.move

            # grab the piece
            from_coords = get_coords(from_square)
            self.arm.move(x=from_coords[0], y=from_coords[1], z=ARM_HOVER_HEIGHT)
            self.arm.move(z=ARM_GRAB_HEIGHT)
            self.arm.grab()
            self.arm.move(z=ARM_HOVER_HEIGHT)

            # move to destination
            to_coords = get_coords(to_square)
            self.arm.move(x=to_coords[0], y=to_coords[1], z=ARM_HOVER_HEIGHT)
            self.arm.move(z=ARM_GRAB_HEIGHT)
            self.arm.release()
            self.arm.move(z=ARM_HOVER_HEIGHT)
            
            self.arm.home()
            return result.move
    
def get_coords(square):
    board = [
        # A  B  C  D  E  F  G  H
        [(335,-105),(335,-75),(335,-45),(335,-15),(335,15),(335,45),(335,75),(335,105)], # 1
        [(305,-105),(305,-75),(305,-45),(305,-15),(305,15),(305,45),(305,75),(305,105)], # 2
        [(275,-105),(275,-75),(275,-45),(275,-15),(275,15),(275,45),(275,75),(275,105)], # 3
        [(245,-105),(245,-75),(245,-45),(245,-15),(245,15),(245,45),(245,75),(245,105)], # 4
        [(215,-105),(215,-75),(215,-45),(215,-15),(215,15),(215,47),(215,75),(215,105)], # 5
        [(185,-105),(185,-75),(185,-45),(185,-15),(185,15),(185,47),(185,75),(185,105)], # 6
        [(155,-105),(155,-75),(155,-45),(155,-15),(155,15),(155,47),(155,75),(155,105)], # 7
        [(125,-105),(125,-75),(125,-45),(125,-15),(125,15),(125,47),(125,75),(125,105)]  # 8
    ]

    letter = square[0]
    if letter=="a":letter=0
    elif letter=="b":letter=1
    elif letter=="c":letter=2
    elif letter=="d":letter=3
    elif letter=="e":letter=4
    elif letter=="f":letter=5
    elif letter=="g":letter=6
    elif letter=="h":letter=7
    number = int(square[1])-1
    return board[number][letter]
