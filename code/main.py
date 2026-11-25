import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 기본 페이지 설정
st.set_page_config(page_title="경제력과 행복도 분석", layout="wide")
st.title("📊 국가의 행복도는 경제력으로 나뉘는가?")

# 2. 데이터 구축
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
# 결측치 처리 (빈칸 삭제)
clean_df = raw_df.dropna(subset=["1인당_GDP_달러", "행복_점수"]).copy()

# --- [1단계: 데이터 개요] ---
st.header("1. 데이터 개요 및 결측치 처리")
with st.expander("데이터프레임 확인하기"):
    st.write(f"원본 데이터: {raw_df.shape[0]}행 ➔ 전처리 후 데이터: {clean_df.shape[0]}행")
    st.dataframe(clean_df.style.format({"명목_GDP_억불": "{:,.0f}", "1인당_GDP_달러": "{:,.0f}", "행복_점수": "{:.3f}"}))


# --- [2단계: 개별 지표 분석 (GDP 따로, 행복도 따로)] ---
st.header("2. 국가별 1인당 GDP 및 행복도 개별 분석")
col1, col2 = st.columns(2)

with col1:
    # 1인당 GDP 막대 그래프 (내림차순 정렬)
    df_gdp = clean_df.sort_values(by="1인당_GDP_달러", ascending=True)
    fig_gdp = px.bar(
        df_gdp, 
        x="1인당_GDP_달러", 
        y="국가", 
        orientation='h', 
        title="[그림 1] 국가별 1인당 명목 GDP 순위", 
        color="1인당_GDP_달러", 
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_gdp, use_container_width=True)

with col2:
    # 행복도 막대 그래프 (내림차순 정렬)
    df_happy = clean_df.sort_values(by="행복_점수", ascending=True)
    fig_happy = px.bar(
        df_happy, 
        x="행복_점수", 
        y="국가", 
        orientation='h', 
        title="[그림 2] 국가별 행복도 점수 순위", 
        color="행복_점수", 
        color_continuous_scale="Greens"
    )
    # 점수 차이를 잘 보이게 하기 위해 X축 범위를 4~8로 설정
    fig_happy.update_xaxes(range=[4, 7.5]) 
    st.plotly_chart(fig_happy, use_container_width=True)


# --- [3단계: 종합 비교 (상관관계 산점도)] ---
st.header("3. 1인당 GDP와 행복도의 종합 상관관계 (비교)")

# GDP와 행복도를 한 번에 띄워서 비교하는 산점도
fig_scatter = px.scatter(
    clean_df, 
    x="1인당_GDP_달러", 
    y="행복_점수", 
    text="국가",
    size="명목_GDP_억불",
    title="[그림 3] 1인당 GDP와 행복도 점수 비교 산점도 (원 크기는 전체 GDP)",
    labels={"1인당_GDP_달러": "1인당 명목 GDP (USD)", "행복_점수": "행복도 점수 (10점 만점)"}
)
fig_scatter.update_traces(textposition='top center', marker=dict(color='royalblue', opacity=0.7))
fig_scatter.update_layout(xaxis_tickformat=',', height=600)

st.plotly_chart(fig_scatter, use_container_width=True)

