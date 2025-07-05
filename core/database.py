from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import Config

# Base para todos los modelos
Base = declarative_base()

# Motor de base de datos
engine = create_engine(
    Config.DATABASE_URL,
    echo=Config.DEBUG
)

# Sesión de base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """Generador de sesiones de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    """Obtiene una sesión de base de datos directa"""
    return SessionLocal()

def init_db():
    """Inicializa todas las tablas"""
    # Importar todos los modelos para registrarlos
    from models import user, mission, game_session
    from models import channel_management
    
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada correctamente")
    print(
        "📊 Tablas creadas: users, missions, user_missions, game_sessions, "
        "game_leaderboards, channels, channel_memberships, entry_tokens, "
        "channel_settings"
    )

def reset_db():
    """Resetea la base de datos (solo para desarrollo)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("\ud83d\udd04 Base de datos reseteada")
