# STEM Chess Robot
# Settings
DEBUG: bool = True # set this to True to enable debug messages



# Imports
import chess
import inspect
from datetime import datetime

class Player:
    def __init__(self, name: str):
        self.name = name

    def move(self, board: chess.Board) -> chess.Move:
        return chess.Move.from_uci(input(f"[Player {self.name}] Enter your move: "))

class Outcome:
    def __init__(self, result: chess.Outcome):
        self.result = result
    def __str__(self):
        match self.result.termination:
            case chess.Termination.CHECKMATE:
                if self.result.winner == chess.WHITE:
                    return f"White wins by checkmate"
                else:
                    return f"Black wins by checkmate"
            case chess.Termination.STALEMATE:
                return f"Game ends in stalemate"
            case chess.Termination.INSUFFICIENT_MATERIAL:
                return f"Game ends in a draw due to insufficient material"
            case chess.Termination.SEVENTYFIVE_MOVES:
                return f"Game ends in a draw due to the seventy-five-move rule"
            case chess.Termination.FIVEFOLD_REPETITION:
                return f"Game ends in a draw due to fivefold repetition"
            case _:
                return "Game ended... without a reason? This shouldn't be possible, get out of here you bugger!"
    def __tuple__(self):
        return (self.result.termination, self.result.winner)
    
class Announcer:
    def __init__(self, output: str = "none", silent: bool = False, debug: bool = False):
        self.silent = silent
        if output != "none":
            self.output = True
            self.output_file = output
            self.output_handle = open(output, "a")
            self.output_handle.write(f"Announcer started at {datetime.now()}\n")
        else:
            self.output = False
        self.DEBUG = debug
        

    def find_caller(self, stack: list[inspect.FrameInfo] ):
        for frame in stack:
            match frame.function:
                case "announce" | "important" | "debug":
                    continue
                case "commentate" | "commentate_turn":
                    return "Commentator"
                case _:
                    return frame.function
                
    def find_piece(self, piece: chess.PieceType | str):
        match piece:
            case chess.PAWN | "P" | "p":
                return "Pawn"
            case chess.KNIGHT | "N" | "n":
                return "Knight"
            case chess.BISHOP | "B" | "b":
                return "Bishop"
            case chess.ROOK | "R" | "r":
                return "Rook"
            case chess.QUEEN | "Q" | "q":
                return "Queen"
            case chess.KING | "K" | "k":
                return "King"
            case _:
                return "Unknown"

    def announce(self, message: str, level: int = 0):
        time = datetime.now().strftime("%H:%M:%S")
        caller = self.find_caller(inspect.stack())
        level_name = AnnouncementLevels.levels[level]
        formatted_message = f"[{time}] [{caller}] [{level_name}] {message}"

        if self.output:
            self.output_handle.write(formatted_message + "\n")
        if not self.silent:
            print(f"{AnnouncementLevels.colours[level]}{formatted_message}{AnnouncementLevels.END}")

    def important(self, message: str):
        self.announce(message, AnnouncementLevels.IMPORTANT)
    
    def debug(self, message: str):
        if self.DEBUG: self.announce(message, AnnouncementLevels.DEBUG)

    def commentate_turn(self, player: Player, side: bool):
        player_name = player.name
        side_name = "White" if side == chess.WHITE else "Black"
        self.announce(f"{side_name} ({player_name}) to move", AnnouncementLevels.INFO)

    def commentate(self, board: chess.Board):
        move: chess.Move = board.pop()
        player = "White" if board.turn == chess.WHITE else "Black"
        piece = self.find_piece(board.piece_at(move.from_square).piece_type)

        self.announce(f"{player} plays {piece} from {chess.square_name(move.from_square)} to {chess.square_name(move.to_square)}")

        # if promotion
        if move.promotion != None:
            self.important(f" - promotes to a {self.find_piece(move.promotion)}")
        
        # if capture
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square).piece_type
            self.announce(f" - captures {self.find_piece(captured_piece)}", level=AnnouncementLevels.CAPTURE)
        
        # if check
        board.push(move)
        if board.is_check():
            self.announce(f" - gives check", level=AnnouncementLevels.CHECK)

        # if checkmate
        if board.is_checkmate():
            self.announce(f" - delivers checkmate", level=AnnouncementLevels.MATE)
            return

class AnnouncementLevels:
    INFO = 0
    IMPORTANT = 1
    CAPTURE = 2
    CHECK = 3
    MATE = 4
    DEBUG = 5
    END = "\033[0m"
    # with respect to above values
    # e.g. colours[AnnouncementLevels.INFO] will give the colour for INFO level announcements
    colours = [
        "\033[0m",  # INFO - Default
        "\033[34m",  # IMPORTANT - Blue
        "\033[31m",  # CAPTURE - Red
        "\033[33m",  # CHECK - Yellow
        "\033[35m",  # MATE - Magenta
        "\033[32m",  # DEBUG - Green
    ]
    levels = [
        "INFO",
        "IMPT",
        "CAPT",
        "CHCK",
        "MATE",
        "DEBG",
    ]




# Game object
class Game:
    def __init__(self, name: str, announcer: Announcer = Announcer(), players: tuple[Player, Player] = (Player("White"), Player("Black"))):
        self.board = chess.Board()
        self.announcer = announcer
        self.white, self.black = players
        self.announcer.debug("Game Setup Complete")
    
    def start(self):
        self.Main()

    def Main(self):
        # Main Game loop
        self.announcer.important("Game Beginning...")
        self.announcer.debug("Entering Main Game Loop")
        while True:
            self.move(self.white if self.board.turn == chess.WHITE else self.black)
            if self.board.is_game_over():
                outcome = Outcome(self.board.outcome())
                self.announcer.important(f"Game Over: {outcome}")
                break
        
        self.announcer.important("Game Ended.")
        self.announcer.announce("Final position:")
        print(self.board)
        self.announcer.output_handle.write(self.board+ "\n")
        self.announcer.announce("Final FEN: " + self.board.fen())

    def move(self, player: Player):
        self.announcer.commentate_turn(player, self.board.turn)
        self.announcer.debug(f"Waiting for move from player {player.name}...")
        while True:
            try: 
                move = player.move(self.board)
                self.announcer.debug(f"Player {player.name} played move: {move.uci()}, from {chess.square_name(move.from_square)} to {chess.square_name(move.to_square)} with promotion {move.promotion}, capture {self.board.is_capture(move)}, and piece {self.board.piece_at(move.from_square)}")
                self.board.push(move)
                break
            except Exception as e:
                self.announcer.debug(f"Error occurred: {e}")
                continue
        self.announcer.commentate(self.board)
        #print(self.board)