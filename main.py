import game

from players import human, stockfish, robotarm

arm = robotarm.Arm(port="COM9")
game_instance = game.Game(
    name="STEM Chess Robot", 
    players=(
        robotarm.RobotArm(arm=arm),
        robotarm.RobotArm(arm=arm),
    ),
    announcer=game.Announcer(debug=True, output="game.txt")
)
game_instance.start()