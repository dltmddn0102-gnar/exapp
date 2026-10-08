# exapp.py
# 실습 과제

# 로컬 실행
# python -m streamlit run ./desktop/webservice/day31/exapp/exapp.py

# Render Cloud 실행
# streamlit run app.py --server.address 0.0.0.0 --server.port $PORT

import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

APP_GREETING = os.getenv('APP_GREETING')
APP_TITLE = os.getenv('APP_TITLE')

st.set_page_config(
    page_title= f'{APP_TITLE} 배포 실습 과제',
    page_icon= '✏',
    layout= 'centered'
)

st.title(f'{APP_TITLE} 배포 실습 과제')
st.write(f'{APP_GREETING} 환영합니다!')

st.divider()

st.subheader('간단한 UI만들기')

season = st.text_input(f'{APP_TITLE} 기수를 입력해주세요', placeholder='예) 9기')

if st.button('확인', type='primary'):
    if season.strip():
        st.success(f'{APP_GREETING}, {APP_TITLE} {season.strip()} 수업에 오신 것을 환영합니다.')
    else:
        st.warning('기수를 먼저 입력해 주세요!')

st.divider()

st.subheader('환경변수 설정 확인')

if os.getenv('APP_GREETING', 'APP_TITLE'):
    st.success('APP_GREETING와 APP_TITLE 환경변수를 성공적으로 읽었습니다!')
    st.write(f'현재 인사말 설정 값: {APP_GREETING}, {APP_TITLE}')
else:
    st.info('환경변수가 설정되지 않아 기본값을 사용 중입니다!')
















