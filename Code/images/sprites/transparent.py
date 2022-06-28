import cv2
import numpy as np
import os

dir_path = "/Users/ongyichong/PythonGames /PythonGame/images/sprites/Rat_west/"
dirs = os.listdir("/Users/ongyichong/PythonGames /PythonGame/images/sprites/Rat_west")
for file in dirs:

    print(file)
    if file.endswith('.png'):



        img = cv2.imread(dir_path + file)

        (h, w) = img.shape[:2]

        for height in range(h):
            for width in range(w):
                if img[height,width] == np.all(np.array(0, 0, 0)):
                    img[height, width] = (255, 255, 255)

        #mask = np.zeros(img.shape, dtype = "uint8")



        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #(T, threshInv) = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

        #new_img = cv2.bitwise_xor(img, mask)


        cv2.imshow("img", img)
        cv2.waitKey(0)
