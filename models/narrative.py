from dataclasses import dataclass

@dataclass
class LorePiece:
    id: int
    code: str
    title: str
    description: str
    rarity: str

@dataclass
class UserBackpack:
    id: int
    user_id: int
    lore_piece_id: int
    obtained_at: str
