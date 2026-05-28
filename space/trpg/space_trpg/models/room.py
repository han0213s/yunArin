from dataclasses import dataclass, field
from datetime import datetime
from .player import Player
import random, string, uuid

def _make_invite_code() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@dataclass
class Room:
    title: str
    max_players: int = 4
    room_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    invite_code: str = field(default_factory=_make_invite_code)
    host_id: str = ""
    players: list = field(default_factory=list)   # list[Player]
    status: str = "waiting"   # waiting / playing / ended
    chat_log: list = field(default_factory=list)
    story_history: list = field(default_factory=list)  # OpenAI messages 형식
    current_scene: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_player(self, player: Player) -> bool:
        if self.is_full():
            return False
        self.players.append(player.to_dict())
        if not self.host_id:
            self.host_id = player.player_id
        return True

    def is_full(self) -> bool:
        return len(self.players) >= self.max_players

    def add_chat(self, sender: str, message: str):
        self.chat_log.append({
            "sender": sender,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def add_story(self, role: str, content: str):
        # OpenAI messages 형식 그대로 누적 → AI에 그냥 넘기면 됨
        self.story_history.append({"role": role, "content": content})

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)