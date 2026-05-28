from dataclasses import dataclass, field
from typing import Optional
import uuid

# ─────────────────────────────────────────
# 아이템 타입 상수
# ─────────────────────────────────────────
class ItemType:
    CONSUMABLE  = "consumable"   # 소모품 (회복, 산소 등)
    TOOL        = "tool"         # 도구 (해킹 장치, 수리 키트 등)
    KEY         = "key"          # 열쇠류 (출입 카드, 암호 칩 등)
    CLUE        = "clue"         # 단서 (로그 파일, 메모, 사진 등)
    WEAPON      = "weapon"       # 무기 (전기 충격기 등)


# ─────────────────────────────────────────
# 아이템 효과 정의
# ─────────────────────────────────────────
class EffectType:
    HEAL        = "heal"         # HP 회복
    OXYGEN      = "oxygen"       # 산소 수치 회복
    POWER       = "power"        # 전력 회복
    HACK_BONUS  = "hack_bonus"   # 해킹 성공률 +N
    REPAIR_BONUS= "repair_bonus" # 수리 성공률 +N
    DAMAGE      = "damage"       # 데미지 (무기)
    UNLOCK      = "unlock"       # 특정 구역/문 해제


# ─────────────────────────────────────────
# 아이템 클래스
# ─────────────────────────────────────────
@dataclass
class Item:
    name: str
    item_type: str
    description: str
    effect_type: Optional[str] = None
    effect_value: int = 0               # 효과 수치 (HP +30, 산소 +20 등)
    unlock_target: Optional[str] = None # KEY 아이템이 열 수 있는 구역/문 이름
    is_consumable: bool = True          # 사용 후 소멸 여부
    item_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(**data)

    def __str__(self) -> str:
        return f"[{self.item_type.upper()}] {self.name} — {self.description}"


# ─────────────────────────────────────────
# 기본 아이템 프리셋
# ORBIT-13 세계관에 맞춘 아이템 목록
# ─────────────────────────────────────────
ITEM_PRESETS = {
    # 소모품
    "med_kit": Item(
        name="의료 키트",
        item_type=ItemType.CONSUMABLE,
        description="기본 외상 처치 키트. HP 30 회복.",
        effect_type=EffectType.HEAL,
        effect_value=30,
    ),
    "oxygen_canister": Item(
        name="산소 캐니스터",
        item_type=ItemType.CONSUMABLE,
        description="비상용 압축 산소통. 산소 수치 25 회복.",
        effect_type=EffectType.OXYGEN,
        effect_value=25,
    ),
    "energy_cell": Item(
        name="에너지 셀",
        item_type=ItemType.CONSUMABLE,
        description="소형 배터리 팩. 전력 수치 20 회복.",
        effect_type=EffectType.POWER,
        effect_value=20,
    ),

    # 도구
    "hack_device": Item(
        name="해킹 장치",
        item_type=ItemType.TOOL,
        description="보안 시스템 우회 장치. 해킹 성공률 +2.",
        effect_type=EffectType.HACK_BONUS,
        effect_value=2,
        is_consumable=False,
    ),
    "repair_kit": Item(
        name="수리 키트",
        item_type=ItemType.TOOL,
        description="기계 수리용 공구 세트. 수리 성공률 +2.",
        effect_type=EffectType.REPAIR_BONUS,
        effect_value=2,
        is_consumable=False,
    ),

    # 열쇠
    "sector_a_card": Item(
        name="A구역 출입 카드",
        item_type=ItemType.KEY,
        description="연구동 A구역 출입 권한 카드.",
        effect_type=EffectType.UNLOCK,
        unlock_target="sector_a",
        is_consumable=False,
    ),
    "captain_card": Item(
        name="함장실 마스터 키",
        item_type=ItemType.KEY,
        description="함장실 및 통제실 출입 가능.",
        effect_type=EffectType.UNLOCK,
        unlock_target="captain_room",
        is_consumable=False,
    ),

    # 단서
    "crew_memo": Item(
        name="승무원 메모",
        item_type=ItemType.CLUE,
        description="구겨진 메모지. 누군가 급하게 쓴 흔적이 있다.",
        is_consumable=False,
    ),
    "log_chip": Item(
        name="로그 칩",
        item_type=ItemType.CLUE,
        description="데이터 로그가 저장된 칩. ECHO가 숨긴 기록일 수도 있다.",
        is_consumable=False,
    ),
    "photo": Item(
        name="사진",
        item_type=ItemType.CLUE,
        description="실험실에서 발견된 사진. 49번째 승무원의 것으로 보인다.",
        is_consumable=False,
    ),

    # 무기
    "stun_gun": Item(
        name="전기 충격기",
        item_type=ItemType.WEAPON,
        description="보안 요원용 충격기. 데미지 15.",
        effect_type=EffectType.DAMAGE,
        effect_value=15,
        is_consumable=False,
    ),
}


def get_preset_item(key: str) -> Optional[Item]:
    """
    프리셋 아이템을 새 item_id로 복사해서 반환.
    같은 프리셋을 여러 플레이어가 가져도 id가 겹치지 않음.
    """
    preset = ITEM_PRESETS.get(key)
    if not preset:
        return None
    data = preset.to_dict()
    data["item_id"] = str(uuid.uuid4())
    return Item.from_dict(data)