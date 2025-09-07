import base64
from datetime import datetime, timezone
from typing import Optional

import pydenticon
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size: int):
        foreground = [
            "rgb(45,79,255)",
            "rgb(254,180,44)",
            "rgb(226,121,234)",
            "rgb(30,179,253)",
            "rgb(232,77,65)",
            "rgb(49,203,115)",
            "rgb(141,69,170)",
        ]
        background = "rgb(224,224,224)"
        padding_size = size // 8
        padding = (padding_size, padding_size, padding_size, padding_size)
        block_size = 8

        generator = pydenticon.Generator(
            block_size, block_size, foreground=foreground, background=background
        )

        identicon = generator.generate(self.username, size, size, padding=padding)

        # returns a data URL for embedding in HTML
        identicon_base64 = base64.b64encode(identicon).decode("ascii")
        return f"data:image/png;base64,{identicon_base64}"


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates="posts")

    def __repr__(self):
        return f"Post {self.body}"
