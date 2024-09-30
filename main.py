import robot

robot = robot.Arm("COM3")

robot.move(100, 100, 1000)
input()
robot.move(200, 200, 200)
input()
robot.move(300, 150, 80)
input()
robot.grab()
input()
robot.home()
input()
robot.release()
input()