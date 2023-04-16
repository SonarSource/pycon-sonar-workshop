import re
import sqlite3


class ConnectionWrapper:
    """A simple connection wrapper class"""

    def __init__(self, db_path):
        self.__conn = sqlite3.connect(db_path)

    def get_all_pokemons(self):
        statement = "SELECT * FROM POKEDEX"
        return self.__conn.execute(statement).fetchall()

    def register_subscriber(self, email):
        try:
            self.__conn.execute("INSERT into SUBSCRIBERS(email) values (?)", (email,))
            self.__conn.commit()
        except sqlite3.DatabaseError:
            raise Exception("Problem with the database!")
        except sqlite3.IntegrityError:
            raise ValueError("Email already exists!")

    def cleanup(self, should_close: bool):
        if should_close:
            self.__conn.close()


def fetch_all_pokemons(wrapper: ConnectionWrapper):
    return wrapper.get_all_pokemons()


def register_subscriber(wrapper: ConnectionWrapper, email):
    pattern = re.compile(r"(.*)@(.*\..*)")
    if not pattern.match(email):
        ValueError("Invalid email!")
    wrapper.register_subscriber(email)
    pass
