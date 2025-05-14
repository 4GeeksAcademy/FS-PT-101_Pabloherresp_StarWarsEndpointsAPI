from app import app, db
from models import Users, Pokemons, Cities, Regions, Favs, Type
from sqlalchemy import select

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = Users(email="pablo2@example.com", password="1234")
    user2 = Users(email="rocky@example.com", password="5678")
    db.session.add_all([user1, user2])
    db.session.commit()

    pokemon1 = Pokemons(name="Pikachu", type=Type.Electric)
    pokemon2 = Pokemons(name="Charmander", type=Type.Fire)
    pokemon3 = Pokemons(name="Mewtwo", type=Type.Psychic)
    db.session.add_all([pokemon1, pokemon2, pokemon3])
    db.session.commit()

    region1 = Regions(name="Kanto")
    region2 = Regions(name="Johto")
    db.session.add_all([region1, region2])
    db.session.commit()

    city1 = Cities(name="Pueblo Paleta", region_id=region1.id)
    city2 = Cities(name="Pueblo Azalea", region_id=region2.id)
    db.session.add_all([city1, city2])
    db.session.commit()

    # fav1 = Favs(user_id=user1.id,city_id=city1.id)
    # fav2 = Favs(user_id=user1.id,city_id=city2.id)
    # fav3 = Favs(user_id=user1.id,pokemon_id=pokemon2.id)
    # fav4 = Favs(user_id=user2.id,region_id=region1.id)
    # fav5 = Favs(user_id=user2.id,pokemon_id=pokemon1.id)
    # fav6 = Favs(user_id=user2.id,city_id=city1.id)
    # db.session.add_all([fav1, fav2, fav3, fav4, fav5, fav6])

    # db.session.commit()
    
    print("✅ Datos sembrados correctamente.")