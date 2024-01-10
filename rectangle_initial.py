import cv2 as cv

import numpy as np

import argparse
import copy




img = cv.imread("./test7.jpg")
img = cv.resize(img, (0,0), fx=0.3,fy=0.3, interpolation=cv.INTER_AREA)
print("img size : ", img.shape)

cv.imshow("blank", img)

rect_coord = []


def mouse_click(event, x, y, flags, param):
    global img
    global rect_coord

    if event == cv.EVENT_FLAG_LBUTTON:
        if len(rect_coord) < 4:
            cv.circle(img, (x, y), 5, (0, 0, 255), 2)
            cv.imshow("blank", img)
            print((x, y))
            rect_coord.append([x, y])
        # else:
        #     print('4 points collected!!')

cv.setMouseCallback("blank", mouse_click)

while True:
    if cv.waitKey(0):
        break




virtual_rect = [[100,100],[130,100],[100,125],[130,125]]


virtual_rect = np.array(virtual_rect).astype(np.float32)
rect_coord = np.array(rect_coord).astype(np.float32)

# print(virtual_rect)
# print(rect_coord)

H, mask = cv.findHomography(virtual_rect, rect_coord, 0)
# print(H)

virtual_card_rect=[]
virtual_card_rect.append([virtual_rect[0][0]-10, virtual_rect[0][1]-20]) #a
virtual_card_rect.append([virtual_rect[1][0]+50, virtual_rect[1][1]-20]) #b
virtual_card_rect.append([virtual_rect[2][0]-10, virtual_rect[2][1]+5]) #c
virtual_card_rect.append([virtual_rect[3][0]+50, virtual_rect[3][1]+5]) #d

# for i in range(4):
#     cv.circle(img, (int(virtual_card_rect[i][0]), int(virtual_card_rect[i][1])), 5, (255, 0, 255), 2)
#     cv.circle(img, (int(virtual_rect[i][0]), int(virtual_rect[i][1])), 5, (255, 0, 0), 2)


cv.line(img, (int(virtual_card_rect[0][0]), int(virtual_card_rect[0][1])), (int(virtual_card_rect[1][0]), int(virtual_card_rect[1][1])), (255, 0, 255), 2 )
cv.line(img, (int(virtual_card_rect[1][0]), int(virtual_card_rect[1][1])), (int(virtual_card_rect[3][0]), int(virtual_card_rect[3][1])), (255, 0, 255), 2 )
cv.line(img, (int(virtual_card_rect[0][0]), int(virtual_card_rect[0][1])), (int(virtual_card_rect[2][0]), int(virtual_card_rect[2][1])), (255, 0, 255), 2 )
cv.line(img, (int(virtual_card_rect[2][0]), int(virtual_card_rect[2][1])), (int(virtual_card_rect[3][0]), int(virtual_card_rect[3][1])), (255, 0, 255), 2 )



cv.line(img, (int(virtual_rect[0][0]), int(virtual_rect[0][1])), (int(virtual_rect[1][0]), int(virtual_rect[1][1])), (255, 0, 0), 2 )
cv.line(img, (int(virtual_rect[1][0]), int(virtual_rect[1][1])), (int(virtual_rect[3][0]), int(virtual_rect[3][1])), (255, 0, 0), 2 )
cv.line(img, (int(virtual_rect[0][0]), int(virtual_rect[0][1])), (int(virtual_rect[2][0]), int(virtual_rect[2][1])), (255, 0, 0), 2 )
cv.line(img, (int(virtual_rect[2][0]), int(virtual_rect[2][1])), (int(virtual_rect[3][0]), int(virtual_rect[3][1])), (255, 0, 0), 2 )


# cv.imshow("blank", img)
#
# cv.waitKey(0)


virtual_card_rect = np.array(virtual_card_rect).astype(np.float32)
# virtual_card_rect = virtual_card_rect.T
virtual_card_rect = np.reshape(virtual_card_rect, (1,) + virtual_card_rect.shape)


virtual_card_rect_warped = cv.perspectiveTransform(virtual_card_rect, H)

virtual_card_rect_warped = np.reshape(virtual_card_rect_warped, virtual_card_rect_warped[0].shape)
print(virtual_card_rect_warped)

# for i in range(4):
#     cv.circle(img, (int(virtual_card_rect_warped[i][0]), int(virtual_card_rect_warped[i][1])), 5, (0, 255, 0), 2)

cv.line(img, (int(virtual_card_rect_warped[0][0]), int(virtual_card_rect_warped[0][1])), (int(virtual_card_rect_warped[1][0]), int(virtual_card_rect_warped[1][1])), (0, 255, 0), 2 )
cv.line(img, (int(virtual_card_rect_warped[1][0]), int(virtual_card_rect_warped[1][1])), (int(virtual_card_rect_warped[3][0]), int(virtual_card_rect_warped[3][1])), (0, 255, 0), 2 )
cv.line(img, (int(virtual_card_rect_warped[0][0]), int(virtual_card_rect_warped[0][1])), (int(virtual_card_rect_warped[2][0]), int(virtual_card_rect_warped[2][1])), (0, 255, 0), 2 )
cv.line(img, (int(virtual_card_rect_warped[2][0]), int(virtual_card_rect_warped[2][1])), (int(virtual_card_rect_warped[3][0]), int(virtual_card_rect_warped[3][1])), (0, 255, 0), 2 )

cv.imshow("blank", img)

cv.waitKey(0)


