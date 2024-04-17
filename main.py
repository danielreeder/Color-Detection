import argparse
import numpy as np
import pandas as pd
import cv2

#Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Reading the image with opencv
img = cv2.imread(img_path)

#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

#Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
df = pd.read_csv('colors.csv', names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color
def get_color_name(r, g, b):
    minimum = 10_000
    for i in np.arange(len(df)):
        d = np.abs(r - int(df.loc[i, "R"])) + np.abs(g - int(df.loc[i, "G"])) + np.abs(b - int(df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            color_name = df.loc[i, "color_name"]
    return color_name

#function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        global b,g,r,xpos,ypos,clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while (1):
    cv2.imshow("image",img)
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        text = get_color_name(r, g, b) + f" r={r}, g={g}, b={b}"


        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        if (r+g+b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

            clicked = False

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()