import streamlit as st
import random

st.title("🪙 동전 던지기 시뮬레이션")

# 슬라이더: 동전 개수 조절
num_coins = st.slider("동전 개수 선택", min_value=1, max_value=100, value=10)

# 버튼: 던지기
if st.button("던지기!"):
    results = [random.choice(["H", "T"]) for _ in range(num_coins)]
    
    # 결과 표시
    st.subheader("결과:")
    st.write(" ".join(results))
