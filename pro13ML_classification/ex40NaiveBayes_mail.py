# 실습2) Spam메일 분류기 생성

# [1단계] : 데이터 불러오기 및 변수설정 
from sklearn.feature_extraction.text import CountVectorizer 
# CountVectorizer : 빈도를 표현
from sklearn.naive_bayes import MultinomialNB

# Multinomial Naiv Bayes(다항 나이브 베이즈)
# 텍스트에서 가장 많이 쓰는 NB모델
# 단어의 "빈도(count)"를 기반으로 분류한다.
# 형태 : "단어가 많이 나왔으면 그 단어 빈도에 비례하여 확률이 커진다."

# 학습용 데이터
texts = [
    "무료 쿠폰 지금 클릭하면 무료 선물",        # 0번째 문서
    "한번만 클릭해도 무료 대박",               # 1번째 문서
    "오늘 회의는 14시 제 3회의실 입니다.",     # 2번째 문서
    "지금 할인 행사 중",                      # 3번째 문서
    "회의 자료는 메일로 보내주세요.",          # 4번째 문서
    "지금 바로 쿠폰 확인"                     # 5번째 문서
]
labels = ["spam", "spam", "ham", "spam", "ham", "spam"]

# 단어 등장 횟수 비전 벡터 생성
vect = CountVectorizer()  # 문서로부터 단어의 순서정보는 무시하고, 단어 빈소수 정보만 받아들인다.
x = vect.fit_transform(texts)
print(vect.get_feature_names_out())
print(x.toarray())
print(vect.vocabulary_)  # 각 단어들에 번호를 붙여준다.
print(x) # "(0, 3)  3"  ->  "(문서번호, 단어번호) 등장횟수"


# [2단계] : NaiveBayes모델 제작 및 학습
from sklearn.metrics import accuracy_score
# 우리는 빈도수를 구해야하기 때문에 Multinomial을 써준다.
model = MultinomialNB()
model.fit(x, labels)
pred = model.predict(x)
print('정확도 : ', accuracy_score(labels, pred))
# 1.0
print()

# [3단계] : 새로운 data로 예측
# 새로운 문장으로 분류
text_test = ['무료 쿠폰 지급 발급', '간부 회의는 언제 시작하나요?']
# 2개의 새로운 데이터셋을 보임

x_test = vect.transform(text_test)
print(x_test)

# 예측 + 확률 출력
preds = model.predict(x_test)
probs = model.predict_proba(x_test)
class_names = model.classes_

for text, pred, prob in zip(text_test, preds, probs):
    prob_str = ", ".join([f'{cls}:{p:.4f}' for cls, p in zip(class_names, prob)]) 
    print(f"'{text}' --> 예측 : {pred} // 확률 : [{prob_str}]")
# 결과 : 
# '무료 쿠폰 지급 발급'           -->  예측 : spam  // 확률 : [ham:0.0627, spam:0.9373]
# '간부 회의는 언제 시작하나요?'  -->   예측 : ham   // 확률 : [ham:0.5588, spam:0.4412]