# Copilot Instructions for espn-api (Basketball-Only)

These notes help AI coding agents be productive quickly in this repo by outlining the architecture, workflows, and project-specific conventions.

## Big Picture
- **Purpose:** Python library to access ESPN Fantasy APIs for basketball only. Provides `League`, `Team`, `Player`, `Matchup`, and box score abstractions.
- **Top-level package:** `espn_api/` with a basketball subpackage and shared utilities.
- **Core flow:**
  - Construct a sport-specific `League` (e.g., `from espn_api.football import League`).
  - League methods use `espn_api.requests.espn_requests` to make HTTP calls to ESPN endpoints.
  - Responses are parsed and mapped to domain objects (`Team`, `Player`, `Matchup`, box scores) per sport.
- **Why structure this way:** Each sport has differing endpoints and payload shapes; common naming and patterns keep the API consistent while allowing sport-specific parsing.

## Key Modules & Patterns
- `espn_api/requests/espn_requests.py`: Centralizes HTTP requests, constants, and error handling. Changes here affect all sports.
- `espn_api/utils/`: Shared helpers and logging (`logger.py`, `utils.py`). Prefer using these utilities over re-implementing helpers.
- `espn_api/base_*` files: Common abstract concepts used by sport-specific implementations.
- Sport package: `basketball/` with `league.py` exposing a `League` class with consistent init args: `league_id`, `year`, optional `espn_s2`, `swid`, `debug`.
- Common objects: `team.py`, `player.py`, `matchup.py`, `box_score.py`, `box_player.py`, `activity.py`.
- **Debugging convention:** Pass `debug=True` to `League(...)` to log raw requests/responses during issue reproduction (see README).

## Public API Expectations
- Import pattern:
  - `from espn_api.basketball import League`
- `League` commonly exposes methods & properties like `teams`, `free_agents`, `scoreboard`, `box_scores`, `settings` depending on sport. Preserve naming consistency across sports when adding features.
- Credentials for private leagues use `espn_s2` and `swid`. Ensure request layer uses these tokens when provided.

## Tests & Workflows
- **Runner:** `pytest` is recommended for Python >= 3.9. Run with `pytest` at repo root.
- **Structure:** Tests live under `tests/` by sport, with `integration/` (API behaviors) and `unit/` (parsing, models). Prefer unit tests when feasible; integration may require live data.
- **Legacy:** `nosetests` via `python setup.py nosetests` exists but is not recommended for >=3.9.
- **Coverage:** `codecov.yml` present; CI likely reports coverage.

## Environment & Dependencies
- Python >= 3.8 supported; >= 3.9 recommended with `pytest`.
- Local dev setup (Windows example):
  - `python -m venv .venv`
  - `.venv\Scripts\Activate.ps1`
  - `pip install -r requirementsV2.txt`
- Packaging files: `pyproject.toml`, `setup.cfg`, `setup.py`. For contributions, stick to `requirementsV2.txt` for dev installs.

## Conventions & Style
- Maintain consistent `League` init signature across sports: `league_id`, `year`, `espn_s2=None`, `swid=None`, `debug=False`.
- Keep domain object names aligned (`Team`, `Player`, `Matchup`, `BoxScore`, `BoxPlayer`). Avoid sport-specific naming unless necessary.
- Use `espn_api/requests/constant.py` for endpoint constants; do not hardcode URLs in sport modules.
- Log via `espn_api.utils.logger` and respect `debug` flag to control verbosity.
- Avoid adding external dependencies without updating `requirementsV2.txt` and tests.

## Common Tasks
- Adding a field parsed from ESPN:
  - Update sport-specific parser (e.g., `football/player.py`).
  - If endpoint changes, adjust `espn_api/requests/espn_requests.py` or constants.
  - Add/adjust unit tests under `tests/<sport>/unit/` for the entity.
- Implementing a new league method:
  - Add method on `League` in `league.py` with clear return types.
  - Reuse helpers in `utils.py`; ensure token handling if accessing private data.
  - Provide a small integration test if it queries live-like structures.

## Examples
- Basic usage:
```python
from espn_api.football import League
league = League(league_id=1245, year=2019, debug=True)
for team in league.teams:
    print(team.team_name, team.wins, team.losses)
```
- Private league:
```python
league = League(league_id=123, year=2024, espn_s2="<token>", swid="{<uuid>}" )
```

## Gotchas
- ESPN endpoints can change by season; prefer defensive parsing and default values.
- Integration tests may rely on current ESPN data; run selectively if rate-limits are a concern.
- Ensure `year` aligns with actual league season; mismatches produce empty or differing payloads.

## Where to Look
- Start in `espn_api/requests/espn_requests.py` to understand request flow.
- Review `espn_api/<sport>/league.py` and `constant.py` to learn sport-specific mappings.
- Check `tests/<sport>/unit/` to see expected object shapes and key behaviors.

---
If anything here is unclear or missing (e.g., preferred return shapes or a specific sport’s conventions), tell me which area to expand and I’ll refine these instructions.