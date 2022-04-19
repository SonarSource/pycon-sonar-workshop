from unittest.mock import Mock

from pokedex import helper


def test_fetch_all_pokemon():
    connection_wrapper_mock = Mock()
    connection_wrapper_mock.get_all_pokemons.return_value = [(1, "Foo", "", "Bar")]
    assert len(helper.fetch_all_pokemons(connection_wrapper_mock)) == 1


def test_fetch_pokemon():
    connection_wrapper_mock = Mock()
    mock_pokemon = (1, "Foo", "", "Bar")
    connection_wrapper_mock.get_single_pokemon.return_value = mock_pokemon
    assert helper.fetch_pokemon(connection_wrapper_mock, 1) == mock_pokemon
