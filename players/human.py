from __main__ import game
import chess
import cv2
from time import sleep
class Human(game.Player):
    def __init__(self):
        super().__init__(name="Human")
        self.cv = ComputerVision()

    def move(self, board):
        self.cv.before()
        input("Press Enter when you have made your move...")
        self.cv.after()
        return self.cv.detect(board)

import cv2
import numpy as np
class ComputerVision:
    def __init__(self, camera_index=1):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        src = self.set_warp()
        dst = np.float32(([0, 0],[400, 0],[0, 400],[400, 400]))
        self.perpspective_matrix = cv2.getPerspectiveTransform(src, dst)
        cols = []
        for col in range(8):
            rows = []
            for row in range(8):
                rows.append((col*50, row*50, (col+1)*50, (row+1)*50))
            cols.append(rows)
        self.boxes = np.array(cols)

    def set_warp(self):
        image = cv2.resize(self.cap.read()[1], (800, 400))

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

        return np.array(points, dtype="float32")
    
    def before(self):
        sleep(3)  # give time to set up
        self.before_frame = cv2.warpPerspective(
            cv2.resize(
                self.cap.read()[1],
                (800, 400)
            ),
            self.perpspective_matrix,
            (400,400)
        )
        cv2.imshow("Before Move", self.before_frame)
        while True:
            k = cv2.waitKey(1)
            if k == 27:
                break
        cv2.destroyAllWindows()
        
    def after(self):
        self.after_frame = cv2.warpPerspective(
            cv2.resize(
                self.cap.read()[1],
                (800, 400)
            ),
            self.perpspective_matrix,
            (400,400)
        )
        cv2.imshow("After Move", self.after_frame)
        while True:
            k = cv2.waitKey(1)
            if k == 27:
                break
        cv2.destroyAllWindows()

    def detect(self, current_board):
        # bw, blur, thresh
        before = cv2.cvtColor(self.before_frame, cv2.COLOR_BGR2GRAY)
        after = cv2.cvtColor(self.after_frame, cv2.COLOR_BGR2GRAY)

        x = 5
        before = cv2.GaussianBlur(before, (x,x),0)
        after = cv2.GaussianBlur(after, (x,x),0)

        thresh = 125
        _, before = cv2.threshold(before, thresh, 255, cv2.THRESH_BINARY)
        _, after = cv2.threshold(after, thresh, 255, cv2.THRESH_BINARY)

        # get the difference
        diff = cv2.absdiff(before, after)

        # rerun blur, thresh
        diff = cv2.GaussianBlur(diff, (x,x),0)
        _, diff = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)

        # disp
        disp = diff.copy()

        # contours
        cnts, _ = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rects = []
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 100:
                rects.append(cv2.boundingRect(c))
                cv2.rectangle(disp, (rects[-1][0], rects[-1][1]), (rects[-1][0]+rects[-1][2], rects[-1][1]+rects[-1][3]), (0,255,0), 2)
        
        cv2.imshow("Contours", disp)
        while True:
            k = cv2.waitKey(1)
            if k == 27:
                break
        cv2.destroyAllWindows()
        

        # find coords
        squares = []
        for rect in rects:
            mid_point = (rect[0] + rect[2]//2, rect[1] + rect[3]//2)
            for i in range(8):
                for j in range(8):
                    if self.boxes[i][j][0] < mid_point[0] < self.boxes[i][j][2] and self.boxes[i][j][1] < mid_point[1] < self.boxes[i][j][3]:
                        squares.append((i, j))
        
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

        uci_squares = [files[sq[0]] + ranks[sq[1]] for sq in squares]

        # find the move made
        return self.find_move(uci_squares, current_board)
    
    def find_move(self, uci_squares, current_board: chess.Board):
        if len(uci_squares) != 2:
            print("Could not detect move with squares", uci_squares)
            exit()

        legal = current_board.legal_moves
        for move in legal:
            if move.uci()[:2] in uci_squares and move.uci()[2:] in uci_squares:
                return move
        print("Could not find legal move with squares", uci_squares)
        exit() # fatal cause i can't be bothered putting proper error handling here