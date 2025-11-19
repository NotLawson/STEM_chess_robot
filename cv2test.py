import cv2
import numpy as np

camera = cv2.VideoCapture(1)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

something, _ = camera.read()
print("Set warp points and press 'ESC' to continue.")
points = []

def add_point(point):
    if len(points) < 4:
        points.append(point)
    print(f"Point added: {point}")

something, img = camera.read()
cv2.imshow("Set Warp Points", img)
cv2.setMouseCallback("Set Warp Points", lambda event, x, y, flags, param: add_point((x, y)) if event == cv2.EVENT_LBUTTONDBLCLK else None)
while True:
    k = cv2.waitKey(1)
    if k == 27:  # Press 'ESC' to exit
        break
    if len(points) == 4:
        break
cv2.destroyAllWindows()

for point in points:
    cv2.circle(img, point, 5, (0, 255, 0), -1)
cv2.imshow("Selected Points", img)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()

# warped
src = np.float32(points)

ret, img = camera.read()
height, width = img.shape[:2]
dst = np.float32([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])
M = cv2.getPerspectiveTransform(src, dst)
warped = cv2.warpPerspective(img, M, (width, height))
cv2.imshow("Warped Image", warped)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()

input("press enter to take a before photo")
ret, img_before = camera.read()

input("press enter to take an after photo")
ret, img_after = camera.read()

img_before = cv2.warpPerspective(img_before, M, (width, height))
img_after = cv2.warpPerspective(img_after, M, (width, height))
diff = cv2.absdiff(img_before, img_after)
diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
_, diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
matrix,diff = cv2.threshold(diff,10,255,cv2.THRESH_BINARY)
cnts, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
while True:
    cv2.imshow("Difference", diff)
    k = cv2.waitKey(1)
    if k == 27:
        break

cv2.destroyAllWindows()

    
print("camera connected")


cv2.findChessboardCorners()