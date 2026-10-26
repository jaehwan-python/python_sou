# [한글 사전]

# pip install JPype1 ... 이 라이브러리는 JAVA로 짜여진 라이브러리이기에 우리 컴퓨터에도 JAVA(컴파일러)가 먼저 설치되어 있어야 한다.
# https://bell-sw.com/pages/downloads/로 들어가서 Java 설치한다.    ...   지금까지 anaconda - python - git/github - mariadb(HeidiSQL) - Java 까지 설치하였다.
# pip install konlpy

# [영어 사전]
# conda install nltk
# python
# - import nltk
# - nltk.download()
# - 후에 nltk downloader에서 download 클릭


# 우리가 설치한 파일에 대해서 형태소 분석을 해본다.
# 말뭉치(Corpus) : 자연어 연구, 언어분석, 인공지능 학습을 위해 다양한 분야의 언어 자료를 
# 컴퓨터가 읽고 처리할 수 있도록 모아둔 대규모 텍스트/음성/영상데이터 집합
# 정의 : 사람이 실제로 쓰고 말한 언어 자료를 수집 빛 정제한 데이터

# 문법연구, 번역 시스템, 챗봇 등 다양한 언어 데이터 분석의 기초 자료로 활용된다.

# 형태소(Morpheme)는 의미를 가지는 가장 작은 단위를 말한다.

# 토큰(Token)이란? (자연어처리에서(NLP))
# : 컴퓨터가 텍스트를 이해하고 연산할 수 있도록 문장, 단어, 형태소 , 혹은 글자의 조각처럼 의미를 가진 최소단위로 쪼갠 결과물을 의미한다. 
# 종류 : 단어 토큰 / 형태소 토큰 / 서브워드 토큰 / 문자토큰
# 단어 토큰 : 
# 형태소 토믄 : 
# 서브워드 토큰 : 
# 문자 토큰 : 
# 숫자변환 어휘사전관리를 위해서 토큰화가 필요하다. 



print("\n\n 1. 영어 토큰(token)화 -----------")

# 1. 영어 토큰화
import nltk
from nltk.tokenize import word_tokenize

# 최초 실행할 때 필요한 데이터를 다운로드한다.
nltk.download("punkt")
nltk.download("punkt_tab")
# 이미 우리가 python에서 nltk.download를 했기에 위 두 문장의 코드들과 같은 코드들이 모두 다 들어있다.

text = "I am studying Python with my friends at room."

# [예제2] : 토큰화
tokens = word_tokenize(text)
print(tokens)
# 영어는 띄어쓰기를 기준으로 해당 문장을 끊는다.
# 결과 : ['I', 'am', 'studying', 'Python', 'with', 'my', 'friends', 'at', 'room', '.']
print()

# 품사 태깅
pos_tags = nltk.pos_tag(tokens)
print(pos_tags)
# 품사를 기준으로 해당 문장을 끊는다.
# 결과 : [('I', 'PRP'), ('am', 'VBP'), ('studying', 'VBG'), ('Python', 'NNP'), ('with', 'IN'), ('my', 'PRP$'), ('friends', 'NNS'), ('at', 'IN'), ('room', 'NN'), ('.', '.')]



print("\n\n 2. 한국어 토큰(token)화 -----------")

# 2. 한글 토큰화

from konlpy.tag import Okt, Kkma, Komoran
# 대표적인 한글 형태소 분석 라이브러리
# 실시간으로는 안된다. 할려면 유료이기 때문...

text = "나는 오늘 아침에 학교에 갔다. 가는 길에 국화가 피어 너무 아름다웠다."

print('예제1. Okt를 써보자. -----------')
# Okt = 한국어 문장을 형태소로 나누고 품사를 분석하는 도구
# [예제1] : Okt()
okt = Okt()
print("형태소 : ", okt.morphs(text))
# 결과 : 형태소 :  ['나', '는', '오늘', '아침', '에', '학교', '에', '갔다', '.', '가는', '길', '에', '국화', '가', '피어', '너무', '아름다웠다', '.']

print("품사 태깅 : ", okt.pos(text))
# 결과 : 품사 태깅 :  [('나', 'Noun'), ('는', 'Josa'), ('오늘', 'Noun'), ('아침', 'Noun'), ('에', 'Josa'), ('학교', 'Noun'), ('에', 'Josa'), ('갔다', 'Verb'), ('.', 'Punctuation'), ('가는', 'Verb'), ('길', 'Noun'), ('에', 'Josa'), ('국화', 'Noun'), ('가', 'Josa'), ('피어', 'Noun'), ('너무', 'Adverb'), ('아름다웠다', 'Adjective'), ('.', 'Punctuation')]

print("품사 태깅(어간 포함) : ", okt.pos(text, stem=True))
# 결과 : 품사 태깅(어간 포함) :  [('나', 'Noun'), ('는', 'Josa'), ('오늘', 'Noun'), ('아침', 'Noun'), ('에', 'Josa'), ('학교', 'Noun'), ('에', 'Josa'), ('가다', 'Verb'), ('.', 'Punctuation'), ('가다', 'Verb'), ('길', 'Noun'), ('에', 'Josa'), ('국화', 'Noun'), ('가', 'Josa'), ('피어', 'Noun'), ('너무', 'Adverb'), ('아름답다', 'Adjective'), ('.', 'Punctuation')]

print("명사 추출 : ", okt.nouns(text))
# 결과 : 명사 추출 :  ['나', '오늘', '아침', '학교', '길', '국화', '피어']

# 이렇게 각 형태소 별로 뽑아서 리스트로 저장해두었다.
# JAVA를 설치한 이유 : 형태소 분석 라이브러리는 JAVA로 짠 코드이기 때문이다.

print('예제2. Kkma를 써보자. -----------')
# [예제2] : Kkma()
kkma = Kkma()
print("형태소 : ", kkma.morphs(text))
print("품사 태깅 : ", kkma.pos(text))
print("품사 태깅(어간 포함) : ", kkma.pos(text, stem=True))
print("명사 추출 : ", kma.nouns(text))

print('예제3. Komoran를 써보자. -----------')
# [예제2] : Kkma()
komoran = Komoran()
print("형태소 : ", komoran.morphs(text))
print("품사 태깅 : ", komoran.pos(text))
print("품사 태깅(어간 포함) : ", komoran.pos(text, stem=True))
print("명사 추출 : ", komoran.nouns(text))

# 가장 좋은 것은 Mecab라이브러리지만 이는 Linux에서만 사용가능하다...!!

