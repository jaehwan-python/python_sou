# pandas 문제 8)

# MariaDB에 저장된 jikwon, buser 테이블을 이용하여 아래의 문제에 답하시오.

# Django 또는 Flask 모듈을 사용하여 결과를 클라이언트 브라우저로 출력하시오.

from flask import Flask, render_template, request
import pymysql
import numpy as np
import pandas as pd
from markupsafe import escape
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

app = Flask(__name__)

config = {'host' : '127.0.0.1',
        'user' : 'root',
        'password' : '123',
        'database' : 'test',
        'port' : 3306,
        'charset' : 'utf8'}

def get_connection():
    return pymysql.connect(**config)

# 라우팅 요청2
@app.route("/")
def index():
    return render_template("index.html")


# 라우팅 요청1
@app.route("/dbshow", methods=["GET", "POST"])
def dbshow():

        # [1단계] ~ [6단계] : db에서 내가 원하는 데이터를 sql문으로 가져와서 내 RAM에서 DataFrame으로 만드는 과정

    # [1단계] 
    dept = request.args.get("dept", "")

    # [2단계]
    sql = """
        select j.jikwonno as 사번, j.jikwonname as 직원명, b.busername as 부서명, j.jikwonjik as 직급, j.jikwonpay as 연봉, j.jikwonibsail as 근무년수, j.jikwongen as 성별
        from jikwon j inner join buser b
        on j.busernum=b.buserno
    """

    # [3단계]
    params = []
    if dept:
        sql += " where b.busername like %s"
        params.append(f"{dept}%")

    # [4단계]
    sql += " order by b.busername asc, j.jikwonname asc"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            cols= [c[0] for c in cur.description]

    # [5단계] : DataFrame구조 생성
    df = pd.DataFrame(rows, columns=cols)


    # < 예제 1번 : 사번, 직원명, 부서명, 직급, 연봉, 근무년수를 DataFrame에 기억 후 출력하시오. (join) : 부서번호, 직원명 순으로 오름 차순 정렬해보자!  >
    if not df.empty:
        jikwondata = df[['사번', '직원명', '부서명', '직급', '연봉', '근무년수']].to_html(index=False)
        jikwondata = df.to_html(index=False)
    else:
        jikwondata = "해당 정보가 없습니다"
    # return render_template("dbshow.html", jikwondata=jikwondata)


    # < 예제 2번 : 부서명, 직급 자료를 이용하여 각각 연봉 합, 연봉 평균을 구해보자!  >
    if not df.empty:
        stats_df = (
            df.groupby(["부서명", "직급"])["연봉"]
            .agg(연봉합계="sum", 연봉평균="mean")
            .round(2)
            .reset_index()
        )

        statsdata = stats_df.to_html(index=False)
    else:
        statsdata = "해당 정보가 없습니다"



#    < 예제 3번. 부서명별 연봉합, 평균을 이용하여 세로막대 그래프를 출력해보자 > 
    chartdata = ""
    if not df.empty:
        chart_df = df.groupby("부서명")["연봉"].agg(연봉합계="sum", 연봉평균="mean")
        fig = Figure(figsize=(9, 5))
        ax = fig.subplots()
        font = FontProperties(family="Malgun Gothic")
        positions = list(range(len(chart_df)))

        ax.bar([x - 0.2 for x in positions], chart_df["연봉합계"], width=0.4, label="연봉합계")
        ax.bar([x + 0.2 for x in positions], chart_df["연봉평균"], width=0.4, label="연봉평균")

        ax.set_xticks(positions)
        ax.set_xticklabels(chart_df.index, fontproperties=font)
        ax.set_title("부서별 연봉 합계와 평균", fontproperties=font)
        
        ax.legend(prop=font)
        fig.tight_layout()

        with BytesIO() as buffer:
            fig.savefig(buffer, format="png")
            chartdata = base64.b64encode(buffer.getvalue()).decode("ascii")



#    < 예제 4번. 성별, 직급별 빈도표를 출력해보자 >
    if not df.empty:
        cross_df = pd.crosstab(df["성별"], df["직급"])
        crossdata = cross_df.to_html()

    else:
        crossdata = "해당 정보가 없습니다"



#    < 예제 5번. 부서별 최고 연봉자 출력 : 부서명별로 가장 연봉이 높은 직원 1명씩 출력 >
#      출력 항목: 부서명, 직원명, 연봉
    if not df.empty:
        # 최고 연봉이 같으면 조회 순서에서 첫 번째 직원 한 명 선택
        top_df = (
            df.sort_values("연봉", ascending=False, kind="stable")
            .drop_duplicates("부서명")[["부서명", "직원명", "연봉"]]
            .sort_values("부서명")
        )
        topdata = top_df.to_html(index=False)
    else:
        topdata = "해당 정보가 없습니다"



#    < 예제 6번. 부서별 직원 비율 계산 : 전체 인원 대비 각 부서 인원 비율(%) >
#        비율 계산 (%)은 dept_ratio = (dept_count / total * 100).round(2)
#       결과를 DataFrame으로 출력
#       예: 총 인원: 30명
#            영업부 20%
#            총무부 30%
#            전산부 5%
#            ...
    total = len(df)
    if not df.empty:
        dept_count = df.groupby("부서명").size()
        dept_ratio = (dept_count / total * 100).round(2)
        ratio_df = pd.DataFrame({"인원수": dept_count, "비율(%)": dept_ratio}).reset_index()
        ratiodata = ratio_df.to_html(index=False)

    else:
        ratiodata = "해당 정보가 없습니다"

    return render_template("dbshow.html", jikwondata=jikwondata, statsdata=statsdata, 
                                        chartdata=chartdata, crossdata=crossdata, topdata=topdata,
                                        ratiodata=ratiodata, total=total, dept=dept)

if __name__ == "__main__":
    app.run(debug=True)
