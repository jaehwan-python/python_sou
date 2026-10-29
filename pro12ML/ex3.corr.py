# 외국인(미국, 일본, 중국)이 국내 관광지(5개) 방문 관련자료 사용
# 국가별 관광지 상관관계 확인하기

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from pathlib import Path

# 입력받은 데이터로 산점도 그리기
def setScatterGraph(tour_table, all_table, tourPoint):
    # print("관광지명 : ", tourPoint)
    # print("tour_table 크기", tour_table)
    # print("all_table 크기", all_table.shape)
    # 결과(tourpoint) : 
    #                   창덕궁
    #                   운현궁
    #                   경복궁
    #                   창경궁
    #                     종묘 

    # 현재 관광지 데이터만 추출
    print('관광지명 : ', tourPoint)
    
    # 계산할 관광지 명에 해당하는 자료만 뽑아 tour에 저장 후 외국인 자료와 병합    
    tour = tour_table[tour_table['resNm'] == tourPoint]
    # print("관광지 방문 데이터 건수 : ", len(tour))
    # print("외국인 방문 데이터 건수 : ", len(all_table))
    print(tour)
    # 결과 :

    merge_table = pd.merge(tour, all_table, left_index=True, right_index=True)
    print(merge_table)
    # 결과 : 

    # 시각화 - 상관계수
    fig = plt.figure()
    fig.suptitle(tourPoint + '상관관계 분석')

    # 1. 중국인 방문객 수 시각화
    plt.subplot(1, 3, 1) 
    plt.xlabel('중국인 방문수')
    plt.ylabel('외국인 입장객 수')
    lamb1 = lambda p:merge_table['china'].corr(merge_table['ForNum'])
    r1 = lamb1(merge_table) # 상관계수1
    print('r1 : ', r1)
    # 결과 : -0.583421898
    plt.title('r={:.5f}'.format(r1))
    plt.scatter(merge_table['china'], merge_table['ForNum'], alpha=0.7, s=6, c='red')
    
    # 2. 일본인 방문객 수 시각화
    plt.subplot(1, 3, 2) 
    plt.xlabel('일본인 방문수')
    plt.ylabel('외국인 입장객 수')
    lamb2 = lambda p:merge_table['japan'].corr(merge_table['ForNum'])
    r2 = lamb2(merge_table) # 상관계수1
    print('r2 : ', r2)
    # 결과 : 0.5298702802205213(r2)
    plt.title('r={:.5f}'.format(r2))
    plt.scatter(merge_table['japan'], merge_table['ForNum'], alpha=0.7, s=6, c='blue')

    # 3. 미국인 방문객 수 시각화
    plt.subplot(1, 3, 3) 
    plt.xlabel('미국인 방문수')
    plt.ylabel('외국인 입장객 수')
    lamb3 = lambda p:merge_table['america'].corr(merge_table['ForNum'])
    r3 = lamb3(merge_table) # 상관계수1
    print('r3 : ', r3)
    # 결과 : -0.1211266682929496
    plt.title('r={:.5f}'.format(r3))
    plt.scatter(merge_table['america'], merge_table['ForNum'], alpha=0.7, s=6, c='blue')
    
    plt.tight_layout()
    plt.show()
    plt.close()

    return[tourPoint, r1, r2, r3]



