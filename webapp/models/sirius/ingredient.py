from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import Base


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String, unique=True)
