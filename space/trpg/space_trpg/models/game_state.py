from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import random

# ─────────────────────────────────────────
# 구역 정의
# ─────────────────────────────────────────
SECTORS = {
    "bridge":       {"name": "함교",        "oxygen": True,  "power": True,  "locked": False},
    "med_bay":      {"name": "의무실",       "oxygen": True,  "power": True,  "locked": False},
    "engine_room":  {"name": "엔진실",       "oxygen": True,  "power": True,  "locked": False},
    "lab_a":        {"name": "연구실 A",     "oxygen": True,  "power": False, "locked": True },
    "lab_b":        {"name": "연구실 B",     "oxygen": False, "power": False, "locked": True },
    "cargo":        {"name": "화물칸",       "oxygen": True,  "power": True,  "locked": False},
    "airlock":      {"name": "에어록",       "oxygen": False, "power": True,  "locked": True },
    "escape_pod":   {"name": "탈출선 격납고", "oxygen": True,  "power": False, "locked": True },
}

# ─────────────────────────────────────────
# 이벤트 정의
# ─────────────────────────────────────────
EVENTS = {
    "blackout": {
        "name": "정전",
        "description": "정거장 전체 전력이 차단되었습니다. 비상 조명만 작동 중입니다.",
        "effect": {"power": -20},
    },
    "oxygen_leak": {
        "name": "산소 누출",
        "description": "산소 파이프 파열 감지. 급격한 산소 감소가 시작됩니다.",
        "effect": {"oxygen": -15},
    },
    "door_lockdown": {
        "name": "격리 잠금",
        "description": "[ECHO] 비정상 생체 신호 감지. 격리 프로토콜을 실행합니다.",
        "effect": {},
    },
    "unknown_signal": {
        "name": "미확인 신호",
        "description": "통신 채널에서 정체불명의 신호가 감지되었습니다.",
        "effect": {},
    },
    "crew_count_anomaly": {
        "name": "승무원 수 이상",
        "description": "[ECHO] 승무원 수 : 48명 → 49명. 오류가 아닙니다.",
        "effect": {},
    },
}


