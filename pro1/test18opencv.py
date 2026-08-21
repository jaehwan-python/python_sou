# open cv : 이미지 자료 처리 ... 따로 공부하기(중요) - 이 세상 구성 : 텍스트 vs 이미지
# opencv lib를 공부
# 파이썬은 이미지 처리를 못하지만 외부모듈인 cv2를 설치하면 가능하다

import cv2 # ... cv2모듈이 기존에 없다면 pip install opencv-python 혹은 conda install opencv-python 이거 설치
print(cv2.__version__)
img1 = cv2.imread('test18_any.jpeg')
print(type(img1)) # <class numpy.ndarray>...이거 왜 안뜨지


print('\n-------------------------------------------------------')

cv2.imshow('image test', img1)
cv2.waitKey() # 이미지를 잠시 세워둠
cv2. destroyAllWindows()
print('end')

# 다른이름으로 저장
cv2.imwrite('test18_any2.jpeg', img1)
cv2.imwrite('test18_any3.jpeg', img1, [cv2. IMWRITE_JPEG_QUALITY, 50]) # 화질

# 이미지 크기 조정
img2 = cv2.resize(img1, (300, 100), interpolation=cv2.INTER_AREA)
cv2.imwrite('test18_any4.jpeg', img2)
# 대문자로 시작한 변수는 상수이고 고정값으로 바뀔 수 없다.

# 밝기, 상하좌우 회전, 자르기 ... 지원
