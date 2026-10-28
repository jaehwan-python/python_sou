from flask import Flask, render_template, request

import pandas as pd

import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt

import seaborn as sns

import koreanize_matplotlib

import matplotlib
matplotlib.use('Agg')
# Anti Grain Gemetric : 이미지 저장 시 오류 방지용(차트 출력 없이 저장할 때)

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
# 현재 파일의 경로를 얻을 수 있다.
# [상대경로 vs 절대경로]
# 절대경로 : 드라이브의 최상위부터 파일 위치를 전부 표시
# 상대경로 : 기준 폴더에서 파일까지의 위치를 표시
STATIC_DIR = BASE_DIR / 'static' / 'images'
STATIC_DIR.mkdir(parents=True, exist_ok=True)
# 이미지 파일의 경로를 연결해줌. 그리고 지정한 경로에 실제 폴더를 만든다.
# .mkdir(): 폴더 생성
# parents=True: 중간 폴더인 static이 없으면 함께 생성
# exist_ok=True: 폴더가 이미 있어도 오류 없이 진행
# app.py위치를 기준으로 이미지 저장 폴더 경로를 정하고, 없으면 생성하는 코드이다.

df = sns.load_dataset('iris')

# 라우팅 요청1
@app.get("/")
def main():
    return render_template("main.html")


# 라우팅 요청2
@app.get("/showdata")
def showdata():
    # df = sns.load_dataset('iris')
    # 라우팅 안에 sns.load_dataset()을 하면
    # showdata를 새로고침할 때마다 긴 iris 데이터를 계속 불러와야한다. ... 비효울적!!
    # 그래서 라우팅 밖으로 빼준다!!
    
    # print(df.head())
    # 결과 :     sepal_length  sepal_width  petal_length  petal_width species
    #        0           5.1          3.5           1.4          0.2  setosa
    #        1           4.9          3.0           1.4          0.2  setosa
    #        2           4.7          3.2           1.3          0.2  setosa
    #        3           4.6          3.1           1.5          0.2  setosa
    #        4           5.0          3.6           1.4          0.2  setosa

    # [1단계]
    irisdata = df.to_html()
    # 인덱스가 있는 iris의 데이터를 태그형태로 인덱스를 빼준다.

    # [2단계]
    # 이번에는 pie chart를 생성 및 저장한다(서버에서 자체적으로 출력하는 것 아니다!!)
    counts = df['species'].value_counts().sort_index()

    # [3단계]
    plt.figure()
    counts.plot.pie(autopct='%1.1f%%', startangle=90, ylabel='')
    plt.tight_layout()

    # [4단계]
    img_path = STATIC_DIR / 'fpro_pandas.png'
    # 내가 지정한 경로에 원하는 파일을 생성한다.
    plt.savefig(img_path, dpi=130)
    # 만든 그래프를 이미지 파일로 저장(그래프  ->  이미지) 
    # dpi : 해상도
    plt.close()
    # 사용이 끝난 그래프를 닫아서 메모리를 정리하기 위해 = 메모리 자원 해지
    # 특히 웹 상에서 꼭 해주어야 한다.

    return render_template("show.html", irisdata = irisdata, piechart = 'images/fpro_pandas.png')
# 외부에서 Iris 데이터를 불러와 종류별 개수를 집계하고, Matplotlib으로 그래프를 만든 뒤
# plt.savefig()로 지정된 경로에 이미지 파일을 저장하면, 
# HTML의 <img> 태그를 통해 브라우저가 Flask 서버에서 해당 이미지를 받아 화면에 표시하는 과정


# 라우팅 요청3 : 동적이미지를 처리
@app.get("/showdata2")
def showdata2():
    irisdata = df.to_html()
    counts = df['species'].value_counts().sort_index()

    # [1단계] : chart.js에 전달할 데이터
    labels = counts.index.to_list()
    # js에서 읽기 위함이다. chart.js에 
    values = counts.tolist()

    return render_template("show2.html", irisdata = irisdata, labels = labels, values = values)

    
    

if __name__ == '__main__':
    app.run(debug=True)