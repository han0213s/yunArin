from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

ROLE_SKILLS = {
    "Engineer": {"repair": 3, "hacking": 1, "combat": 1},
    "Hacker":   {"repair": 1, "hacking": 3, "combat": 1},
    "Soldier":  {"repair": 1, "hacking": 1, "combat": 3},
    "Medic":    {"repair": 2, "hacking": 1, "combat": 1, "heal_bonus": 2},
}

@dataclass
class Player:
    username: str
    character_name: str
    role: str
    player_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    hp: int = 100
    max_hp: int = 100
    inventory: list = field(default_factory=list)  # list[dict] — Item.to_dict() 형태
    is_alive: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def skills(self) -> dict:
        return ROLE_SKILLS.get(self.role, {})

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.is_alive = False

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

    def add_item(self, item_dict: dict):
        """item.py의 Item.to_dict() 결과를 받아서 인벤토리에 추가"""
        self.inventory.append(item_dict)

    def use_item(self, item_id: str) -> Optional[dict]:
        """
        item_id로 아이템 사용.
        소모품이면 인벤토리에서 삭제 후 반환.
        비소모품이면 삭제 없이 반환.
        없으면 None 반환.
        """
        for i, item_data in enumerate(self.inventory):
            if item_data.get("item_id") == item_id:
                if item_data.get("is_consumable", True):
                    self.inventory.pop(i)
                return item_data
        return None

    def get_item_by_type(self, item_type: str) -> list:
        """특정 타입 아이템만 필터링 (예: 'clue', 'key')"""
        return [item for item in self.inventory if item.get("item_type") == item_type]

    def has_item(self, item_name: str) -> bool:
        """이름으로 아이템 보유 여부 확인"""
        return any(item.get("name") == item_name for item in self.inventory)

    def to_dict(self) -> dict:       # session_state 저장용
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict):  # session_state 복원용
        return cls(**data)