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

# 세션 상태 초기화
if 'consult_list' not in st.session_state:
    st.session_state.consult_list = []
if 'completed_list' not in st.session_state:  # 상담 완료 목록 저장 공간 추가
    st.session_state.completed_list = []
if 'verified' not in st.session_state:
    st.session_state.verified = False
if 'current_season' not in st.session_state:
    st.session_state.current_season = ""

# 1. 기수 입력 섹션
season = st.text_input(
    f'{APP_TITLE} 기수를 입력해주세요',
    placeholder='예) 9기',
    key='season'
)

if st.button('확인', type='primary'):
    if season.strip():
        st.session_state.verified = True
        st.session_state.current_season = season.strip()
        st.success(f'{APP_GREETING}, {APP_TITLE} {season.strip()} 수업에 오신 것을 환영합니다.')
    else:
        st.session_state.verified = False
        st.warning('기수를 먼저 입력해 주세요!')

st.divider()

# 2. 상담 신청 폼 섹션 (기수 확인 버튼을 눌러 인증된 경우에만 활성화)
if st.session_state.verified:
    st.info(f"현재 입력된 기수: **{st.session_state.current_season}** (기수를 변경하려면 위에서 다시 입력 후 확인을 눌러주세요.)")

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
            consult_item = {
                'season': st.session_state.current_season,
                'name': name.strip(),
                'date': date,
                'time': time
            }
            st.session_state.consult_list.append(consult_item)
            st.success('상담 신청이 접수되었습니다.')
            st.rerun()
        else:
            st.warning('이름을 입력하세요!')
else:
    st.warning('⚠️ 상단의 기수 입력창에 기수를 입력하고 [확인] 버튼을 눌러야 상담 신청이 가능합니다.')

st.divider()

# 정렬을 위한 가중치 정의
date_order = {'월요일': 1, '화요일': 2, '수요일': 3, '목요일': 4, '금요일': 5, '토요일': 6, '일요일': 7}
time_order = {'오전': 1, '오후': 2, '저녁': 3}

# 3. 상담 신청 목록 섹션 (취소 / 완료 버튼 배치)
st.subheader('상담 신청 목록')

if st.session_state.consult_list:
    # 요일 순 정렬 후, 같은 요일 내에서 시간 순으로 정렬
    st.session_state.consult_list = sorted(
        st.session_state.consult_list,
        key=lambda x: (date_order.get(x['date'], 99), time_order.get(x['time'], 99))
    )

    # 내용(70%), 완료 버튼(15%), 취소 버튼(15%) 비율 분할
    for i, item in enumerate(st.session_state.consult_list, start=1):
        col1, col2, col3 = st.columns([0.70, 0.15, 0.15])

        with col1:
            st.write(
                f'{i}. '
                f'{APP_TITLE} 기수: {item["season"]} | '
                f'이름: {item["name"]} | '
                f'**{item["date"]}** | '
                f'**{item["time"]}**'
            )
        with col2:
            if st.button('완료', key=f'complete_{i}'):
                # 신청 목록에서 꺼내어 완료 목록에 추가
                completed_item = st.session_state.consult_list.pop(i - 1)
                st.session_state.completed_list.append(completed_item)
                st.success(f'{item["name"]}님의 상담이 완료 처리되었습니다.')
                st.rerun()
        with col3:
            if st.button('취소', key=f'cancel_{i}'):
                st.session_state.consult_list.pop(i - 1)
                st.success('신청이 취소되었습니다.')
                st.rerun()
else:
    st.info('아직 상담 신청 내역이 없습니다.')

st.divider()

# 4. 상담 완료 목록 섹션 (요청하신 기능 추가)
st.subheader('✅ 상담 완료 목록')

if st.session_state.completed_list:
    # 완료 목록도 가독성을 위해 요일/시간 순 정렬
    st.session_state.completed_list = sorted(
        st.session_state.completed_list,
        key=lambda x: (date_order.get(x['date'], 99), time_order.get(x['time'], 99))
    )

    # 내용(85%), 삭제 버튼(15%) 비율 분할
    for j, item in enumerate(st.session_state.completed_list, start=1):
        col_c1, col_c2 = st.columns([0.85, 0.15])

        with col_c1:
            st.write(
                f'{j}. '
                f'[{APP_TITLE} {item["season"]}] {item["name"]}님 '
                f'({item["date"]} / {item["time"]}) - 완료됨'
            )
        with col_c2:
            if st.button('삭제', key=f'delete_done_{j}'):
                st.session_state.completed_list.pop(j - 1)
                st.success('완료 내역이 삭제되었습니다.')
                st.rerun()
else:
    st.info('완료된 상담 내역이 없습니다.')

st.divider()

st.subheader('환경변수 설정 확인')
if APP_GREETING and APP_TITLE:
    st.success('APP_GREETING와 APP_TITLE 환경변수를 성공적으로 읽었습니다!')
    st.write(f'현재 환경변수 설정 값: {APP_GREETING}, {APP_TITLE}')
else:
    st.info('환경변수가 설정되지 않았습니다.')
