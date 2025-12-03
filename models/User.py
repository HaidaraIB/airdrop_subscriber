import sqlalchemy as sa
from sqlalchemy.orm import relationship
from models.DB import Base
from models.Language import Language
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    user_id = sa.Column(sa.BigInteger, primary_key=True)
    username = sa.Column(sa.String)
    name = sa.Column(sa.String)
    lang = sa.Column(sa.Enum(Language), default=Language.ENGLISH)
    is_banned = sa.Column(sa.Boolean, default=0)
    is_admin = sa.Column(sa.Boolean, default=0)

    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    subscriptions = relationship("AirdropSubscription", back_populates="user")

    @property
    def username_or_name(self):
        return f'@{self.username}' if self.username else self.name

    def __str__(self):
        return (
            f"ID: <code>{self.user_id}</code>\n"
            f"Username: {self.username_or_name}\n"
            f"Name: <b>{self.name}</b>"
        )

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username}, name={self.name}, is_admin={bool(self.is_admin)}, is_banned={bool(self.is_banned)}"
