############################################### 방법 3 #######################################################
############################################### 방법 3 #######################################################
############################################### 방법 3 #######################################################
############################################### 방법 3 #######################################################

import os
import math
import cv2
import numpy as np
import argparse

for i in os.listdir('C:/Users/rlaqk/Desktop/detect/image/test/'):
    path = 'C:/Users/rlaqk/Desktop/detect/image/test/' + i
    print(path)

    image = cv2.imread(path)
    image_to_show = np.copy(image)
    image_to_show0 = np.copy(image)
    image_to_show1 = np.copy(image)

    list = []
    lists = np.zeros((4, 2), dtype=np.float32)
    count = 0

    mouse_pressed = False
    def mouse_callback(event, x, y, flags, param):
        global image_to_show, mouse_pressed, count, lists, image_to_show0, image_to_show1

        if event == cv2.EVENT_LBUTTONDOWN:
            mouse_pressed = True
            cv2.circle(image_to_show, center=(x,y), radius=3, color=(0, 0, 255), thickness=-1)
            list.append([x, y])
            count += 1
            if count == 4:
                ##### 마우스 클릭 좌표 생성
                x0, y0 = list[0][0], list[0][1]
                x1, y1 = list[1][0], list[1][1]
                x2, y2 = list[2][0], list[2][1]
                x3, y3 = list[3][0], list[3][1]

                ##### 마우스로 찍은 좌표로 생성된 사각형 그리기          (실제로는 line)
                line1 = cv2.line(image_to_show, pt1=(x0, y0), pt2=(x1, y1), color=(0, 255, 0), thickness=3) # 상
                line2 = cv2.line(image_to_show, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=3) # 우
                line3 = cv2.line(image_to_show, pt1=(x2, y2), pt2=(x3, y3), color=(0, 255, 0), thickness=3) # 하
                line4 = cv2.line(image_to_show, pt1=(x0, y0), pt2=(x3, y3), color=(0, 255, 0), thickness=3) # 좌

                ##### 마우스로 찍은 좌표 중 두 개 선택하여 사각형 그리기
                # cv2.rectangle(image_to_show, pt1=(x0, y0), pt2=(x2, y2), color=(0, 255, 0), thickness=1)
                cv2.line(image_to_show, pt1=(x0, y0), pt2=(x1, y0), color=(255, 0, 0), thickness=3) # 상
                cv2.line(image_to_show, pt1=(x1, y0), pt2=(x1, y2), color=(255, 0, 0), thickness=3) # 우
                cv2.line(image_to_show, pt1=(x1, y2), pt2=(x0, y2), color=(255, 0, 0), thickness=3) # 하
                cv2.line(image_to_show, pt1=(x0, y2), pt2=(x0, y0), color=(255, 0, 0), thickness=3) # 좌
                cv2.imshow('rectangle and line', image_to_show)

                print('\n',
                      'x0, y0: ', x0, y0, '\n',
                      'x1, y1: ', x1, y1, '\n',
                      'x2, y2: ', x2, y2, '\n',
                      'x3, y3: ', x3, y3)

                dist_up = abs(math.sqrt(pow(x1-x0, 2) + pow(y1 - y0, 2)))
                dist_right = abs(math.sqrt(pow(x2-x1, 2) + pow(y2 - y1, 2)))
                dist_left = abs(math.sqrt(pow(x3-x0, 2) + pow(y3 - y0, 2)))
                dist_bottom = abs(math.sqrt(pow(x2-x3, 2) + pow(y2 - y3, 2)))

                ##### 임의의 사각형으로부터 신분증의 실제 비율과 같게 한 좌표
                rx0, ry0 = int(x0 - 490), int(y0 - 40)
                rx1, ry1 = int(x1 + 43), int(y1 - 40)
                rx2, ry2 = int(x2 + 43), int(y2 + 160)
                rx3, ry3 = int(x3 - 490), int(y3 + 160)



                ##### 위의 좌표 리스트에 추가
                r_list = ([[rx0, ry0]], [[rx1, ry1]], [[rx2, ry2]], [[rx3, ry3]])

                ##### 실제 신분증 비율로 테두리 만들기
                cv2.line(image_to_show, pt1=(rx0, ry0), pt2=(rx1, ry1), color=(0, 255, 0), thickness=3)
                cv2.line(image_to_show, pt1=(rx1, ry1), pt2=(rx2, ry2), color=(0, 255, 0), thickness=3)
                cv2.line(image_to_show, pt1=(rx2, ry2), pt2=(rx3, ry3), color=(0, 255, 0), thickness=3)
                cv2.line(image_to_show, pt1=(rx0, ry0), pt2=(rx3, ry3), color=(0, 255, 0), thickness=3)

                print('dist_up: ', dist_up)
                print('dist_right: ', dist_right)
                print('dist_left: ', dist_left)
                print('dist_bottom: ', dist_bottom)


                ##### 마우스로 찍은 좌표, 그 좌표로 만든 사각형 좌표, 실제 신분증 비율로 구한 테두리 좌표
                pts1 = np.array(list).astype(np.float32)
                pts2 = ([[x0, y0]], [[x2, y0]], [[x2, y2]], [[x0, y2]])
                pts2 = np.array(pts2).astype(np.float32)
                pts3 = np.array(r_list).astype(np.float32)


                print('pts1: ', '\n', pts1)
                print('pts2: ', '\n', pts2)

                ##### 작은 사각형 간 호모그래피 구하기
                H, mask = cv2.findHomography(srcPoints=pts2, dstPoints=pts1)
                print('H: ', H)

                A = np.linalg.inv(H)
                print('A: ', A)

                rows, cols = image_to_show.shape[1], image_to_show.shape[0]


                M = cv2.getPerspectiveTransform(pts1, pts2)
                print(M.shape)

                dst = cv2.warpPerspective(image_to_show, H, (rows, cols))
                print('dst: ', dst[0][0])

                B = cv2.perspectiveTransform(pts3, H)
                print('B: ', '\n', B)
                print(B)
                print('-' * 100)
                print(B.shape)
                print(B[0][0])
                print(B[0][0][1])
                print(B[1][0])

                ##### 실제 신분증 테두리 좌표
                R_Arr0_x, R_Arr0_y = int(B[0][0][0]), int(B[0][0][1])
                R_Arr1_x, R_Arr1_y = int(B[1][0][0]), int(B[1][0][1])
                R_Arr2_x, R_Arr2_y = int(B[2][0][0]), int(B[2][0][1])
                R_Arr3_x, R_Arr3_y = int(B[3][0][0]), int(B[3][0][1])

                cv2.line(image_to_show, pt1=(R_Arr0_x, R_Arr0_y), pt2=(R_Arr1_x, R_Arr1_y), color=(255, 0, 0), thickness=3)
                cv2.line(image_to_show, pt1=(R_Arr1_x, R_Arr1_y), pt2=(R_Arr2_x, R_Arr2_y), color=(255, 0, 0), thickness=3)
                cv2.line(image_to_show, pt1=(R_Arr2_x, R_Arr2_y), pt2=(R_Arr3_x, R_Arr3_y), color=(255, 0, 0), thickness=3)
                cv2.line(image_to_show, pt1=(R_Arr0_x, R_Arr0_y), pt2=(R_Arr3_x, R_Arr3_y), color=(255, 0, 0), thickness=3)
                cv2.imshow('detect', image_to_show)

                width, height = 1400, 1400


                cv2.rectangle(image_to_show0, pt1=(x0, y0), pt2=(x2, y2), color=(0, 255, 0), thickness=2)
                ##### 실제 신분증 비율로 테두리 만들기
                cv2.line(image_to_show0, pt1=(rx0, ry0), pt2=(rx1, ry1), color=(0, 255, 0), thickness=3)
                cv2.line(image_to_show0, pt1=(rx1, ry1), pt2=(rx2, ry2), color=(0, 255, 0), thickness=3)
                cv2.line(image_to_show0, pt1=(rx2, ry2), pt2=(rx3, ry3), color=(0, 255, 0), thickness=3)
                cv2.line(image_to_show0, pt1=(rx0, ry0), pt2=(rx3, ry3), color=(0, 255, 0), thickness=3)
                cv2.imshow('real', image_to_show0)


                ##### 실제 신분증 비율로 테두리 만들기
                cv2.line(image_to_show1, pt1=(rx0, ry0), pt2=(rx1, ry1), color=(0, 255, 0), thickness=3)
                cv2.line(image_to_show1, pt1=(rx1, ry1), pt2=(rx2, ry2), color=(0, 255, 0), thickness=3)
                cv2.line(image_to_show1, pt1=(rx2, ry2), pt2=(rx3, ry3), color=(0, 255, 0), thickness=3)
                cv2.line(image_to_show1, pt1=(rx0, ry0), pt2=(rx3, ry3), color=(0, 255, 0), thickness=3)

                cv2.line(image_to_show1, pt1=(R_Arr0_x, R_Arr0_y), pt2=(R_Arr1_x, R_Arr1_y), color=(255, 0, 0), thickness=3)
                cv2.line(image_to_show1, pt1=(R_Arr1_x, R_Arr1_y), pt2=(R_Arr2_x, R_Arr2_y), color=(255, 0, 0), thickness=3)
                cv2.line(image_to_show1, pt1=(R_Arr2_x, R_Arr2_y), pt2=(R_Arr3_x, R_Arr3_y), color=(255, 0, 0), thickness=3)
                cv2.line(image_to_show1, pt1=(R_Arr0_x, R_Arr0_y), pt2=(R_Arr3_x, R_Arr3_y), color=(255, 0, 0), thickness=3)
                cv2.imshow('33', image_to_show1)




                img = np.zeros((height, width, 3), np.uint8)

                cv2.line(img, pt1=(R_Arr0_x, R_Arr0_y), pt2=(R_Arr1_x, R_Arr1_y), color=(255, 255, 255), thickness=3)
                cv2.line(img, pt1=(R_Arr1_x, R_Arr1_y), pt2=(R_Arr2_x, R_Arr2_y), color=(255, 255, 255), thickness=3)
                cv2.line(img, pt1=(R_Arr2_x, R_Arr2_y), pt2=(R_Arr3_x, R_Arr3_y), color=(255, 255, 255), thickness=3)
                cv2.line(img, pt1=(R_Arr0_x, R_Arr0_y), pt2=(R_Arr3_x, R_Arr3_y), color=(255, 255, 255), thickness=3)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                binary = cv2.bitwise_not(gray)

                contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for i in range(len(contours)):
                    image = cv2.drawContours(img, [contours[i]], 0, (0, 0, 255), 2, cv2.LINE_8, hierarchy)
                    cv2.imshow('image', image)



    while True:
        cv2.imshow('11', image_to_show)
        cv2.setMouseCallback('11', mouse_callback, image_to_show)

        k = cv2.waitKey(1)

        if k == 27:
            break
    cv2.destroyAllWindows()