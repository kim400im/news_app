# pip install streamlit
# streamlit run streamlit_practice.py

import streamlit as st

st.title("첫 번째 데모")
st.header("헤더입니다")
st.subheader("서브 헤더입니다")
st.text("텍스트입니다")

st.markdown("**마크다운 문법 적용**")
st.code('print("hello")', language='python')

name = st.text_input("이름을 입력하시오")
age = st.number_input("나이를 입력하시오: ", min_value=0, max_value=120)

st.write("이름: ", name)
st.write("나이: ", age)

if st.button("확인 버튼"):
    st.write("확인되셨습니다.")
else:
    st.write("취소되셨습니다")