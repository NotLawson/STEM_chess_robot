from players.robotarm import Arm, get_coords

arm = Arm("COM3")

# a1
a1 = get_coords("a1")
arm.move(x=a1[0], y=a1[1], z=50)
arm.move(z=8)
input()
arm.move(z=50)

# a8
a8 = get_coords("a8")
arm.move(x=a8[0], y=a8[1], z=50)
arm.move(z=8)
input()
arm.move(z=50)

# h8
h8 = get_coords("h8")
arm.move(x=h8[0], y=h8[1], z=50)
arm.move(z=8)
input()
arm.move(z=50)

# h1
h1 = get_coords("h1")
arm.move(x=h1[0], y=h1[1], z=50)
arm.move(z=8)
input()
arm.move(z=50)


arm.home()
input()