# find camera warp points for chessboard
import cv2
import numpy as np

image = cv2.resize(cv2.imread('testing/image1.jpg'), (800, 400))

print("Set warp points and press 'ESC' to continue.")
points = []

def add_point(point):
    if len(points) < 4:
        points.append(point)
    print(f"Point added: {point}")
cv2.imshow("Set Warp Points", image)
cv2.setMouseCallback("Set Warp Points", lambda event, x, y, flags, param: add_point((x, y)) if event == cv2.EVENT_LBUTTONDBLCLK else None)
while True:
    k = cv2.waitKey(1)
    if k == 27:  # Press 'ESC' to exit
        break
    if len(points) == 4:
        break
cv2.destroyAllWindows()

for point in points:
    cv2.circle(image, point, 5, (0, 255, 0), -1)
cv2.imshow("Selected Points", image)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()

points = np.array(points, dtype="float32")
np.savetxt('testing/points.txt', points)
print("Points saved to 'testing/points.txt':")