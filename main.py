import game

from players import human, stockfish

game_instance = game.Game(
    name="STEM Chess Robot", 
    players=(
        stockfish.Stockfish(think_time=0.5),
        stockfish.Stockfish(think_time=0.5)
    )
)
game_instance.start()