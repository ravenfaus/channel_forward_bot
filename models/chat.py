from sqlalchemy.sql import expression

from models.base import BaseModel, db
from models.chain import Chain


class Chat(BaseModel):
    __tablename__ = "chats"

    chat_id = db.Column(db.BigInteger, primary_key=True, unique=True)
    type = db.Column(db.String)
    title = db.Column(db.String)
    forward_id = db.Column(
        db.ForeignKey(f"{Chain.__tablename__}.chat_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

