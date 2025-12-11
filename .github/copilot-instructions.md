# Copilot Instructions for espn-api (Basketball)

Focused, repo-specific notes to make AI agents productive immediately.

## Big Picture
- **Scope:** Fantasy Basketball only. Public API centers on `League`, with domain objects `Team`, `Player`, `Matchup`, `BoxScore`, `BoxPlayer`, `Activity`, `Transaction`.
- **Architecture:** `espn_api/basketball/league.py` builds on `BasketballLeague` (`espn_api/basketball_league.py`) and calls `EspnFantasyRequests` (`espn_api/requests/espn_requests.py`). Responses map into sport-specific objects under `espn_api/basketball/`.
- **Why:** Basketball payload shapes differ by season; centralized request layer + sport parsers keep a stable public API while handling ESPN quirks.

## Key Modules
- `requests/espn_requests.py`: HTTP client, endpoints, cookies, and errors. Handles 401 by toggling between `/seasons/.../segments/0/leagues/{id}` and `/leagueHistory/{id}?seasonId={year}`. Raises `ESPNAccessDenied`, `ESPNInvalidLeague`, `ESPNUnknownError`. Debug logging via `Logger.log_request`.
- `requests/constant.py`: Base URLs and sport map (`nba -> fba`). Do not hardcode endpoints.
- `basketball_league.py`: Shared league plumbing (fetch league data, draft, teams, player map, pro schedule).
- `basketball/league.py`: Public `League` with methods like `teams`, `scoreboard`, `free_agents`, `box_scores`, `player_info`, `recent_activity`, `transactions`.
- `utils/logger.py`: Lightweight debug logger that prints full request/response JSON when `debug=True`.

## Public API & Usage
- Import: `from espn_api.basketball import League`
- Init signature: `League(league_id, year, espn_s2=None, swid=None, fetch_league=True, debug=False)`
  - Private leagues require cookies: `{'espn_s2': ..., 'SWID': ...}` (note `SWID` capitalization).
  - Set `debug=True` to log raw requests/responses.
- Examples:
```python
from espn_api.basketball import League
league = League(league_id=123456, year=2024, debug=True)
scores = league.scoreboard()
fas = league.free_agents(size=25)
boxes = league.box_scores(matchup_period=3)
```
```python
# Private league
league = League(league_id=123456, year=2024, espn_s2="<token>", swid="{<uuid>}")
```

## Behaviors & Conventions
- Year-specific logic: Older seasons (<2018) use different endpoints and some features are restricted (e.g., `free_agents`, `box_scores`, `recent_activity` raise if year < 2019).
- Consistent naming: Keep `Team`, `Player`, `Matchup`, `BoxScore`, `BoxPlayer` aligned; avoid sport-invented names.
- Extend via league methods in `basketball/league.py`; reuse helpers from `basketball_league.py` and the request client.
- Log via `utils/logger.py`; respect the `debug` flag; don’t introduce new logging systems.

## Dev Workflow
- Environment (Windows PowerShell):
  - `python -m venv .venv`
  - `.\.venv\Scripts\Activate.ps1`
  - `pip install -r requirementsV2.txt`
- Tests: `pytest` at repo root. Integration test in `tests/basketball/integration/test_league.py` is `@skip`ped; favor unit tests (e.g., `tests/espn_requests/test_access_denied.py`).
- Packaging files: `pyproject.toml`, `setup.cfg`, `setup.py`. Use `requirementsV2.txt` for local dev.

## When Editing
- Requests: Update `requests/espn_requests.py` and `requests/constant.py` together; preserve endpoint toggle and error semantics. Ensure `Logger.log_request` still receives full JSON.
- Parsers/Models: Modify basketball objects under `espn_api/basketball/`; keep return shapes stable. Prefer defensive parsing with defaults.
- Tokens: Always pass cookies as `espn_s2` and `SWID` when needed; surface `ESPNAccessDenied` if missing or unauthorized.
- Tests: Add unit tests under `tests/` mirroring patterns in `tests/espn_requests/`. Use `requests_mock` or `unittest.mock`.

## Pointers
- Start at `requests/espn_requests.py` to see how views/filters are requested (`x-fantasy-filter` headers, `view` params) and how responses are logged.
- Check `basketball/league.py` for how API views map to domain objects and for method-specific guards (e.g., year checks).
- Refer to `README.md` for quick usage and contributor notes (e.g., `BasketballLeague`, `BasketballSettings`, `BasketballPick`).

If anything is unclear (e.g., expected shapes for league methods or adding new filters), ask which area to expand and I’ll refine these instructions.