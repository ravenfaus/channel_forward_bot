from __future__ import annotations

from sqlalchemy.sql import expression

from models.base import BaseModel, db


class Chain(BaseModel):
    __tablename__ = "chains"

    chat_id = db.Column(db.BigInteger, primary_key=True, unique=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
