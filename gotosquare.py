import robot, time, pickle
from robot import get_coords

robot = robot.Arm("COM3")

if __name__ == "__main__":

    while True:
        
        current = (input("Where from? (a1) "))
        coords = (input("Where to? (a1) "))

        robot.move_square(current, coords)

