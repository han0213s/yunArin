import streamlit as st
from models.player import Player
from models.room import Room
from models.item import get_preset_item
from models.game_state import GameState

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="ORBIT-13",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
# 스타일
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
    background-color: #080c14;
    color: #c8d8e8;
}

/* 전체 배경 */
.stApp {
    background: #080c14;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(0,60,120,0.15) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(0,100,80,0.1) 0%, transparent 50%);
}

/* 헤더 */
.orbit-header {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #3a7abf;
    text-transform: uppercase;
    margin-bottom: 2px;
}

/* 카드 */
.card {
    background: rgba(10, 20, 35, 0.85);
    border: 1px solid rgba(0, 120, 200, 0.2);
    border-radius: 4px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.card-danger {
    border-color: rgba(200, 50, 50, 0.4);
    background: rgba(30, 8, 8, 0.85);
}
.card-success {
    border-color: rgba(0, 180, 120, 0.3);
    background: rgba(0, 20, 15, 0.85);
}

/* HP 바 */
.hp-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 2px;
    height: 8px;
    width: 100%;
    overflow: hidden;
}
.hp-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.5s ease;
}

/* 배지 */
.role-badge {
    display: inline-block;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    padding: 2px 10px;
    border-radius: 2px;
    text-transform: uppercase;
}
.badge-Engineer { background: rgba(0,100,200,0.25); color:#5aadff; border:1px solid rgba(0,100,200,0.4); }
.badge-Hacker   { background: rgba(0,200,80,0.15);  color:#40e080; border:1px solid rgba(0,200,80,0.3); }
.badge-Soldier  { background: rgba(200,60,0,0.2);   color:#ff8040; border:1px solid rgba(200,60,0,0.4); }
.badge-Medic    { background: rgba(0,180,180,0.15); color:#40e0e0; border:1px solid rgba(0,180,180,0.3); }

/* 상태 수치 */
.stat-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    color: #3a7abf;
    text-transform: uppercase;
}
.stat-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 22px;
    font-weight: bold;
    color: #e0f0ff;
}

/* 아이템 태그 */
.item-tag {
    display: inline-block;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    padding: 3px 8px;
    margin: 2px;
    border-radius: 2px;
    background: rgba(0,80,160,0.2);
    border: 1px solid rgba(0,100,200,0.25);
    color: #7ab8e8;
}
.item-clue  { background: rgba(140,80,0,0.2); border-color:rgba(200,120,0,0.3); color:#f0a040; }
.item-key   { background: rgba(100,0,140,0.2); border-color:rgba(160,0,200,0.3); color:#c060f0; }
.item-weapon{ background: rgba(140,0,0,0.2); border-color:rgba(200,0,0,0.3); color:#f06060; }

/* 플레이어 행 */
.player-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

/* 채팅 메시지 */
.msg-gm   { color:#5aadff; font-family:'Share Tech Mono',monospace; font-size:13px; }
.msg-player{color:#c8d8e8; font-size:13px; }
.msg-echo { color:#40e080; font-family:'Share Tech Mono',monospace; font-size:13px; font-style:italic; }

/* 버튼 오버라이드 */
.stButton > button {
    background: rgba(0,60,120,0.4) !important;
    border: 1px solid rgba(0,120,200,0.4) !important;
    color: #7ab8e8 !important;
    border-radius: 3px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(0,80,160,0.6) !important;
    border-color: rgba(0,160,255,0.6) !important;
    color: #c8e8ff !important;
}

/* 입력창 */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(0,20,40,0.8) !important;
    border: 1px solid rgba(0,100,180,0.3) !important;
    color: #c8d8e8 !important;
    border-radius: 3px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* 구분선 */
hr { border-color: rgba(0,100,200,0.15) !important; }

/* 탭 */
.stTabs [data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    color: #3a7abf !important;
}
.stTabs [aria-selected="true"] {
    color: #5aadff !important;
    border-bottom-color: #5aadff !important;
}

/* 경고 숨기기 */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 세션 초기화 헬퍼
# ─────────────────────────────────────────
def init_session():
    if "room" not in st.session_state:
        st.session_state.room = None
    if "player" not in st.session_state:
        st.session_state.player = None
    if "page" not in st.session_state:
        st.session_state.page = "lobby"   # lobby | setup | game
    if "game_state" not in st.session_state:
        st.session_state.game_state = GameState().to_dict()


def get_room() -> Room | None:
    if st.session_state.room:
        return Room.from_dict(st.session_state.room)
    return None


def save_room(room: Room):
    st.session_state.room = room.to_dict()


def get_player() -> Player | None:
    if st.session_state.player:
        return Player.from_dict(st.session_state.player)
    return None


def save_player(player: Player):
    st.session_state.player = player.to_dict()


# ─────────────────────────────────────────
# HP 바 렌더
# ─────────────────────────────────────────
def hp_color(ratio: float) -> str:
    if ratio > 0.6:
        return "#00c878"
    elif ratio > 0.3:
        return "#f0a020"
    else:
        return "#e03030"


def render_hp_bar(hp: int, max_hp: int):
    ratio = hp / max_hp if max_hp > 0 else 0
    color = hp_color(ratio)
    st.markdown(f"""
    <div class="hp-bar-bg">
      <div class="hp-bar-fill" style="width:{ratio*100:.0f}%; background:{color};"></div>
    </div>
    <div style="font-family:'Share Tech Mono',monospace; font-size:11px; color:{color}; margin-top:3px;">
      {hp} / {max_hp}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# 페이지 1 — 로비 (방 생성 / 입장)
# ─────────────────────────────────────────
def page_lobby():
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 20px;">
      <div style="font-family:'Share Tech Mono',monospace; font-size:11px; letter-spacing:6px; color:#3a7abf;">
        ◈  UNITED SPACE AUTHORITY  ◈
      </div>
      <div style="font-family:'Share Tech Mono',monospace; font-size:52px; color:#e0f0ff; line-height:1; margin:8px 0;">
        ORBIT-13
      </div>
      <div style="font-family:'Exo 2',sans-serif; font-size:13px; color:#4a7a9a; letter-spacing:2px;">
        STATION INCIDENT RESPONSE SYSTEM
      </div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="orbit-header">// 새 임무 생성</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        title = st.text_input("임무명", value="ORBIT-13 구조 작전", key="new_room_title")
        max_p = st.selectbox("최대 인원", [2, 3, 4], index=2, key="new_room_max")
        if st.button("🛸  임무 개시", use_container_width=True):
            room = Room(title=title, max_players=max_p)
            save_room(room)
            st.session_state.page = "setup"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="orbit-header">// 임무 참가</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        code = st.text_input("초대 코드", placeholder="예: AB3X7K", key="join_code")
        if st.button("📡  참가", use_container_width=True):
            # MVP: 현재 세션의 방만 지원 (추후 DB 연동)
            room = get_room()
            if room and room.invite_code == code.upper():
                st.session_state.page = "setup"
                st.rerun()
            else:
                st.error("유효하지 않은 초대 코드입니다.")
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
# 페이지 2 — 캐릭터 설정
# ─────────────────────────────────────────
def page_setup():
    room = get_room()
    if not room:
        st.session_state.page = "lobby"
        st.rerun()

    st.markdown(f"""
    <div class="orbit-header">// 요원 등록 — {room.title}</div>
    <div style="font-family:'Share Tech Mono',monospace; font-size:11px; color:#3a5a7a; margin-bottom:16px;">
      초대 코드 : {room.invite_code} &nbsp;|&nbsp; 인원 {len(room.players)} / {room.max_players}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    ROLE_DESC = {
        "Engineer": "시스템 수리 특화. 발전기·문 해제에 강점.",
        "Hacker":   "보안 우회 특화. 암호화된 로그·시스템 접근.",
        "Soldier":  "전투 특화. 위협 제거 및 팀 보호.",
        "Medic":    "치료 특화. 팀원 HP 회복 및 독성 처리.",
    }

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="orbit-header">요원 정보</div>', unsafe_allow_html=True)
        username      = st.text_input("사용자명", key="setup_username")
        char_name     = st.text_input("캐릭터명", key="setup_charname")
        role          = st.selectbox("역할", list(ROLE_DESC.keys()), key="setup_role")
        st.caption(ROLE_DESC[role])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="orbit-header">역할 능력치 미리보기</div>', unsafe_allow_html=True)
        from models.player import ROLE_SKILLS
        skills = ROLE_SKILLS.get(role, {})
        for skill, val in skills.items():
            bar = "█" * val + "░" * (3 - val)
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; margin:6px 0;">
              <span style="font-family:'Share Tech Mono',monospace; font-size:11px; color:#4a8ab0; letter-spacing:1px;">
                {skill.upper()}
              </span>
              <span style="font-family:'Share Tech Mono',monospace; font-size:13px; color:#5aadff;">
                {bar} {val}
              </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✅  요원 등록 완료", use_container_width=True):
        if not username or not char_name:
            st.warning("사용자명과 캐릭터명을 입력하세요.")
        else:
            player = Player(username=username, character_name=char_name, role=role)
            # 테스트용 아이템 지급
            for key in ["med_kit", "oxygen_canister", "log_chip"]:
                item = get_preset_item(key)
                if item:
                    player.add_item(item.to_dict())
            save_player(player)
            # 방에 플레이어 추가
            room.add_player(player)
            room.status = "playing"
            room.add_story("system", f"[{player.character_name}({player.role})] 임무에 합류했습니다.")
            save_room(room)
            st.session_state.page = "game"
            st.rerun()


# ─────────────────────────────────────────
# 페이지 3 — 게임 메인
# ─────────────────────────────────────────
def page_game():
    room   = get_room()
    player = get_player()
    gs = GameState.from_dict(st.session_state.game_state)
    if not room or not player:
        st.session_state.page = "lobby"
        st.rerun()
    

    # ── 상단 상태바 ──────────────────────────
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between;
                border-bottom:1px solid rgba(0,100,200,0.2); padding-bottom:10px; margin-bottom:16px;">
      <div>
        <span style="font-family:'Share Tech Mono',monospace; font-size:18px; color:#e0f0ff;">
          ORBIT-13
        </span>
        <span style="font-family:'Share Tech Mono',monospace; font-size:11px;
                     color:#3a7abf; margin-left:14px; letter-spacing:2px;">
          {room.title}
        </span>
      </div>
      <div style="font-family:'Share Tech Mono',monospace; font-size:11px; color:#3a5a7a; letter-spacing:1px;">
        STATUS : {room.status.upper()} &nbsp;|&nbsp; CODE : {room.invite_code}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 3단 레이아웃 ─────────────────────────
    left, center, right = st.columns([1, 2, 1], gap="medium")

    # ── 왼쪽: 캐릭터 패널 ────────────────────
    with left:
        st.markdown('<div class="orbit-header">// 요원 상태</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)

        role_class = f"badge-{player.role}"
        st.markdown(f"""
        <div style="margin-bottom:10px;">
          <div style="font-family:'Share Tech Mono',monospace; font-size:16px; color:#e0f0ff;">
            {player.character_name}
          </div>
          <div style="margin-top:4px;">
            <span class="role-badge {role_class}">{player.role}</span>
          </div>
          <div style="font-size:11px; color:#3a5a7a; margin-top:4px;">
            {player.username}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="stat-label">HP</div>', unsafe_allow_html=True)
        render_hp_bar(player.hp, player.max_hp)
        st.markdown('</div>', unsafe_allow_html=True)

        # 능력치
        st.markdown('<div class="card" style="margin-top:0;">', unsafe_allow_html=True)
        st.markdown('<div class="orbit-header">능력치</div>', unsafe_allow_html=True)
        for skill, val in player.skills.items():
            bar = "█" * val + "░" * (3 - val)
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; margin:4px 0;">
              <span style="font-family:'Share Tech Mono',monospace; font-size:10px; color:#3a6a8a;">
                {skill.upper()}
              </span>
              <span style="font-family:'Share Tech Mono',monospace; font-size:11px; color:#4a9abf;">
                {bar}
              </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 인벤토리
        st.markdown('<div class="orbit-header">// 인벤토리</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if player.inventory:
            for item in player.inventory:
                itype = item.get("item_type", "")
                extra_class = {"clue": "item-clue", "key": "item-key", "weapon": "item-weapon"}.get(itype, "")
                st.markdown(
                    f'<span class="item-tag {extra_class}">{item.get("name","?")}</span>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown('<span style="font-size:11px; color:#2a4a6a;">— 없음 —</span>', unsafe_allow_html=True)

        # 회복 아이템 사용 버튼
        heal_items = [i for i in player.inventory if i.get("effect_type") == "heal"]
        if heal_items:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"💊 {heal_items[0]['name']} 사용", use_container_width=True):
                used = player.use_item(heal_items[0]["item_id"])
                if used:
                    player.heal(used.get("effect_value", 0))
                    save_player(player)
                    room.add_chat("SYSTEM", f"{player.character_name}이(가) {used['name']}을(를) 사용했습니다.")
                    save_room(room)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── 중앙: 스토리 로그 + 행동창 ───────────
    with center:
        st.markdown('<div class="orbit-header">// 임무 로그</div>', unsafe_allow_html=True)

        # 스토리 히스토리
        story_box = st.container(height=340)
        with story_box:
            if not room.story_history:
                st.markdown(
                    '<div class="msg-echo">[ECHO] 시스템 초기화 완료. 요원 여러분을 감지했습니다.</div>',
                    unsafe_allow_html=True
                )
            for msg in room.story_history:
                role_tag = msg.get("role", "")
                content  = msg.get("content", "")
                if role_tag == "assistant":
                    st.markdown(f'<div class="msg-echo">[ECHO] {content}</div>', unsafe_allow_html=True)
                elif role_tag == "system":
                    st.markdown(f'<div class="msg-gm">◈ {content}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="msg-player">▶ {content}</div>', unsafe_allow_html=True)

        # 행동 입력
        st.markdown('<div class="orbit-header" style="margin-top:12px;">// 행동 입력</div>', unsafe_allow_html=True)
        action = st.text_input(
            "", placeholder="행동을 입력하세요 (예: 3구역 문을 연다)",
            key="action_input", label_visibility="collapsed"
        )
        col_a, col_b = st.columns([3, 1])
        with col_a:
            if st.button("📡  전송", use_container_width=True):
                if action.strip():
                    room.add_story("user", f"[{player.character_name}] {action}")
                    # TODO: echo.py 연결 후 AI 응답 추가
                    room.add_story("assistant", "신호를 수신했습니다. 분석 중...")
                    save_room(room)
                    st.rerun()
        with col_b:
            if st.button("🎲  d20", use_container_width=True):
                import random
                result = random.randint(1, 20)
                room.add_story("system", f"🎲 {player.character_name} → d20 결과 : {result}")
                save_room(room)
                st.rerun()

    # ── 오른쪽: 방 정보 + 채팅 ───────────────
    with right:
        # 방 상태
        st.markdown('<div class="orbit-header">// 정거장 상태</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)

        # 산소 / 전력 (game_state.py 연결 전 하드코딩)
        for label, val, color in [
            ("산소", gs.oxygen, "#00c878"),
            ("전력", gs.power,  "#f0a020"),
            ]:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
              <div style="display:flex; justify-content:space-between;">
                <span class="stat-label">{label}</span>
                <span style="font-family:'Share Tech Mono',monospace; font-size:11px; color:{color};">{val}%</span>
              </div>
              <div class="hp-bar-bg" style="margin-top:4px;">
                <div class="hp-bar-fill" style="width:{val}%; background:{color};"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 참가자 목록
        st.markdown('<div class="orbit-header">// 요원 목록</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for p_dict in room.players:
            p = Player.from_dict(p_dict)
            role_class = f"badge-{p.role}"
            alive_dot  = "🟢" if p.is_alive else "🔴"
            st.markdown(f"""
            <div class="player-row">
              <span>{alive_dot}</span>
              <span style="font-family:'Share Tech Mono',monospace; font-size:12px; color:#c8d8e8;">
                {p.character_name}
              </span>
              <span class="role-badge {role_class}" style="font-size:9px;">{p.role}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 채팅
        st.markdown('<div class="orbit-header">// 채팅</div>', unsafe_allow_html=True)
        chat_box = st.container(height=180)
        with chat_box:
            if not room.chat_log:
                st.markdown('<span style="font-size:11px; color:#2a4a6a;">— 채팅 없음 —</span>', unsafe_allow_html=True)
            for msg in room.chat_log[-20:]:
                st.markdown(
                    f'<div style="font-size:12px; margin:3px 0;">'
                    f'<span style="color:#3a7abf; font-family:\'Share Tech Mono\',monospace;">{msg["sender"]}</span> '
                    f'<span style="color:#8aa8c0;">{msg["message"]}</span></div>',
                    unsafe_allow_html=True
                )

        chat_msg = st.text_input("", placeholder="채팅 입력...", key="chat_input", label_visibility="collapsed")
        if st.button("💬  전송", use_container_width=True, key="chat_send"):
            if chat_msg.strip():
                room.add_chat(player.character_name, chat_msg)
                save_room(room)
                st.rerun()

    # ── 하단: 방 초기화 버튼 (개발용) ────────
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("↩  로비로 돌아가기"):
        st.session_state.page  = "lobby"
        st.session_state.room  = None
        st.session_state.player= None
        st.rerun()


# ─────────────────────────────────────────
# 메인 라우터
# ─────────────────────────────────────────
init_session()

if st.session_state.page == "lobby":
    page_lobby()
elif st.session_state.page == "setup":
    page_setup()
elif st.session_state.page == "game":
    page_game()