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
        # bloque de código que separa los favoritos en función del tipo de favorito para no tener valores nulos en la respuesta
        favs_pokemons = []
        favs_cities = []
        favs_regions = []
        for item in self.favs:
            if item.serialize()["pokemon"]:
                favs_pokemons.append({"pokemon": item.serialize()["pokemon"]})
            elif item.serialize()["city"]:
                favs_cities.append({"cities": item.serialize()["city"]})
            elif item.serialize()["region"]:
                favs_regions.append({"regions": item.serialize()["region"]})

        return {
            "id": self.id,
            "email": self.email,
            "favs_pokemon": favs_pokemons,
            "favs_cities": favs_cities,
            "favs_regions": favs_regions
        }

class Pokemons(db.Model):
    __tablename__ = "pokemons"
    id:  Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type1: Mapped[Type] = mapped_column(Enum(Type), nullable=False)
    type2: Mapped[Type] = mapped_column(Enum(Type), nullable=True)
    desc: Mapped[str] = mapped_column(nullable=False)

    favved_by: Mapped[list["Favs"]] = relationship(back_populates="pokemon")
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "type1": self.type1._name_,
            "type2": self.type2._name_ if self.type2 else None,
            "desc": self.desc,
            "favved_by": [item.user.email for item in self.favved_by]
        }

class Cities(db.Model):
    __tablename__ = "cities"
    id:  Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)

    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    region: Mapped["Regions"] = relationship(back_populates="cities", uselist=False)
    favved_by: Mapped[list["Favs"]] = relationship(back_populates="city")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "region": self.region.name if self.region else None,
            "favved_by": [item.user.email for item in self.favved_by]
        }

class Regions(db.Model):
    __tablename__ = "regions"
    id:  Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    cities: Mapped[list["Cities"]] = relationship(back_populates="region")
    favved_by: Mapped[list["Favs"]] = relationship(back_populates="region")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "cities": [city.name for city in self.cities],
            "favved_by": [item.user.id for item in self.favved_by]
        }

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

    def serialize(self):
        return{
            "user": self.user.email,
            "pokemon": self.pokemon.serialize() if self.pokemon else None,
            "city": self.city.serialize() if self.city else None,
            "region": self.region.serialize() if self.region else None
        }