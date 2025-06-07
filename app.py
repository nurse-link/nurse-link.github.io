import streamlit as st

# ----------------- 데이터 정의 (status 필드 추가) -----------------
patients = [
    {
        "bed": "11호", "name": "김○○", "info": "XX세/남", "favorite": False,
        "requests": [
            {"time": "05월30일 14:20", "type": "진단서", "emergency": False, "status": "default"}
        ]
    },
    {
        "bed": "11호", "name": "이○○", "info": "XX세/남", "favorite": False,
        "requests": []
    },
    {
        "bed": "12호", "name": "정○○", "info": "XX세/여", "favorite": True,
        "requests": [
            {"time": "05월30일 13:50", "type": "진단서", "emergency": False, "status": "default"},
            {"time": "05월30일 13:45", "type": "통증", "emergency": True, "status": "default"},
            {"time": "05월30일 13:30", "type": "체위변경", "emergency": False, "status": "default"},
        ]
    }
]

# ----------------- 세션 상태 초기화 -----------------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None
if "patients_data" not in st.session_state:
    # deepcopy로 해야 실제 데이터와 분리됨
    import copy
    st.session_state.patients_data = copy.deepcopy(patients)

params = st.query_params

# ----------------- CSS -----------------
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        max-width: 430px !important;
        margin: 0 auto;
        font-size: 16px;
        background: #e3f2fd;
    }
    [data-testid="stHeader"] { display: none; }
    .star {
        position: absolute;
        left: 12px;
        top: 18px;
        font-size: 1.28em;
        z-index: 2;
        user-select: none;
    }
    .card {
        border-radius:13px;
        padding:14px 10px 14px 38px;
        margin-bottom:16px;
        font-size:1.07em;
        color:#222;
        position: relative;
        width: 98%;
        min-width: 140px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        background: #ECECEC;
        border: none;
        outline: none;
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: background 0.15s;
        overflow: hidden;
        min-height: 72px;
        max-height: 72px;
        line-height: 1.22em;
    }
    .card-emergency {
        background: #FFCDD2 !important;
    }
    .card-yellow {
        background: #FFF9C4 !important;
    }
    .card-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 0px;
        line-height: 1.16em;
    }
    .bed-line {
        font-size:1.13em; font-weight:600; margin-bottom:0px; line-height:1.1em;
    }
    .name-line {
        font-size:1.05em; margin-top:0px; line-height:1.1em;
    }
    .card:hover {
        filter: brightness(0.97);
    }
    .click-overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent;
        border: none;
        cursor: pointer;
        z-index: 10;
        padding: 0;
    }
    .badge {
        position: absolute;
        top: 18px;
        right: 14px;
        background: #E53935;
        color: #fff;
        border-radius: 50%;
        min-width: 28px;
        min-height: 28px;
        font-size: 1.01em;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 7px;
        z-index: 20;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        border: 2px solid #fff;
        letter-spacing: 1px;
    }
    .req-row {
        display: flex;
        align-items: stretch;
        margin-bottom: 16px;
        width: 98%;
        min-height: 72px;
        max-height: 72px;
        position: relative;
    }
    .req-btn-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: stretch;
        height: 72px;
        margin-left: 10px;
        gap: 6px;
        position: relative;
        z-index: 1;
    }
    .req-btn {
        border-radius: 11px;
        font-weight: 600;
        font-size: 1.01em;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 70px;
        height: 32px;
        margin: 0;
        padding: 0;
        border: none;
        outline: none;
        user-select: none;
        cursor: pointer;
    }
    .req-btn-complete {
        background-color: #757575;
        color: #fff;
        margin-bottom: 6px;
    }
    .req-btn-alarm {
        background-color: #FFD600;
        color: #222;
        flex-direction: column;
        font-size: 0.99em;
    }
    .req-btn-alarm span {
        display: block;
        width: 100%;
        text-align: center;
        line-height: 1.2em;
    }
    .req-btn-disabled {
        opacity: 0.6;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- 로그인 화면 ----------------
if st.session_state.page == "login":
    st.markdown(
        """
        <div style="height:40px;"></div>
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <h2 style="margin-bottom:28px; font-size:1.5em;">로그인</h2>
        </div>
        """, unsafe_allow_html=True
    )
    id_val = st.text_input("아이디를 입력하세요", key="id_input")
    pw_val = st.text_input("비밀번호를 입력하세요", type="password", key="pw_input")
    if st.button("확인"):
        st.session_state.page = "patient_list"
        st.rerun()

# ---------------- 환자리스트(재원환자) 화면 ----------------
elif st.session_state.page == "patient_list":
    if st.button("← 뒤로가기"):
        st.session_state.page = "login"
        st.rerun()
    st.markdown(
        '<div style="padding: 10px 0 6px 0;"><div style="font-size: 1.5em; font-weight: 600; color: #222;">12 병동<br>담당간호사: 김ㅇㅇ<br>환자리스트</div></div>',
        unsafe_allow_html=True
    )
    sort_options = ["침상 위치 순", "응급 요청 순", "최근 요청 순", "즐겨찾기 순"]
    sort_selected = st.selectbox(
        "", sort_options, key="sort_patients", label_visibility="collapsed"
    )
    def sort_patients_func(patients, option):
        if option == "침상 위치 순":
            return sorted(patients, key=lambda x: x["bed"])
        elif option == "응급 요청 순":
            return sorted(patients, key=lambda x: not any(r.get("emergency") for r in x["requests"]))
        elif option == "최근 요청 순":
            return patients[::-1]
        elif option == "즐겨찾기 순":
            return sorted(patients, key=lambda x: not x["favorite"])
        return patients
    sorted_patients = sort_patients_func(st.session_state.patients_data, sort_selected)
    with st.container(height=430):
        for idx, p in enumerate(sorted_patients):
            star_color = "#FFD600" if p["favorite"] else "#BDBDBD"
            star_icon = "⭐" if p["favorite"] else "☆"
            is_emergency = any(r.get("emergency") for r in p["requests"])
            card_class = "card card-emergency" if is_emergency else "card"
            # 완료된 요청은 카운트에서 제외
            req_count = len([r for r in p["requests"] if r.get("status", "default") != "finished"])
            badge_html = f'<span class="badge">{req_count}</span>' if req_count > 0 else ""
            st.markdown(
                f'''<div class="{card_class}" style="position:relative;">
                    <span class="star" style="color:{star_color};">{star_icon}</span>
                    <div class="card-content">
                        <span class="bed-line">{p['bed']}</span>
                        <span class="name-line">{p['name']}({p['info']})</span>
                    </div>{badge_html}
                    <form method="get" action="">
                        <button name="select_patient" value="{st.session_state.patients_data.index(p)}" class="click-overlay" type="submit" aria-label="환자 선택" style="background:none; border:none; width:100%; height:100%; cursor:pointer; padding:0;"></button>
                    </form>
                </div>''',
                unsafe_allow_html=True
            )
        st.markdown(
            '<div style="font-size:1.05em; margin-top:10px; color:#222; text-align:center;">마지막 환자입니다.</div>',
            unsafe_allow_html=True
        )

# ---------------- 요청리스트 화면 ----------------
elif st.session_state.page == "request_list":
    if st.button("← 뒤로가기"):
        st.session_state.page = "patient_list"
        st.query_params.clear()
        st.rerun()
    idx = st.session_state.selected_patient
    patient = st.session_state.patients_data[idx]
    star_color = "#FFD600" if patient["favorite"] else "#BDBDBD"
    star_icon = "⭐" if patient["favorite"] else "☆"
    st.markdown(
        f"""
        <div style="background:#e3f2fd;padding:18px 0 6px 30px; position:relative;">
            <span class="star" style="left:0px;top:18px;color:{star_color};font-size:1.5em;position:absolute;">{star_icon}</span>
            <span style="font-size:1.5em;font-weight:700;">{patient['bed']}</span><br>
            <span style="font-size:1.5em;font-weight:600;">{patient['name']}({patient['info']})</span><br>
            <span style="font-size:1.5em;font-weight:700;">요청리스트</span>
        </div>
        """, unsafe_allow_html=True
    )
    sort_options = ["최근 요청 순", "응급 요청 순"]
    sort_selected = st.selectbox(
        "", sort_options, key="req_sort", label_visibility="collapsed"
    )
    def sort_requests(requests, option):
        if option == "응급 요청 순":
            return sorted(requests, key=lambda x: not x["emergency"])
        return requests

    req_indices = list(range(len(patient["requests"])))
    sorted_requests = [patient["requests"][i] for i in req_indices]
    sorted_requests = sort_requests(sorted_requests, sort_selected)

    with st.container(height=430):
        # 완료(finished)된 요청은 표시하지 않음
        visible_requests = [r for r in sorted_requests if r.get("status", "default") != "finished"]
        if not visible_requests:
            st.markdown(
                '<div style="text-align:center;font-size:1.07em;color:#888;margin:18px 0 8px 0;">요청이 없습니다</div>',
                unsafe_allow_html=True
            )
        else:
            for order, req in enumerate(visible_requests):
                # 카드 색상 결정
                card_class = "card"
                if req.get("emergency"):
                    card_class += " card-emergency"
                elif req.get("status") == "remind":
                    card_class += " card-yellow"

                st.markdown(
                    f'''
                    <div class="req-row" style="position:relative;">
                        <div class="{card_class}" style="flex:2;min-width:0;display:flex;flex-direction:column;justify-content:center;position:relative;">
                            <span style="font-size:0.98em;">{req['time']}</span>
                            <b style="font-weight:700;">{req['type']}</b>
                        </div>
                    ''',
                    unsafe_allow_html=True
                )
                # 버튼 구현
                col_spacer, col0, col1, col2 = st.columns([0.4, 0.8, 0.6, 1])
                with col0:
                    if req["type"] == "통증":
                        if st.button("상세정보", key=f"pain_detail_{order}"):
                            st.session_state.pain_request_patient_idx = st.session_state.selected_patient
                            st.session_state.pain_request_info = req
                            st.session_state.page = "pain_request"
                            st.rerun()
                with col1:
                    if st.button("완료", key=f"complete_{order}"):
                        req["status"] = "finished"
                        st.rerun()
                with col2:
                    if req.get("status") != "remind":
                        if st.button("10분 뒤 알림", key=f"remind_{order}"):
                            req["status"] = "remind"
                            st.rerun()
                    else:
                        st.markdown('<div style="background:#FFD600;color:#222;border-radius:11px;text-align:center;">알림 예약됨</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:1.07em; margin-top:8px; color:#222; text-align:center;">마지막 요청입니다.</div>',
                unsafe_allow_html=True
            )

# ------------------ 통증 요청 화면 ------------------
elif st.session_state.page == "pain_request":
    patient_idx = st.session_state.pain_request_patient_idx
    req = st.session_state.pain_request_info
    patient = st.session_state.patients_data[patient_idx]
    # 헤더: 뒤로가기, 별모양, bed, name, info
    back = st.button("← 뒤로가기")
    if back:
        st.session_state.page = "request_list"
        st.rerun()
    star_color = "#FFD600" if patient["favorite"] else "#BDBDBD"
    star_icon = "⭐" if patient["favorite"] else "☆"
    st.markdown(
        f"""
        <div style="background:#e3f2fd;padding:18px 0 6px 30px; position:relative;">
            <span class="star" style="left:0px;top:18px;color:{star_color};font-size:1.5em;position:absolute;">{star_icon}</span>
            <span style="font-size:1.5em;font-weight:700;">{patient['bed']}</span><br>
            <span style="font-size:1.5em;font-weight:600;">{patient['name']}({patient['info']})</span>
        </div>
        """, unsafe_allow_html=True
    )

    # 통증 요청 상세 정보
    st.markdown(f"""
    <div style="padding:18px 0 0 30px;">
        <b><span style="font-size:1.5em;font-weight:600;">{req['time']}</span><br>
        <b>통증 부위:</b> 배<br>
        <b>통증 강도:</b> 5/10<br>
        <b>통증 양상:</b> 찌르듯이
    </div>
    """, unsafe_allow_html=True)
    st.stop()

    st.image("pain.png", use_column_width=True)

# 쿼리파라미터 감지 및 페이지 전환
if params.get("select_patient"):
    st.session_state.selected_patient = int(params["select_patient"])
    st.session_state.page = "request_list"
    st.query_params.clear()
    st.rerun()

