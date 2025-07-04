from dataclasses import dataclass

@dataclass
class Mission:
    id: int
    mission_type: str
    title: str
    description: str
    reward_besitos: int
    reward_lore: int

@dataclass
class UserMission:
    id: int
    user_id: int
    mission_id: int
    progress: int
    completed: bool
    claimed: bool

@dataclass
class DailyGift:
    id: int
    user_id: int
    claimed_at: str
    besitos_reward: int
    lore_reward: int