# 각 관광지 정보받기 및 데이터 저장하기
def processFunc():
    # 서울특별시_관광지입장정보 읽기
    fname = "서울특별시_관광지입장정보_2011_2016.json"
    jsonTP = json.loads(open(fname, mode = 'r', encoding = 'utf-8').read())
    # 내가 지정한 데이터(fname)를 jsonTP라는 명령어로 열 수 있게 되었다.
    print(jsonTP)
    # 서울특별시_관광지입장정보를 가져옴

    tour_table = pd.DataFrame(jsonTP, columns=('yyyymm', 'resNm', 'ForNum'))
    # 방문년월, 관광지명, 외국인방문객수를 정리하여 df로 만들었다.
    tour_table = tour_table.set_index('yyyymm')
    print(tour_table.head()) 
    # 결과 : 
    #              resNm   ForNum
    #    yyyymm              
    #    201101    창덕궁    14137
    #    201101    운현궁        0
    #    201101    경복궁    40224
    #    201101    창경궁      697
    #    201101     종묘      6837

    resNm = tour_table.resNm.unique()
    print(resNm[:5])
    # 결과 : ['창덕궁', '운현궁', '경복궁', '창경궁', '종묘']

    # 1. 중국인 관광지 정보 파일 읽기
    cdf = '중국인방문객.json'
    jdata = json.loads(open(cdf, mode = 'r', encoding = 'utf-8').read())
    china_table = pd.DataFrame(jdata, columns=('yyyymm', 'visit_cnt'))
    china_table = china_table.rename(columns={'visit_cnt' : 'china'})
    china_table = china_table.set_index('yyyymm')
    print(china_table[:2])
    # 결과 : 
    #              china
    #    yyyymm        
    #    201101    91252
    #    201102   140571

    # 2. 일본인 관광지 정보 파일 읽기
    cdf = '일본인방문객.json'
    jdata = json.loads(open(cdf, mode = 'r', encoding = 'utf-8').read())
    japan_table = pd.DataFrame(jdata, columns=('yyyymm', 'visit_cnt'))
    japan_table = japan_table.rename(columns={'visit_cnt' : 'japan'})
    japan_table = japan_table.set_index('yyyymm')
    print(japan_table[:2])
    # 결과 : 
    #              japan
    #   yyyymm        
    #   201101    209184
    #   201102    230362

    # 3. 미국인 관광지 정보 파일 읽기
    cdf = '미국인방문객.json'
    jdata = json.loads(open(cdf, mode = 'r', encoding = 'utf-8').read())
    america_table = pd.DataFrame(jdata, columns=('yyyymm', 'visit_cnt'))
    america_table = america_table.rename(columns={'visit_cnt' : 'america'})
    america_table = america_table.set_index('yyyymm')
    print(america_table[:2])
    # 결과 : 
    #             america
    #   yyyymm         
    #   201101     43065
    #   201102     41077

    # < table 합치기 >
    all_table = pd.merge(china_table, japan_table, left_index = True, right_index = True)
    # 2개의 변수에 대해서 table합치기
    all_table = pd.merge(all_table, america_table, left_index = True, right_index= True)
    # 모든 변수에 대해서 table을 하나로 합치기
    print(all_table)
    # 결과 : 
    #            china    japan   america
    #   yyyymm                         
    #   201101   91252   209184    43065
    #   201102  140571   230362    41077
    #   201103  141457   306126    54610
    #   201104  147680   239075    59616
    #   201105  154066   241695    59780
    #   ...        ...     ...      ...
    #   201608  513275   148632    63522
    #   201609  591242   157313    63793
    #   201610  650174   180348    77878
    #   201611  507579   164685    62273
    #   201612  465218   159877    57580

    # < 관광지별 산점도 생성 및 반환 결과 수집 >
    r_list = []
    for tourPoint in resNm[:5]:
    # 관광지이름(resNm)을 하나씩 빼서 tourPoint에 넣는다.
        r_list.append(setScatterGraph(tour_table, all_table, tourPoint))
        # 넣은 관광지 이름을 r_list[]에 넣고,
        # 위에 setScatterGraph함수로 올라가서 산점도 받아오기
        # ... 

        # setScatterGraph의 결과로 tourPoint와 r1, r2, r3를 받아왔다.
    print('r-list : ', r_list)
    # 결과 : 
    # [['창덕궁', np.float64(-0.05879110406006314), np.float64(0.2774443570141011), np.float64(0.4028160633050156)], 
    #  ['운현궁', np.float64(0.44594488384450376), np.float64(0.30261521828798604), np.float64(0.2812576500158649)], 
    #  ['경복궁', np.float64(0.5256734293511215), np.float64(-0.43522818613412334), np.float64(0.4251372638704492)], 
    #  ['창경궁', np.float64(0.4512325398089607), np.float64(-0.16458589402253013), np.float64(0.6245403780269381)], 
    #  ['종묘', np.float64(-0.5834218986767473), np.float64(0.5298702802205213), np.float64(-0.1211266682929496)]]

    # 우리가 원하는 최종적인 자료
    r_df = pd.DataFrame(r_list, columns = ('고궁명', '중국', '일본', '미국'))
    r_df = r_df.set_index('고궁명')
    print(r_df)
    # 결과 : 
    #          중국       일본      미국
    # 고궁명                              
    # 창덕궁 -0.058791  0.277444  0.402816
    # 운현궁  0.445945  0.302615  0.281258
    # 경복궁  0.525673 -0.435228  0.425137
    # 창경궁  0.451233 -0.164586  0.624540
    # 종묘   -0.583422  0.529870 -0.121127

    r_df.plot(kind='bar', rot=50)
    plt.show()


if __name__ == "__main__":
    processFunc()

# 지금도 우리는 기술통계를 하고 있다. 아직 추론 통계를 하지 않았다.