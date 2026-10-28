# 'numpy'로 데이터를 계산하여 값을 조작해보았고
# 'pandas'를 이용하여 데이터를 2차원인 데이터프레임으로 만들었다. 그리고 file, db, web에서 데이터를 가져와서 내 컴퓨터의 RAM에서 DataFrame형태로 저장해보았다. 
# 이때 저장한 DataFrame을 numpy를 이용하여 연산한다. 
# 'matplotlib'를 이용하여 데이터를 보기좋게 시각화하였다.
# 이제 보기 좋게 만들어진 데이터를 서버에서 보이게 출력하도록 만들 것이다.

# 그럼 DB에 있는 정보를 가지고 웹에 표현해보자.
# maria DB-test DB  ->  DataFrame시각화(numpy/pandas/matplotlib)  ->  Flask서버  ->  브라우저

# flask를 쓰고 있지만 실무에서는 Fast API나 Django서버를 사용한다.

from flask import Flask, render_template, request
import pymysql
import numpy as np
import pandas as pd
from markupsafe import escape
# 웹에 출력되는 입력값의 특수문자(예:<,>,&,")를 안전한 html엔티티(&lt;, &gt;)로 바꾸어서 XSS공격에 방지. 
# markupsafe는 Flask서버에서만 사용가능하다.


app = Flask(__name__)

config = {'host' : '127.0.0.1',
        'user' : 'root',
        'password' : '123',
        'database' : 'test',
        'port' : 3306,
        'charset' : 'utf8'}

def get_connection():
    return pymysql.connect(**config)


# 라우팅 요청1 : /
@app.route("/")
def index():
    return render_template("index.html")


# [직원번호, 직원명, 부서명, 부서전화, 연봉, 직급 자료 읽어 출력]
# 라우팅을 여러 개 작성하지 않고 하나의 라우팅 안에서 조건문을 통해 여러 작업의 결과를 출력해보자.

