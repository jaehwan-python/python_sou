# 정규 표현식
import re # 정규표현식 지원 모듈을 로딩함.

ss = "1234abc가나다abcABC_1234555실습중78입니다_6'뿌웨웨엑~ 나는 우주경찰 빵빵 또로로로롱 빵빵 띵띵띵띵 띵땅땅 김덕배 입니다아"
print(ss)
print(re.findall('123', ss)) #ss에 있는 123 패턴이 있는 걸 모두 찾는다. # re.findall(패턴, 대상 문자열)
# list 타입으로 받음
# 're. ' 모듈 내에 findall이라는 함수가 있다.
print(re.findall(r'빵', ss))
print(re.findall(r'[0-9]', ss))
print(re.findall(r'[0 1 3]', ss)) # 이 값들 중 한 개씩
print(re.findall(r'[0-9]+', ss))
print(re.findall(r'[0-9]+', ss))
print(re.findall(r'[0-9]{2}', ss))
print(re.findall(r'[0-9]{2,3}', ss))

print()

print(re.findall(r'[a b]', ss))
print(re.findall(r'[ab]', ss)) # a b사이에 공백이 있냐 없냐에 따라서 패턴 문자의 형태가 달라짐
print(re.findall(r'[a-zA-Z]', ss))
print(re.findall(r'[a-zA-Z]+', ss))
print(re.findall(r'[가-힣]+', ss)) # 한글값만 뽑아냄.

print()

print(re.findall(r'\d', ss)) # 모든 숫자
print(re.findall(r'\d+', ss)) # 
print(re.findall(r'\D+', ss)) # \d 반대

print()

print(re.findall(r'\s', ss)) # 공백, 탭 문자와 매핑
print(re.findall(r'\s+', ss)) 
print(re.findall(r'\S+', ss)) 

# 정규표현식 기초 공부

# r을 왜 붙이지..?
# [0-9] ..? : 0에서 9까지 숫자만
# +, {2, 3} ..? : + 연속적 / * 