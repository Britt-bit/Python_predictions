"""
PokéAPI client — no API key: https://pokeapi.co/docs/v2
"""

from __future__ import annotations

import requests

API_ROOT = "https://pokeapi.co/api/v2"
POKEMON_LIST = f"{API_ROOT}/pokemon"

REQUEST_TIMEOUT = 30


def normalize_identifier(raw: str) -> str:
    """Strip whitespace and lowercase for PokéAPI Pokémon names."""
    return raw.strip().lower()


def fetch_pokemon(name: str) -> dict | None:
    """GET /pokemon/{name-or-id}. Returns None if not found (404)."""
    slug = normalize_identifier(name)
    if not slug:
        return None
    url = f"{POKEMON_LIST}/{slug}"
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def fetch_pokemon_page(limit: int, offset: int) -> dict:
    """GET /pokemon?limit=&offset= returns API JSON (results, count, next, …)."""
    response = requests.get(
        POKEMON_LIST,
        params={"limit": limit, "offset": offset},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def print_pokemon(data: dict) -> None:
    print("Name:", data["name"])
    for slot in data.get("types", []):
        t = slot.get("type") or {}
        print("Type:", t.get("name", "?"))
    species = data.get("species") or {}
    print("Species:", species.get("name", "?"))


def main() -> None:
    choice = input(
        "What do you want to do, show one Pokémon or list many? (one / all): "
    ).strip().lower()

    if choice == "all":
        limit = 20
        offset = 0
        while True:
            payload = fetch_pokemon_page(limit=limit, offset=offset)
            for entry in payload.get("results", []):
                print(entry.get("name", "?"))

            see_more = input("See the next page? (y/n): ").strip().lower()
            if see_more != "y":
                break
            offset += limit

    elif choice == "one":
        user_pick = input("Choose your Pokémon: ").strip()
        data = fetch_pokemon(user_pick)
        if data is None:
            print("Pokémon not found.")
            return
        print_pokemon(data)
    else:
        print("Please type 'one' or 'all'.")


if __name__ == "__main__":
    main()
