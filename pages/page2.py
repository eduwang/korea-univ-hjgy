import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import matplotlib
import platform

# ✅ 한글 폰트 수동 등록 (Linux: GitHub Codespaces 포함)
if platform.system() == "Linux":
    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    font_prop = fm.FontProperties(fname=font_path)
else:
    # Windows or macOS (시스템 기본 폰트)
    font_prop = None
    if platform.system() == "Windows":
        matplotlib.rc('font', family='Malgun Gothic')
    elif platform.system() == "Darwin":
        matplotlib.rc('font', family='AppleGothic')

matplotlib.rc('axes', unicode_minus=False)

# ✅ Streamlit UI 설정
st.set_page_config(page_title="📊 성적 분석 대시보드", layout="wide")
st.title("📊 학생 성적 분석 Web App")

# 현재 폰트 상태 출력 (디버깅용)
if font_prop:
    st.write(f"✅ 현재 사용 중인 폰트: {font_prop.get_name()}")

# ✅ CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "이름" not in df.columns:
        st.error("❗ CSV 파일에 '이름' 열이 포함되어야 합니다.")
    else:
        subjects = [col for col in df.columns if col != "이름"]

        # 1️⃣ 학생별 평균 성적
        st.subheader("1️⃣ 학생별 평균 성적")
        df["평균"] = df[subjects].mean(axis=1)
        st.dataframe(df[["이름", "평균"]].sort_values("평균", ascending=False))

        # 2️⃣ 과목별 성적 분포 (히스토그램)
        st.subheader("2️⃣ 과목별 성적 분포 (히스토그램)")
        for subject in subjects:
            fig, ax = plt.subplots()
            sns.histplot(df[subject], bins=10, kde=True, ax=ax)
            if font_prop:
                ax.set_title(f"{subject} 성적 분포", fontproperties=font_prop)
                ax.set_xlabel("점수", fontproperties=font_prop)
                ax.set_ylabel("학생 수", fontproperties=font_prop)
            else:
                ax.set_title(f"{subject} 성적 분포")
                ax.set_xlabel("점수")
                ax.set_ylabel("학생 수")
            st.pyplot(fig)

        # 3️⃣ 과목별 성적 상자그림 (Boxplot)
        st.subheader("3️⃣ 과목별 성적 상자그림 (Boxplot)")
        melted_df = df.melt(id_vars="이름", value_vars=subjects, var_name="과목", value_name="점수")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(x="과목", y="점수", data=melted_df, ax=ax)
        if font_prop:
            ax.set_title("과목별 성적 상자그림", fontproperties=font_prop)
            ax.set_xlabel("과목", fontproperties=font_prop)
            ax.set_ylabel("점수", fontproperties=font_prop)
        else:
            ax.set_title("과목별 성적 상자그림")
            ax.set_xlabel("과목")
            ax.set_ylabel("점수")
        st.pyplot(fig)
else:
    st.info("👆 위에 성적 CSV 파일을 업로드해 주세요.")
