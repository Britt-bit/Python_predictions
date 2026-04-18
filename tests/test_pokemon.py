from unittest.mock import MagicMock, patch

from tryout.pokemon.client import (
    REQUEST_TIMEOUT,
    fetch_pokemon,
    fetch_pokemon_page,
    normalize_identifier,
)


def test_normalize_identifier_trims_and_lowercases() -> None:
    assert normalize_identifier("  Pikachu  ") == "pikachu"


def test_normalize_identifier_empty() -> None:
    assert normalize_identifier("   ") == ""


@patch("tryout.pokemon.client.requests.get")
def test_fetch_pokemon_page_uses_query_params(mock_get: MagicMock) -> None:
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "count": 2,
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
        ],
    }
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    data = fetch_pokemon_page(limit=2, offset=0)

    mock_get.assert_called_once()
    assert mock_get.call_args[0][0] == "https://pokeapi.co/api/v2/pokemon"
    kwargs = mock_get.call_args[1]
    assert kwargs["params"] == {"limit": 2, "offset": 0}
    assert kwargs["timeout"] == REQUEST_TIMEOUT
    assert [r["name"] for r in data["results"]] == ["bulbasaur", "ivysaur"]


@patch("tryout.pokemon.client.requests.get")
def test_fetch_pokemon_returns_none_on_404(mock_get: MagicMock) -> None:
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_get.return_value = mock_resp

    assert fetch_pokemon("missingmon") is None
    mock_get.assert_called_once()
    assert mock_get.call_args[0][0] == "https://pokeapi.co/api/v2/pokemon/missingmon"


@patch("tryout.pokemon.client.requests.get")
def test_fetch_pokemon_returns_json_on_success(mock_get: MagicMock) -> None:
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"name": "pikachu", "id": 25}
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    data = fetch_pokemon("pikachu")
    assert data == {"name": "pikachu", "id": 25}
    kwargs = mock_get.call_args[1]
    assert kwargs["timeout"] == REQUEST_TIMEOUT


@patch("tryout.pokemon.client.requests.get")
def test_fetch_pokemon_empty_name_returns_none(mock_get: MagicMock) -> None:
    assert fetch_pokemon("   ") is None
    mock_get.assert_not_called()
