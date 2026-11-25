import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 기본 페이지 설정
st.set_page_config(page_title="경제력과 행복도 분석", layout="wide")
st.title("📊 국가의 행복도는 경제력으로 나뉘는가?")

# 2. 데이터 구축 (이전 데이터 재사용)
@st.cache_data
def load_data():
    data = {
        "국가": ["미국", "중국", "독일", "일본", "영국", "인도", "프랑스", "러시아", "이탈리아", "브라질", "캐나다", "대한민국", "결측치테스트국가"],
        "명목_GDP_억불": [326840, 215470, 54713, 43420, 42685, 40619, 35542, 28612, 27017, 26548, 24903, 22458, None],
        "1인당_GDP_달러": [95212, 15371, 65699, 35400, 61108, 2750, 51448, 19953, 45886, 12397, 60105, 43512, 10000],
        "행복_점수": [6.816, 6.074, 6.882, 6.130, 6.694, 4.536, 6.586, 5.835, 6.574, 6.634, 6.741, 6.040, None],
        "행복_순위": [23, 65, 17, 61, 29, 116, 35, 79, 38, 32, 25, 67, None]
    }
    return pd.DataFrame(data)

raw_df = load_data()

# --- [체크리스트 1 & 4: 데이터 개요 및 전처리 기준] ---
st.header("1. 데이터 개요 및 전처리 (결측치 처리)")
col1, col2 = st.columns(2)

with col1:
    st.subheader("원본 데이터")
    st.write(f"- **행·열 수:** {raw_df.shape[0]}행, {raw_df.shape[1]}열")
    st.write("- **각 열의 자료형:**")
    st.write(raw_df.dtypes.astype(str))
    st.write("- **결측치(빈 칸) 개수:**")
    st.write(raw_df.isnull().sum())

clean_df = raw_df.dropna(subset=["1인당_GDP_달러", "행복_점수"]).copy()

with col2:
    st.subheader("전처리 결과")
    st.error("**처리 기준:** 분석 핵심인 `1인당_GDP_달러`나 `행복_점수`가 빈칸(결측치)인 국가는 행 전체를 삭제함.")
    st.write(f"- **처리 전:** {raw_df.shape[0]}행 ➔ **처리 후:** {clean_df.shape[0]}행")
    st.dataframe(clean_df.style.format({"명목_GDP_억불": "{:,.0f}", "1인당_GDP_달러": "{:,.0f}", "행복_점수": "{:.3f}"}))


# --- [체크리스트 2: 제목과 축 이름이 있는 그래프] ---
st.header("2. 탐색적 데이터 분석 (산점도 그래프)")

fig = px.scatter(
    clean_df, 
    x="1인당_GDP_달러", 
    y="행복_점수", 
    text="국가",
    size="명목_GDP_억불",
    title="[그림 1] 1인당 GDP와 행복도 점수의 상관관계 (2026년 상위 12개국)",
    labels={"1인당_GDP_달러": "1인당 명목 GDP (USD)", "행복_점수": "행복도 점수 (10점 만점)"}
)
fig.update_traces(textposition='top center', marker=dict(color='royalblue', opacity=0.7))
fig.update_layout(xaxis_tickformat=',', height=500)

st.plotly_chart(fig, use_container_width=True)


# --- [체크리스트 3 & 5: 근거 수치와 함께 말하기 & 처음 예상과 다르게 나온 점] ---
st.header("3. 그래프 분석 결과 및 다음 계획 (★발표 대본)")

st.info("""
**[그래프에서 찾아낸 것 (수치 근거)]**  
그래프를 보면 우상향하는 기본 추세는 있지만, 완벽하게 비례하지는 않습니다.  
예를 들어, **대한민국**은 1인당 GDP가 **43,512달러**로 매우 높지만 행복 점수는 **6.040점**에 불과합니다.  
반면, **브라질**은 1인당 GDP가 **12,397달러**로 한국의 3분의 1 수준에도 못 미치지만, 행복 점수는 **6.634점**으로 한국보다 훨씬 높게 나타났습니다.
""")

st.warning("""
**[처음 예상과 다르게 나온 점 및 다음 분석에서 확인할 점]**  
처음에는 **'돈이 많을수록 무조건 더 행복할 것'**이라고 예상했습니다.  
하지만 브라질과 한국의 사례처럼 경제력만으로는 설명되지 않는 예외 그룹이 존재함을 확인했습니다.  
따라서 다음 분석에서는 **'사회적 지원'** 같은 비경제적 요인을 변수로 추가하여, **군집 분석(Clustering)**을 통해 국가들이 어떻게 묶이는지 더 깊이 확인해 보겠습니다.
""")