# 라우팅 요청2 : /dbshow
@app.route("/dbshow", methods=["GET", "POST"])
def dbshow():

    # [1단계] ~ [6단계] : db에서 내가 원하는 데이터를 sql문으로 가져와서 내 RAM에서 DataFrame으로 만드는 과정

    # [1단계] 
    dept = request.args.get("dept", "")
    # get방식의 요청(args)으로 "dept"을 받게되면 해당 값을 dept로 저장하고 없으면 빈 문자열을 반환한다.

    # [2단계]
    sql = """
        select j.jikwonno as 직원번호, j.jikwonname as 직원명, b.busername as 부서명, b.busertel as 부서전화, j.jikwonpay as 연봉, j.jikwonjik as 직급
        from jikwon j inner join buser b
        on j.busernum=b.buserno
    """

    # [3단계]
    params = []
    if dept:
        sql += " where b.busername like %s"
        params.append(f"{dept}%")
    # 내가 입력한 dept값 있으면 sql문에 where조건을 붙인다.
    # 그때 붙인 조건의 값은 params로 넣어준다. ... %s : params의 값이 들어갈 자리
    # 이때 %s를 안쓰고 곧바로 dept를 넣어주게 되면 sql 인젝션 문제가 발생할 수 있다.

    # 아무것도 입력되지 않으면 sql문에 아무것도 붙지 않은, 전체 직원을 조회하게 한다. = 즉, 3번은 실행하지 않고 4번으로 넘어간다.

    # [4단계]
    sql += " order by j.jikwonno asc"
    # 우리가 위에서 만들어 둔 긴 sql문에다가 특정 조건이 붙게 되면 조건문으로 바뀐 조건에 따라 sql문을 붙여준다.

    # [5단계]
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            cols= [c[0] for c in cur.description]
    # 앞에서 만든 SQL을 실제 DB에서 실행하고, 결과와 열 이름을 가져온다.

    # [6단계] : DataFrame구조 생성
    df = pd.DataFrame(rows, columns=cols)
    print(df)
    print(df.to_html())
    # 조건에 따라 가져온 데이터를 DataFrame형태로 만들었다.
    # 브라우저에서 조회를 누르고 터미널 창을 보면 'df'에 의해 DataFrame이 보이고
    #                                           'df.to_html()'에 의해 인덱스가 빠진 html 태그가 보인다.

    # return render_template("dbshow.html", 
    #                         jikwondata=df.to_html(index=False))

        # 가져온 db의 데이터를 DataFrame형태로 만들고 이를 dbshow.html로 응답한다.
        # df_to.html로 요청받은 자료를 jikwondata에 저장한다. 왜?  jinja2문법을 쓰기 위해서(python-html)
        # 그냥 'df'로 넘기면 안되는 이유 : 인덱스도 같이 넘어가는 것을 방지하기 위해서이다.

    # 그래서 앞으로 예제를 풀때 .to_html()을 붙여서 table의 인덱스를 없애준 후에 넘겨줄 것이다.


    # < 예제 1번 : 부서명을 입력하고 조회하게 되면(부서명을 입력받으면) 해당 부서에 근무하는 직원을 출력해보자! >

    if not df.empty:
        jikwondata = df[['직원번호', '직원명', '부서명', '부서전화', '연봉']].to_html(index=False)
        # jikwondata = df.to_html(index=False)
    else:
        jikwondata = "직원정보가 없습니다"

    # print(jikwondata)

    # return render_template("dbshow.html", 
    #                         jikwondata = jikwondata, 
    #                         dept=escape(dept))
    # dept=escape(dept) : xss방지
    # 부서명을 입력하면 입력한 부서의 직원들의 정보가 조회된다.  ->  dbshow.html의 {{jikwondata | safe}}로 받는다.


    # < 예제2 : 직급별 연봉의 통계(평균, 표준편차)를 출력해보자! >
    if not df.empty:
        stats_df = (
            df.groupby("직급")["연봉"]
            .agg(평균 = "mean", 표준편차=lambda x:x.std(ddof=0))
            # ddof=0 : 모표준편차를 의미
            # ddof=1 : 표본표준편차를 의미
            .round(2)
            .reset_index()
            .sort_values(by='평균', ascending=False)
        )
        stats_df['표준편차'] = stats_df['표준편차'].fillna(0)
        print(stats_df.to_html(index=False))
        # print(stats_df.to_html(index=False))이게 출력되면 잘된거임 ㅇㅇ
        # cross table과 dataframe만 .to_html이 가능하다!
        statsdata = stats_df.to_html(index=False)

    else:
        statsdata = "통계대상 자료가 없습니다."
    
    # return render_template("dbshow.html", 
    #                         jikwondata = jikwondata, 
    #                         statsdata=statsdata, 
    #                         dept=escape(dept))
    # 각 직급별 대상의 연봉의 평균이 뜬다.  ->  dbshow.html의 {{statsdata | safe}}로 받는다.


    # < 예제3 : 부서별 직급별 직원 수 교차표를 출력해보자! >
    if not df.empty:
        crosst = pd.crosstab(
            index=df['부서명'],
            columns=df['직급'],
            margins=True, margins_name='합계'
        )
        crossdata = crosst.to_html()
    else:
        crossdata = "교차표대상 자료가 없습니다"


    return render_template('dbshow.html',
                            jikwondata=jikwondata,
                            statsdata= statsdata,
                            crossdata= crossdata,
                            dept=escape(dept)) 

if __name__ == "__main__":
    app.run(debug=True)

# 메인페이지에서 db조회페이지로 들어가서 
# 부서명에 아무것도 입력하지 않고 조회를 누르면
# 전체 직원목록 + 전체 직급별 연봉 통계 + 모든 부서별-직급별 인원수가 나온다.

# 부서명을 입력하고 조회를 누르면 해당 부서에 대한 값만 출력된다.
# 그때 부서명의 fullname을 입력하지 않고 첫글자만 적고 조회를 눌러도 해당 값이 출력된다.
# 이유 : sql += " where b.busername like %s"
#       params.append(f"{dept}%")
# 해당 위 코드에서 %가 '뒤에 글자가 없거나 어떤 글자가 와도 된다'라는 의미

# db에 존재하지 않는 부서명을 입력하고 조회를 누르면 
# "직원정보가 없습니다"
# "통계대상 자료가 없습니다"
# "교차표대상 자료가 없습니다"
# 가 뜨게 된다.
