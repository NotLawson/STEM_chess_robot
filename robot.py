import uarm
class Arm:
    def __init__(self, port):
        self.swift = uarm.SwiftAPI(port=port)
        self.home()
    def home(self):
        self.swift.reset(wait=True, speed=10000000)
    def move(self, x, y, z, speed=10000000):
        self.swift.set_position(x=x, speed=speed)
        self.swift.set_position(y=y)
        self.swift.set_position(z=z)
        self.swift.flush_cmd(wait_stop=True)
    def grab(self):
        self.swift.set_gripper(True, wait=True)
    def release(self):
        self.swift.set_gripper(False, wait=True)