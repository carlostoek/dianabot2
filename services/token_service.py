from sqlalchemy.orm import Session
from models.token import Token

class TokenService:
    @staticmethod
    def create_token(db: Session, name: str, duration_days: int, price: float) -> Token:
        new_token = Token(name=name, duration_days=duration_days, price=price)
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        return new_token

    @staticmethod
    def get_token_by_name(db: Session, name: str) -> Token:
        return db.query(Token).filter(Token.name == name).first()

    @staticmethod
    def get_all_tokens(db: Session):
        return db.query(Token).all()
