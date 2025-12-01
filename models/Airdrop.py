import sqlalchemy as sa
from sqlalchemy.orm import relationship
from models.DB import Base
from datetime import datetime
from common.common import format_datetime, format_float
from models.Language import Language


class Airdrop(Base):
    __tablename__ = "airdrops"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    contract_address = sa.Column(sa.String)
    token_name = sa.Column(sa.String)
    amount = sa.Column(sa.BigInteger)
    distribution_date = sa.Column(sa.DateTime)

    photo = sa.Column(sa.String)

    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    subscriptions = relationship("AirdropSubscription", back_populates="airdrop")

    @property
    def total_subscriptions(self):
        return len(self.subscriptions)

    def calculate_time_remaining(self, lang: Language):
        total_seconds = (self.distribution_date - datetime.now()).total_seconds()
        days = format_float(total_seconds // 86400)
        hours = format_float((total_seconds % 86400) // 3600)
        minutes = format_float((total_seconds % 3600) // 60)
        seconds = format_float(total_seconds % 60)
        if lang == Language.ARABIC:
            return f"<b>{days} يوم, {hours} ساعة, {minutes} دقيقة, {seconds} ثانية</b>"
        return (
            f"<b>{(days)} days, {hours} hours, {minutes} minutes, {seconds} seconds</b>"
        )

    def __str__(self):
        return (
            f"Token Name: <code>{self.token_name}</code>\n"
            f"Distribution Amount: <b>{format_float(self.amount)}</b>\n"
            f"Total Subscriptions: <b>{self.total_subscriptions}</b>\n"
            f"Contract Address: <code>{self.contract_address}</code>\n"
            f"Distribution Date: <b>{format_datetime(self.distribution_date)}</b>"
        )

    def __repr__(self):
        return f"Airdrop(id={self.id}, contract_address={self.contract_address}, token_name={self.token_name})"
