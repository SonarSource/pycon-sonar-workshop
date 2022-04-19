import sqlite3

connection = sqlite3.connect("database.db")


with open("pokedex/schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open("pokemon.txt") as file:
    lines = file.readlines()
    pokemon_number = 1
    for line in lines:
        name, description = line.split(";")
        cur.execute(
            f"INSERT INTO POKEDEX (id, pokemon_name, image_url, description) VALUES ("
            f"{pokemon_number}, "
            f'"{name}", '
            f'"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_number}.png", '
            f'"{description}")'
        )
        pokemon_number += 1

connection.commit()
connection.close()
