import cv2
import numpy as np

i'm# load image
image = cv2.resize(cv2.imread('testing/image1.jpg'), (800, 400))

# load points from file
src = np.load('testing/points.npy', allow_pickle=True).astype('float32')

# warp
dst = np.float32(([0, 0],[400, 0],[0, 400],[400, 400]))
perpspective_matrix = cv2.getPerspectiveTransform(src, dst)
warp = cv2.warpPerspective(image, perpspective_matrix, (400,400))
cv2.imshow("Warped Image", warp)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()


# grid
for i in range(8):
    cv2.line(warp, (0, i*50), (400, i*50), (255, 0, 0), 1)
    cv2.line(warp, (i*50, 0), (i*50, 400), (255, 0, 0), 1)
cv2.imshow("Warped Image with Grid", warp)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()

before = cv2.warpPerspective(cv2.resize(cv2.imread('testing/image1.jpg'), (800, 400)), perpspective_matrix, (400,400))
after = cv2.warpPerspective(cv2.resize(cv2.imread('testing/image2.jpg'), (800, 400)), perpspective_matrix, (400,400))

before = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
after = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

x = 5
before = cv2.GaussianBlur(before, (x,x),0)
after = cv2.GaussianBlur(after, (x,x),0)

thresh = 125
_, before = cv2.threshold(before, thresh, 255, cv2.THRESH_BINARY)
_, after = cv2.threshold(after, thresh, 255, cv2.THRESH_BINARY)

diff = cv2.absdiff(before, after)   
diff = cv2.GaussianBlur(diff, (x,x),0)
_, diff = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)
# grid
disp = diff.copy()
for i in range(8):
    cv2.line(disp, (0, i*50), (400, i*50), (255, 0, 0), 1)
    cv2.line(disp, (i*50, 0), (i*50, 400), (255, 0, 0), 1)
cv2.imshow("Difference Image", disp)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()

# contours

cnts, _ = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

rects = []
for c in cnts:
    area = cv2.contourArea(c)
    if area > 100:     
        print("c")   
        (x, y, w, h) = cv2.boundingRect(c)
        rects.append((x, y, w, h))
        cv2.rectangle(disp, (x, y), (x + w, y + h), (255, 255, 255), 2)

cv2.imshow("Contours", disp)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()

# black square
black_square = np.zeros((400, 400, 3), dtype=np.uint8)
for i in range(8):
    cv2.line(black_square, (0, i*50), (400, i*50), (255, 0, 0), 1)
    cv2.line(black_square, (i*50, 0), (i*50, 400), (255, 0, 0), 1)

for rect in rects: cv2.rectangle(black_square, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)
cv2.imshow("Black Square with Contours", black_square)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()

# highlight square
## rect coords
cols = []
for col in range(8):
    rows = []
    for row in range(8):
        rows.append((col*50, row*50, (col+1)*50, (row+1)*50))
    cols.append(rows)
boxes = np.array(cols)

checkerboard = np.zeros((400, 400, 3), dtype=np.uint8)
x = True
for col in cols:
    for row in col:
        if x:
            cv2.rectangle(checkerboard, (row[0], row[1]), (row[2], row[3]), (255, 255, 255), -1)
            x = not x
        else:
            x = not x
    x = not x

for rect in rects: cv2.rectangle(checkerboard, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 0, 255), 2)

cv2.imshow("Checkerboard", checkerboard)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()


# find square containing contour midpoints
squares = []
for rect in rects:
    mid_point = (rect[0] + rect[2]//2, rect[1] + rect[3]//2)
    for i in range(8):
        for j in range(8):
            if boxes[i][j][0] < mid_point[0] < boxes[i][j][2] and boxes[i][j][1] < mid_point[1] < boxes[i][j][3]:
                print(f"Contour at {rect} is in square ({i}, {j})")
                squares.append([i, j])
                cv2.circle(checkerboard, mid_point, 5, (0, 0, 255), -1)
                cv2.rectangle(checkerboard, (boxes[i][j][0], boxes[i][j][1]), (boxes[i][j][2], boxes[i][j][3]), (0, 255, 0), 2)


cv2.imshow("Checkerboard with Midpoints", checkerboard)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()

# new checkerboard with without contours
finalboard = np.zeros((400, 400, 3), dtype=np.uint8)
x = True
for col in cols:
    for row in col:
        if x:
            cv2.rectangle(finalboard, (row[0], row[1]), (row[2], row[3]), (255, 255, 255), -1)
            x = not x
        else:
            x = not x
    x = not x

for square in squares:
    cv2.rectangle(finalboard, (boxes[square[0]][square[1]][0], boxes[square[0]][square[1]][1]), (boxes[square[0]][square[1]][2], boxes[square[0]][square[1]][3]), (0, 0, 255), -1)

cv2.imshow("Final Board", finalboard)
while True:
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()

# get chess squares from coords
def coords_to_square(col, row):
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    return files[col] + ranks[row]
for square in squares:
    chess_square = coords_to_square(square[1], square[0])
    print(f"Square at coords ({square[0]}, {square[1]}) is {chess_square}")


# find move with chess library
import chess

# if a standard move
# get board
# loop through legal moves
# see if any match the detected move squares
# if found, return that move
