import streamlit as st
import openai

# OpenAI API 키 불러오기 (Streamlit secrets 사용)
openai.api_key = st.secrets["openai"]["api_key"]

# Streamlit 페이지 기본 설정
st.set_page_config(page_title="수학 개념 챗봇", page_icon="🧮")
st.title("🧮 수학 개념 챗봇")
st.write("모르는 수학 개념을 물어보면 친절하게 설명해줄게요!")

# 대화 히스토리 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "당신은 엄격하고 무서운 수학 선생님입니다. 학생이 모르는 수학 개념을 물어보면, 공부를 열심히 하라고 따끔하게 훈계하면서 설명해주세요."}
    ]

# 사용자 입력
user_input = st.text_input("❓ 궁금한 수학 개념을 입력해 보세요:", key="user_input")

if st.button("질문하기") and user_input:
    # 대화 히스토리에 사용자 메시지 추가
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # GPT 응답 요청
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=st.session_state.chat_history,
        temperature=0.7
    )

    bot_reply = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# 대화 내용 출력
for msg in st.session_state.chat_history[1:]:  # system 메시지는 제외
    if msg["role"] == "user":
        st.markdown(f"🧑‍🎓 **질문:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"📘 **챗봇:** {msg['content']}")
