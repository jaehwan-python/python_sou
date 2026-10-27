from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import koreanize_matplotlib
import scipy.stats as stats


BRAND_ORDER = ["스타벅스", "폴바셋", "이디야", "탐앤탐스"]

# 함수1 : analysis_func : 설문 자료로 성별과 커피 브랜드 선호도가 관련 있는지 카이제곱 검정을 하는 함수(통계분석을 담당)
def analysis_func(rdata:list[dict]):
    df = pd.DataFrame(rdata)

    # 조건1 : 데이터에 값 유무
    if df.empty:
    # DataFrame에 값이 없다면
        return pd.DataFrame(), "데이터가 없어요", pd.DataFrame()

    df = df.dropna(subset = ["gender", "co_survey"])
    # gender와 co_survey 둘 다 NaN인 행은 지운다.

    # 그렇지 않고 DataFrame에 데이터가 있다면
    # 성별 브랜드별 선호 빈도수를 구해라
    crossTab = pd.crosstab(index=df["gender"], columns=df["co_survey"])

    # 조건2 : 데이터에 값이 있을 때 적절한 갯수의 충족여부 
    if crossTab.size == 0 or crossTab.shape[0] < 2 or crossTab.shape[1] < 2:
    # 표본자료수가 0행은 2개 미만, 열도 2개 미만이면...
        return crossTab, "표본자료가 부족해서 카이제곱 검정 수행이 불가하다!", df
        # df는 데이터값이 부족한 DataFrame이 나타날 것이다.

    # 그렇지 않고 데이터수가 2개 이상이면... = 충분히 많으면..
    alpha = 0.05
    # 뒤에서 사용할 유의수준을 0.05로 고정함.
    chi2, pv, dof, expected = stats.chi2_contingency(crossTab)

    # 조건3 : 기대빈도의 최소값
    min_expected = expected.min()
    note = ""
    if min_expected < 5:
        note = f"<br><small> * 주의 : 기대빈도 최소값 {min_expected:.2f} (5미만)</small>"

    # 조건4 : p값에 따라서 어느 가설을 채택할 지 결정 
    if pv >= alpha:
        results = f" p값:{pv:.7f} >= {alpha} : 성별에 따른 커피 선호 브랜드의 <b>차이가 없다(귀무가설 채택).</b> {note}"
    else:
        results = f" p값:{pv:.7f} < {alpha} : 성별에 따른 커피 선호 브랜드의 <b>차이가 있다(대립가설 채택).</b> {note}"

    return crossTab, results, df


# 함수2 : save_barchart_func : 커피 브랜드별 선호 건수를 막대그래프로 만들어 이미지 파일로 저장하는 함수
def save_barchart_func(df:pd.DataFrame, out_path:Path):
    if df is None or df.empty or "co_survey" not in df.columns:
        return False
    
    counts = df["co_survey"].value_counts().reindex(BRAND_ORDER, fill_value=0)
    
    # 만약에 저장소가 없으면 만들고 있으면 만들지 마.
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure()
    ax = counts.plot(kind="bar", width=0.6, edgecolor="black")
    ax.set_xlabel("커피 브랜드명")
    ax.set_ylabel("선호 건수")
    ax.set_title("커피 브랜드별 선호 건수")
    ax.set_xticklabels(BRAND_ORDER, rotation=0)
    fig.tight_layout()
    fig.savefig(str(out_path), dpi=120, bbox_inches="tight")
    # 불필요한 여백 제거!
    plt.close(fig)
    # 자원해제를 해주기!

    return True
