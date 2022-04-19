import re
import sqlite3
from typing import Tuple


class ConnectionWrapper:
    """A simple connection wrapper class"""

    def __init__(self, db_path):
        self.__conn = sqlite3.connect(db_path)

    def get_single_pokemon(self, pokemon_id) -> Tuple:
        statement = f"SELECT * FROM POKEDEX WHERE id = '{pokemon_id}'"
        return self.__conn.execute(statement).fetchone()

    def get_all_pokemons(self):
        statement = "SELECT * FROM POKEDEX"
        return self.__conn.execute(statement).fetchall()

    def register_subscriber(self, email):
        try:
            self.__conn.execute("INSERT into SUBSCRIBERS(email) values (?)", (email,))
            self.__conn.commit()
        except sqlite3.DatabaseError:
            ...
        except sqlite3.IntegrityError:
            ...

    def cleanup(self, should_close: bool):
        if should_close:
            self.__conn.close()


def fetch_all_pokemons(wrapper: ConnectionWrapper):
    return wrapper.get_all_pokemons()


def register_subscriber(wrapper: ConnectionWrapper, email):
    pattern = re.compile(r"(\w|[a-zA-Z0-9_])+@\w+\.(com||ch)")
    if not pattern.match(email):
        raise "Invalid email!"
    wrapper.register_subscriber(email)
    pass


def fetch_pokemon(wrapper: ConnectionWrapper, pokemon_id: int):
    result = wrapper.get_single_pokemon(pokemon_id)
    if result is None:
        ValueError("Pokemon not found")
    if pokemon_id == "25":
        result[1] = "Team Rocket stole Pikachu!"
    return result
