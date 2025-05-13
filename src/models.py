import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Type(enum.Enum):
    Fire = "Fire"
    Water =  "Water"
    Grass = "Grass"
    Bug = "Bug"
    Dark = "Dark"
    Dragon = "Dragon"
    Electric = "Electric"
    Fairy = "Fairy"
    Fighting = "Fighting"
    Flying = "Flying"
    Ghost = "Ghost"
    Ground = "Ground"
    Ice = "Ice"
    Normal = "Normal"
    Poison = "Poison"
    Psychic = "Psychic"
    Rock = "Rock"
    Steel = "Steel"


class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favs: Mapped[list["Favs"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }

class Pokemons(db.Model):
    __tablename__ = "pokemons"
    id:  Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type : Mapped[Type] = mapped_column(Enum(Type), nullable=False)
    favved_by: Mapped[list["Favs"]] = relationship(back_populates="pokemon")

class Cities(db.Model):
    __tablename__ = "cities"
    id:  Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    region: Mapped["Regions"] = relationship(back_populates="cities", uselist=False)
    favved_by: Mapped[list["Favs"]] = relationship(back_populates="city")

class Regions(db.Model):
    __tablename__ = "regions"
    id:  Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    cities: Mapped[list["Cities"]] = relationship(back_populates="region")
    favved_by: Mapped[list["Favs"]] = relationship(back_populates="region")

class Favs(db.Model):
    __tablename__ = "favs"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),primary_key=True)
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id"),primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"),primary_key=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"),primary_key=True)

    user: Mapped["Users"] = relationship(back_populates="favs")
    pokemon: Mapped["Pokemons"] = relationship(back_populates="favved_by")
    city: Mapped["Cities"] = relationship(back_populates="favved_by")
    region: Mapped["Regions"] = relationship(back_populates="favved_by")