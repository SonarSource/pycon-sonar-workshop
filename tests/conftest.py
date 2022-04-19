import sqlite3

import pytest

from pokedex import app as poke_app


@pytest.fixture(scope="session")
def app(tmp_path_factory):
    test_db_path = tmp_path_factory.mktemp("test") / "test.db"
    poke_app.app.config.update(
        {
            "TESTING": True,
            "DATABASE": test_db_path,
        }
    )
    init_test_db(test_db_path)
    yield poke_app.app


@pytest.fixture()
def client(app):
    return app.test_client()


def init_test_db(db_path):
    connection = sqlite3.connect(db_path)
    connection.executescript(
        """
        CREATE TABLE POKEDEX (
            id INTEGER PRIMARY KEY,
            pokemon_name TEXT NOT NULL,
            image_url TEXT NOT NULL,
            description TEXT NOT NULL
        );

        CREATE TABLE SUBSCRIBERS (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE
        );
        """
    )

    cur = connection.cursor()
    cur.execute(
        'INSERT INTO POKEDEX (id, pokemon_name, image_url, description) VALUES '
        '(42, "MockPokemon", "https://bla.com", "MockDescription")'
    )
    connection.commit()
    connection.close()
