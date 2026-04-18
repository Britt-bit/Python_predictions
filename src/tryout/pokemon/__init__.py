"""PokéAPI client (https://pokeapi.co/docs/v2)."""

from tryout.pokemon.client import (
    API_ROOT,
    POKEMON_LIST,
    REQUEST_TIMEOUT,
    fetch_pokemon,
    fetch_pokemon_page,
    normalize_identifier,
    print_pokemon,
)

__all__ = [
    "API_ROOT",
    "POKEMON_LIST",
    "REQUEST_TIMEOUT",
    "fetch_pokemon",
    "fetch_pokemon_page",
    "normalize_identifier",
    "print_pokemon",
]
