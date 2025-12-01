import sqlalchemy as sa
from sqlalchemy.orm import relationship
from models.DB import Base
from datetime import datetime


class AirdropSubscription(Base):
    __tablename__ = "airdrop_subscriptions"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    airdrop_id = sa.Column(sa.Integer, sa.ForeignKey("airdrops.id"))
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.user_id"))
    wallet_address = sa.Column(sa.String)

    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    airdrop = relationship("Airdrop", back_populates="subscriptions")
    user = relationship("User", back_populates="subscriptions")

    def __str__(self):
        return (
            f"Airdrop: <code>{self.airdrop.token_name}</code>\n"
            f"Wallet Address: <code>{self.wallet_address}</code>\n"
        )

    def __repr__(self):
        return f"AirdropSubscription(id={self.id}, airdrop_id={self.airdrop_id}, user_id={self.user_id}, wallet_address={self.wallet_address})"
