import uarm, time
class Arm:
    def __init__(self, port):
        self.swift = uarm.SwiftAPI(port=port)
        self.home()
    def home(self):
        self.swift.reset(wait=True, speed=10000000)
    def move(self, x, y, z, speed=1000000):
        self.swift.set_position(x=x, speed=speed)
        self.swift.set_position(y=y)
        self.swift.set_position(z=z)
        self.swift.flush_cmd(wait_stop=True)
    def grab(self):
        self.swift.set_gripper(True, wait=True)
    def release(self):
        self.swift.set_gripper(False, wait=True)
    def move_square(self, from_sq, to_sq):
        from_sq = get_coords(from_sq)
        to_sq = get_coords(to_sq)
        self.move(from_sq[0], from_sq[1], 9)

        self.swift.set_pump(True)
        time.sleep(1)

        self.move(from_sq[0], from_sq[1], 170)

        self.swift.set_servo_attach(wait=True, timeout=None)
        self.swift.set_position(x=200, y=0, z=150, speed=10000000, wait=True, timeout=None)
        self.swift.set_wrist(90, wait=True, timeout=None)
        time.sleep(1)

        self.move(to_sq[0], to_sq[1], 170)
        self.move(to_sq[0], to_sq[1], 9)

        self.swift.set_pump(False)

        time.sleep(0.5)

        self.move(to_sq[0], to_sq[1], 15)
        time.sleep(0.2)
        self.move(to_sq[0], to_sq[1], 170)

        self.home()

    def murder(self, square):
        from_sq = get_coords(square)
        self.move(from_sq[0], from_sq[1], 9)

        self.swift.set_pump(True)
        time.sleep(1)

        self.move(from_sq[0], from_sq[1], 170)

        self.swift.set_servo_attach(wait=True, timeout=None)
        self.swift.set_position(x=200, y=0, z=150, speed=10000000, wait=True, timeout=None)
        self.swift.set_wrist(90, wait=True, timeout=None)
        time.sleep(1)

        self.move(100, -200, 100)

        self.swift.set_pump(False)

        time.sleep(0.5)


        self.home()

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
