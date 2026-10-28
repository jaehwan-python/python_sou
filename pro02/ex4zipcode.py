# 파일에서 데이터 가져와 읽기
# 데이터베이스에서 데이터 가져와 읽기
# 웹에서 데이터 가져와 읽기

# 이번시간에는 파일에서 데이터를 가져와 읽기를 해본다.

# 우편정보 파일 자료 읽기
# 키보드에서 입력한 동일한 이름으로 해당 주소 정보를 출력한다.

def zipProcess():
    dongIrum = input('동 이름을 입력하세요 : ')
#   dongIrum = '안기동' 
#   print(dongIrum)

    with open(r'zipcode.txt', mode = 'r', encoding = 'utf-8') as f:
#       line = f.read() # zipcod.txt 전체 다 읽기
        line = f.readline() # 하나의 행만 읽기

#       print(line) # 135-806 서울    강남구  개포1동 경남아파트              1
#       주소 문자열 자르기
#       lines = line.split('\t') # Tab키를 기준으로 구분지어서 리스트 타입 형태로 반환한다
#       print(lines) # ['135-806', '서울', '강남구', '개포1동 경남아파트', '', '1\n']  # 동네 이름은 3번째 인덱스에서 나온다.
#       아스키 코드의 Tab 키는 9이다.

        lines = line.split(chr(9)) # chr(9) : line에서 아스키코드 9라는 값에 해당하는 키를 기준으로 split(잘라서)해서 변수 lines에 저장ㅎ나다. 
#       =  lines = line.split('\t')

        while line: # 읽을 자료가 있으면 True고 없으면 Fasle이다.
            lines = line.split(chr(9)) # 뽑아온 하나의 행을 다시 잘라서 가져옴. 문자열 자르기 : split  chr(9) : 아스키 코드 기준으로 Tab키를 의미
            if lines[3].startswith(dongIrum): # line의 3번째 인덱스의 시작위치가 동이름이 맞는가?
#               print(lines)
                print(f'우:{lines[0]}, {lines[1]}, {lines[3]}')
            line = f.readline()

# zipcode.txt에서 내가 원하는 행만 쏙 뽑아서 읽는 방법
if __name__ == '__main__':
    zipProcess()
