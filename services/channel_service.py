from sqlalchemy.orm import Session
from models.channel import Channel, ChannelTariff, EntryToken, ChannelMembership, ChannelType
from models.user import User
from datetime import datetime, timedelta
import secrets
import string
import logging

logger = logging.getLogger(__name__)

class ChannelService:
    """Servicio para gestión de canales"""

    @staticmethod
    def register_channel(db: Session, channel_id: int, channel_name: str, channel_type: ChannelType) -> Channel:
        """Registra un nuevo canal"""
        try:
            existing = db.query(Channel).filter(Channel.channel_id == channel_id).first()
            if existing:
                raise ValueError(f"Canal {channel_id} ya está registrado")

            channel = Channel(
                channel_id=channel_id,
                channel_name=channel_name,
                channel_type=channel_type
            )

            db.add(channel)
            db.commit()
            db.refresh(channel)

            logger.info(f"Canal registrado: {channel_name} ({channel_type.value})")
            return channel

        except Exception as e:
            logger.error(f"Error registrando canal: {e}")
            db.rollback()
            raise

    @staticmethod
    def create_tariff(db: Session, channel_id: int, name: str, duration_days: int, price_besitos: int) -> ChannelTariff:
        """Crea una nueva tarifa para un canal"""
        try:
            channel = db.query(Channel).filter(Channel.id == channel_id).first()
            if not channel:
                raise ValueError("Canal no encontrado")

            tariff = ChannelTariff(
                channel_id=channel_id,
                name=name,
                duration_days=duration_days,
                price_besitos=price_besitos
            )

            db.add(tariff)
            db.commit()
            db.refresh(tariff)

            logger.info(f"Tarifa creada: {name} - {duration_days} días - {price_besitos} besitos")
            return tariff

        except Exception as e:
            logger.error(f"Error creando tarifa: {e}")
            db.rollback()
            raise

    @staticmethod
    def generate_entry_token(db: Session, tariff_id: int, created_by: int) -> str:
        """Genera un token de entrada único"""
        try:
            tariff = db.query(ChannelTariff).filter(ChannelTariff.id == tariff_id).first()
            if not tariff:
                raise ValueError("Tarifa no encontrada")

            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

            expires_at = datetime.utcnow() + timedelta(days=tariff.duration_days)

            entry_token = EntryToken(
                token=token,
                tariff_id=tariff_id,
                created_by=created_by,
                expires_at=expires_at
            )

            db.add(entry_token)
            db.commit()
            db.refresh(entry_token)

            bot_username = "tu_bot_username"
            link = f"https://t.me/{bot_username}?start={token}"

            logger.info(f"Token generado: {token}")
            return link

        except Exception as e:
            logger.error(f"Error generando token: {e}")
            db.rollback()
            raise

    @staticmethod
    def get_channels(db: Session) -> list:
        """Obtiene todos los canales registrados"""
        return db.query(Channel).filter(Channel.is_active == True).all()

    @staticmethod
    def get_channel_tariffs(db: Session, channel_id: int) -> list:
        """Obtiene las tarifas de un canal"""
        return db.query(ChannelTariff).filter(
            ChannelTariff.channel_id == channel_id,
            ChannelTariff.is_active == True
        ).all()
