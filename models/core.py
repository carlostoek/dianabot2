from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    telegram_id: int
    username: str
    first_name: str
    is_onboarded: bool
    created_at: str
