from unittest.mock import Mock

from pokedex import helper


def test_fetch_all_pokemon():
    connection_wrapper_mock = Mock()
    connection_wrapper_mock.get_all_pokemons.return_value = [(1, "Foo", "", "Bar")]
    assert len(helper.fetch_all_pokemons(connection_wrapper_mock)) == 1
