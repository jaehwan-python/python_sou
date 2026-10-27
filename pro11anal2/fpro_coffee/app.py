# 지금까지 외부파일(github/pykwon)에서 자료를 가져와 카이제곱 검정을 통해 귀무가설과 대립가설 중 무엇을 택할지
# ctab을 만들어서 chi2, pv, dof, expected값을 알아내어(chi2_contingency) 가설을 선택하였다. -> 유의수준과 유의확률의 관계를 따짐

# 목표 : "실제 'web'을 통해 데이터를 받고 받은 데이터를 DB에 저장한다. 그리고 DB에 저장된 데이터를 다시 뽑아 DataFrame으로 만들어 데이터 분석을 통한 가설검정을 진행히보자!!"

# 우선 DB 프롬프트에 들어가서 아래 명령어들을 순서대로 입력하여 coffeedb라는 db에다가 survey라는 table을 만든다.
# mysql -uroot -p
# create database coffeedb;
# use coffeedb; 
# create table survey(rnum int primary key auto_increment, gender varchar(4),age int(3),co_survey varchar(10));
# insert into survey (gender,age,co_survey) values ('남',10,'탐앤탐스');
# insert into survey (gender,age,co_survey) values ('여',10,'스타벅스');
# select * from survey;
# 를 차례대로 입력하면 table이 새로 만들어졌다.

# app.py에서 작업진행과정 숙지  ->  db.py로 이동  ->  analysis.py로 이동  ->  templates/index.html로 이동  ->  app.py로 다시 돌아와라

from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from db import insert_survey, fetchall_survey
from analysis import analysis_func, save_barchart_func
# analysis.py파일에 만들어둔 2개의 함수를 불러올 것이다.

BASE_DIR = Path(__file__).resolve().parent
IMG_PATH = BASE_DIR / "static" / "images" / "vbar.png"

app = Flask(__name__)

# 라우팅 요청1
@app.get("/")
def index():
    return render_template("index.html")


# 라우팅 요청2
@app.get("/coffee/survey")
def survey_view():
    return render_template("coffee/coffeesurvey.html")


# 라우팅 요청3
@app.post("/coffee/surveyprocess")
def surveyprocess():
    gender = (request.form.get("gender") or "").strip()
    age_raw = (request.form.get("age") or "").strip()
    co_survey = (request.form.get("co_survey") or "").strip()

    print(gender, age_raw, co_survey)
    # 클라이언트가 입력한 정보가 터미널 창에 뜬다!! 하지만 아직 db에 저장된 것은 아니다..

    # 1번. web에서 입력한 값을 db로 저장해보자.
    # 입력 검증
    if not gender or not co_survey or not age_raw.isdigit():
        return redirect(url_for("survey_view"))
        # url로 survey_view라는 함수(라우팅 요청2)를 호출한다.
    age = int(age_raw)

    # DB에 저장!! _ (db.py를 불러온다. db.py의 함수를 불러온다. 위에서 db.py를 import했음)
    insert_survey(gender=gender, age=age, co_survey=co_survey)
    # db.py에서 auto commit으로 설정되어 있기에 이제 이 실행문을 하면 db.py에 의해 web에서 클라이언트가 넣은 값이 db로 들어간다!!


    # 2번. db데이터 조회 및 분석
    rdata = fetchall_survey()
    crosstab, results, df = analysis_func(rdata)
    # analysis.py의 analysis_func()가 crosstab, results, df를 반환한다.
    # 입력한 rdata를 analysis.py로 보내는 것이다.


    # 3번. 차트에 저장 = 이미지 폴더에 저장한다!
    if not df.empty:
        save_barchart_func(df, IMG_PATH)

    return render_template("/coffee/result.html", 
                            crossTab = crosstab.to_html() if not crosstab.empty else "데이터가 없군요", 
                            results = results,
                            df = df.to_html(index=False) if not df.empty else " ")
    # 웹에서 입력받은 데이터를 db에 저장했고 fetchall로 불러와서 rdata로 저장하였다. 
    # 그리고 rdata를 analysis.py의 analysis_func로 보내서 df로 만들어 가설검정을 하여 결과를 만든 후,
    # result.html로 보낸다. = 가설검정을 하였다.



# 라우팅 요청4 : 설문을 제출하지않고도 /coffee/surveyshow 주소로 결과 페이지를 열 수 있게 하는 것
@app.get("/coffee/surveyshow")
def survey_show():

    # 저장없이 결과만 출력
    rdata = fetchall_survey()
    crosstab, results, df = analysis_func(rdata)

    return render_template("/coffee/result.html", 
                            crossTab = crosstab.to_html() if not crosstab.empty else "데이터가 없군요", 
                            results = results,
                            df = df.to_html(index=False) if not df.empty else " ")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
