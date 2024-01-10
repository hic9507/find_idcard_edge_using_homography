# Find ID Card edge(boundary) 

## 방법 1. 전통적인 방법(blur, canny, contour 등의 opencv 연산 사용) - draw_contour.py

### 사용된 주요 알고리즘
cv2.equalizeHist -> 신분증을 선명하게 처리

cv2.GaussianBlur -> 배경을 흐릿하게 처리

cv2.Canny -> 신분증 edge 탐색

cv2.findContours -> edge를 이용해 boundary 탐색

cv2.drawContours -> edge boundary 생성
#### 시연 과정
![방법1](https://github.com/hic9507/find_idcard_edge_using_various_method/assets/65755028/e4787a19-12be-429e-8b8c-3fa14b0d9aa6)

## 방법 2. 호모그래피(Homography)를 이용한 방법

### 사용된 주요 알고리즘
cv2.EVENT_LBUTTONDOWN -> 마우스 입력 함수

cv2.findHomography -> 사각형 간의 호모그래피(투시행렬) 계산

cv2.perspectiveTransform -> 호모그래피를 이용해 좌표들을 원하는 방향으로 변환

#### 시연 과정
![방법2 시연과정](https://github.com/hic9507/find_idcard_edge_using_various_method/assets/65755028/c2feba85-9e84-43cd-8132-ab4840c869cc)

초록색 테두리 - 실제 촬영한 신분증

파란색 테두리 - 정면에서 본 신분증
1) 신분증을 기울여서 찍은 모습

2) 신분증을 기울여서 찍었을 때 증명사진 부분의 꼭짓점을 사용해 임의의 파란 사각형을 그린다. 이 파란 사각형은 정면에서 신분증을 보았을 때의 증명사진을 나타낸다. 그리고 작은 사각형(초록색 평행사변형과 파란색 사각형) 간의 homography(H)를 계산한다.

3) 실제 신분증의 증명사진 부분과 테두리 길이를 계산한 비율을 통해 임의의 사각형으로부터 큰 직사각형(정면에서 본 신분증)을 생성한다.

4) 위의 2)에서 구한 호모그래피를 이용하여 큰 파란 직사각형으로부터 사진에 있는 신분증의 테두리를 그린다. 계산을 통해 생성한 정면에서 본 신분증의 테두리를 이용해서 실제 신분증의 테두리를 구하는 과정

5) 4)에서 실제 얻고자 하는 테두리만 남긴다.

6) 실제 신분증의 테두리를 얻는다.
