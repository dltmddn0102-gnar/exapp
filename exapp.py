# exapp.py

import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

APP_GREETING = os.getenv('APP_GREETING')
APP_TITLE = os.getenv('APP_TITLE')

st.set_page_config(
    page_title=f'{APP_TITLE} 배포 실습 과제',
    page_icon='✏',
    layout='centered'
)

st.title(f'{APP_TITLE} 배포 실습 과제')
st.write(f'{APP_GREETING} 환영합니다!')

st.divider()

st.subheader('상담 리스트')

if 'list' not in st.session_state:
    st.session_state.list = []

season = st.text_input(
    f'{APP_TITLE} 기수를 입력해주세요',
    placeholder='예) 9기',
    key='season'
)


if st.button('확인', type='primary'):
    if season.strip():
        st.success(
            f'{APP_GREETING}, {APP_TITLE} {season.strip()} 수업에 오신 것을 환영합니다.'
        )
    else:
        st.warning('기수를 먼저 입력해 주세요!')

date = st.selectbox(
    '희망 요일',
    ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
)

name = st.text_input(
    '이름',
    placeholder='이름을 입력하세요.'
)

time = st.radio(
    '상담 희망 시간',
    ['오전', '오후', '저녁']
)

if st.button('신청'):

    if name.strip():

        list = {
            'season': season,
            'name': name,
            'date': date,
            'time': time
        }

        st.session_state.list.append(list)
        st.success('상담 신청이 접수되었습니다.')
    else:
        st.warning('이름을 입력하세요!')

st.divider()

st.subheader('상담 신청 목록')

if st.session_state.list:
    for i, list in enumerate(
        st.session_state.list,
        start=1
    ):
        st.write(
            f'{i}. '
            f'{APP_TITLE}기수: {list["season"]} | '
            f'이름: {list["name"]} | '
            f'희망 요일: {list["date"]} | '
            f'상담 시간: {list["time"]}'
        )

else:
    st.info('아직 상담 신청 내역이 없습니다.')

st.divider()

st.subheader('환경변수 설정 확인')

if APP_GREETING and APP_TITLE:
    st.success('APP_GREETING와 APP_TITLE 환경변수를 성공적으로 읽었습니다!')
    st.write(f'현재 환경변수 설정 값: {APP_GREETING}, {APP_TITLE}')

else:
    st.info('환경변수가 설정되지 않았습니다.')