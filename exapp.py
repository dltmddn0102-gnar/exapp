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
if 'completed_list' not in st.session_state:
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
        placeholder='이름을 입력하세요.',
        key='input_name'
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

# 리스트를 요일/시간 순으로 미리 정렬
st.session_state.consult_list = sorted(
    st.session_state.consult_list,
    key=lambda x: (date_order.get(x['date'], 99), time_order.get(x['time'], 99))
)
st.session_state.completed_list = sorted(
    st.session_state.completed_list,
    key=lambda x: (date_order.get(x['date'], 99), time_order.get(x['time'], 99))
)

# 3. 상담 신청 목록 섹션
st.subheader('상담 신청 목록')

if st.session_state.consult_list:
    search_req = st.text_input('🔍 신청 목록 이름 검색', placeholder='검색할 이름을 입력하세요.', key='search_req')

    # 누적 횟수를 실시간 계산하기 위한 딕셔너리 카운터
    run_count = {}

    display_index = 1
    for orig_idx, item in enumerate(st.session_state.consult_list):
        key_pair = (item['season'], item['name'])
        # 처음 등장하면 1회, 이후 등장할 때마다 +1 증가
        run_count[key_pair] = run_count.get(key_pair, 0) + 1
        current_nth = run_count[key_pair]

        # 검색 필터링 (화면 출력만 제어하고, 차수 카운트는 유지하여 정합성 보존)
        if search_req.strip() and search_req.strip() not in item['name']:
            continue

        col1, col2, col3 = st.columns([0.70, 0.15, 0.15])

        with col1:
            st.write(
                f'{display_index}. '
                f'{APP_TITLE} 기수: {item["season"]} | '
                f'이름: {item["name"]} **({current_nth}회)** | '
                f'**{item["date"]}** | '
                f'**{item["time"]}**'
            )
        with col2:
            if st.button('완료', key=f'complete_{orig_idx}'):
                completed_item = st.session_state.consult_list.pop(orig_idx)
                st.session_state.completed_list.append(completed_item)
                st.success(f'{item["name"]}님의 상담이 완료 처리되었습니다.')
                st.rerun()
        with col3:
            if st.button('취소', key=f'cancel_{orig_idx}'):
                st.session_state.consult_list.pop(orig_idx)
                st.success('신청이 취소되었습니다.')
                st.rerun()
        display_index += 1

    if display_index == 1 and search_req.strip():
        st.info('검색 결과와 일치하는 신청 내역이 없습니다.')
else:
    st.info('아직 상담 신청 내역이 없습니다.')

st.divider()

# 4. 상담 완료 목록 섹션
st.subheader('✅ 상담 완료 목록')

if st.session_state.completed_list:
    search_comp = st.text_input('🔍 완료 목록 이름 검색', placeholder='검색할 이름을 입력하세요.', key='search_comp')

    # 완료 목록용 개별 카운터
    run_count_c = {}

    display_index_c = 1
    for orig_idx_c, item in enumerate(st.session_state.completed_list):
        key_pair_c = (item['season'], item['name'])
        run_count_c[key_pair_c] = run_count_c.get(key_pair_c, 0) + 1
        current_nth_c = run_count_c[key_pair_c]

        if search_comp.strip() and search_comp.strip() not in item['name']:
            continue

        col_c1, col_c2 = st.columns([0.85, 0.15])

        with col_c1:
            st.write(
                f'{display_index_c}. '
                f'[{APP_TITLE} {item["season"]}] {item["name"]}님 **({current_nth_c}회)** '
                f'({item["date"]} / {item["time"]}) - 완료됨'
            )
        with col_c2:
            if st.button('삭제', key=f'delete_done_{orig_idx_c}'):
                st.session_state.completed_list.pop(orig_idx_c)
                st.success('완료 내역이 삭제되었습니다.')
                st.rerun()
        display_index_c += 1

    if display_index_c == 1 and search_comp.strip():
        st.info('검색 결과와 일치하는 완료 내역이 없습니다.')
else:
    st.info('완료된 상담 내역이 없습니다.')

st.divider()

st.subheader('환경변수 설정 확인')
if APP_GREETING and APP_TITLE:
    st.success('APP_GREETING와 APP_TITLE environment 변수를 성공적으로 읽었습니다!')
    st.write(f'현재 환경변수 설정 값: {APP_GREETING}, {APP_TITLE}')
else:
    st.info('환경변수가 설정되지 않았습니다.')
