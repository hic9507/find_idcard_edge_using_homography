############################################### 방법 1 #######################################################
############################################### 방법 1 #######################################################
############################################### 방법 1 #######################################################
############################################### 방법 1 #######################################################

import os
import cv2
import numpy as np
import imutils

for i in os.listdir('C:/Users/user/Desktop/bs/'):
    path = 'C:/Users/user/Desktop/bs/' + i

    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    clahe = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(4, 4))
    cll = clahe.apply(image)
    equ = cv2.equalizeHist(cll)
    blur = cv2.GaussianBlur(equ, (15, 15), sigmaX=0)
    canny = cv2.Canny(image, 50, 50)

    # cv2.imshow('2', canny)
    # cv2.imshow('3', blur)
    # cv2.imshow('1', equ)
    # cv2.waitKey()

    ####### erosion, dilate, median blur 등 ######
    # k = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    # erosion = cv2.dilate(equ, k)
    # erosion2 = cv2.dilate(erosion, k)
    # erosion3 = cv2.dilate(erosion2, k)
    # blur = cv2.GaussianBlur(image, (15, 15), sigmaX=0)
    # blur = cv2.medianBlur(image,7)
    # dilate = cv2.dilate(blur, k)
    # dilate1 = cv2.dilate(dilate, k)
    # canny = cv2.Canny(image, 50, 50)


    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    try:
        img1 = image.copy().astype("uint8")
        img2 = image.copy().astype("uint8")
        ret, imthres = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

        contour2, _ = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(img2, contour2, -1, (0, 255, 0), 4)

        for j in contour2:
            for k in j:
                cv2.circle(img2, tuple(k[0]), 1, (255, 0, 0), -1)

        c0 = contour2[0]

        x, y, w, h = cv2.boundingRect(c0)
        img1 = cv2.rectangle(img1, (x, y), (x + w, y + h), 7)

        rect = cv2.minAreaRect(c0)
        box = cv2.boxPoints(rect)
        box = box.astype('int')
        canny = cv2.drawContours(img2, [box], -1, 7)

        cnts = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        findCnt = None
    except:
        continue

    try:
        # 정렬된 contours를 반복문으로 수행하며 4개의 꼭지점을 갖는 도형을 검출
        for c in cnts:
            # print(c)
            peri = cv2.arcLength(c, True)
            # print(peri)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)

            # contours가 크기순으로 정렬되어 있기때문에 제일 첫번째 사각형을 영역으로 판단하고 break
            if len(approx) == 4:
                findCnt = approx
                break

        # 만약 추출한 윤곽이 없을 경우 오류
        if findCnt is None:
            raise Exception(("Could not find outline."))
    except:
        continue

    output = image.copy()
    draw = cv2.drawContours(output, [findCnt], -1, (0, 255, 0), 2)
    draw_contour = cv2.drawContours(draw, [findCnt], -1, (255, 255, 255), 2)

    cv2.imshow('s', draw_contour)
    cv2.waitKey()
    cv2.destroyAllWindows()
    # cv2.imwrite("C:\\Users\\user\\Desktop\\false_contour\\" + i, tmp)