# ─────────────────────────────────────────
# GameState 클래스
# ─────────────────────────────────────────
@dataclass
class GameState:
    # 정거장 핵심 자원
    oxygen: int = 100        # 0 → 전멸 엔딩
    power: int = 100         # 0 → 정전 이벤트 강제 발동

    # 현재 구역
    current_sector: str = "bridge"

    # 구역별 잠금 상태 (잠긴 구역 key 목록)
    locked_sectors: list = field(default_factory=lambda: ["lab_a", "lab_b", "airlock", "escape_pod"])

    # 해금된 단서 목록 (item_id 또는 clue 이름)
    discovered_clues: list = field(default_factory=list)

    # 발생한 이벤트 기록
    event_log: list = field(default_factory=list)

    # 탈출선 활성화 여부
    escape_pod_active: bool = False

    # 게임 턴 수
    turn: int = 0

    # 생성 시각
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # ── 자원 관련 ─────────────────────────

    def drain_oxygen(self, amount: int = 2):
        """매 턴 산소 자연 감소 (기본 2씩)"""
        self.oxygen = max(0, self.oxygen - amount)

    def drain_power(self, amount: int = 1):
        """매 턴 전력 자연 감소 (기본 1씩)"""
        self.power = max(0, self.power - amount)

    def restore_oxygen(self, amount: int):
        self.oxygen = min(100, self.oxygen + amount)

    def restore_power(self, amount: int):
        self.power = min(100, self.power + amount)

    def is_oxygen_critical(self) -> bool:
        return self.oxygen <= 20

    def is_power_critical(self) -> bool:
        return self.power <= 20

    # ── 구역 관련 ─────────────────────────

    def move_to(self, sector_key: str) -> dict:
        """
        구역 이동 시도.
        반환: {"success": bool, "message": str}
        """
        if sector_key not in SECTORS:
            return {"success": False, "message": "존재하지 않는 구역입니다."}

        if sector_key in self.locked_sectors:
            sector_name = SECTORS[sector_key]["name"]
            return {"success": False, "message": f"{sector_name} 구역은 잠겨 있습니다. 출입 카드가 필요합니다."}

        self.current_sector = sector_key
        sector_name = SECTORS[sector_key]["name"]

        # 산소 없는 구역 진입 경고
        if not SECTORS[sector_key]["oxygen"]:
            return {"success": True, "message": f"{sector_name} 구역으로 이동했습니다. ⚠ 이 구역은 산소가 없습니다."}

        return {"success": True, "message": f"{sector_name} 구역으로 이동했습니다."}

    def unlock_sector(self, sector_key: str, key_item_target: str) -> dict:
        """
        아이템의 unlock_target과 sector_key가 일치하면 잠금 해제.
        반환: {"success": bool, "message": str}
        """
        if sector_key not in self.locked_sectors:
            return {"success": False, "message": "이미 열려 있는 구역입니다."}

        if key_item_target != sector_key:
            return {"success": False, "message": "이 카드로는 열 수 없는 구역입니다."}

        self.locked_sectors.remove(sector_key)
        sector_name = SECTORS[sector_key]["name"]
        return {"success": True, "message": f"{sector_name} 구역 잠금이 해제되었습니다."}

    def get_current_sector_info(self) -> dict:
        """현재 구역 정보 반환"""
        info = SECTORS.get(self.current_sector, {})
        return {
            "key":   self.current_sector,
            "name":  info.get("name", "알 수 없는 구역"),
            "oxygen": info.get("oxygen", False),
            "power":  info.get("power", False),
            "locked": self.current_sector in self.locked_sectors,
        }

    # ── 이벤트 관련 ───────────────────────

    def trigger_event(self, event_key: str) -> dict:
        """
        이벤트 발동.
        반환: {"name": str, "description": str}
        """
        event = EVENTS.get(event_key)
        if not event:
            return {}

        # 효과 적용
        effect = event.get("effect", {})
        if "oxygen" in effect:
            self.oxygen = max(0, self.oxygen + effect["oxygen"])
        if "power" in effect:
            self.power = max(0, self.power + effect["power"])

        # 로그 기록
        self.event_log.append({
            "event_key":   event_key,
            "name":        event["name"],
            "description": event["description"],
            "turn":        self.turn,
            "timestamp":   datetime.now().isoformat(),
        })

        return {"name": event["name"], "description": event["description"]}

    def maybe_trigger_random_event(self, chance: float = 0.15) -> Optional[dict]:
        """
        매 턴 일정 확률로 랜덤 이벤트 발생.
        chance: 0.0 ~ 1.0 (기본 15%)
        """
        if random.random() < chance:
            event_key = random.choice(list(EVENTS.keys()))
            return self.trigger_event(event_key)
        return None

    # ── 단서 관련 ─────────────────────────

    def add_clue(self, clue_name: str):
        if clue_name not in self.discovered_clues:
            self.discovered_clues.append(clue_name)

    def get_clue_count(self) -> int:
        return len(self.discovered_clues)

    # ── 엔딩 판정 ─────────────────────────

    def check_ending(self, all_players_alive: bool) -> Optional[str]:
        """
        엔딩 조건 체크.
        반환: 엔딩 key 문자열 or None (게임 계속)
        """
        if self.oxygen <= 0:
            return "extinction"         # 전멸 엔딩

        if not all_players_alive:
            return "extinction"

        if self.escape_pod_active:
            return "escape"             # 탈출 엔딩

        # 단서 7개 이상 + ECHO 관련 단서 있으면 은폐 엔딩 가능
        if self.get_clue_count() >= 7 and "echo_secret" in self.discovered_clues:
            return "coexist"            # AI 공존 엔딩 (분기 가능)

        return None                     # 게임 계속

    # ── 턴 진행 ───────────────────────────

    def next_turn(self) -> dict:
        """
        턴 넘길 때 호출.
        자원 감소 + 랜덤 이벤트 체크.
        반환: {"turn": int, "event": dict or None, "warnings": list}
        """
        self.turn += 1
        self.drain_oxygen()
        self.drain_power()

        event   = self.maybe_trigger_random_event()
        warnings = []

        if self.is_oxygen_critical():
            warnings.append("⚠ 산소 위험 수치입니다!")
        if self.is_power_critical():
            warnings.append("⚠ 전력 위험 수치입니다!")

        return {"turn": self.turn, "event": event, "warnings": warnings}

    # ── 직렬화 ────────────────────────────

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        return cls(**data)