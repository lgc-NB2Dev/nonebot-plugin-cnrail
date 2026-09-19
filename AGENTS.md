# AGENTS.md

First: This project expects the working root to be github repo `lgc-NB2Dev/workspace` because some recommended workspace-level files is not stored in this plugin project. If you are not working from that root, stop and notify the user.

## Commands

NOTE: The following command are expected to be run under the plugin repo root rather than the workspace root.

```bash
poe test [...]      # pytest
poe coverage [...]  # pytest (with branch coverage and terminal report)
```

## Structure

```text
nonebot_plugin_cnrail/  12306 train timetable query plugin package
  __init__.py           Plugin metadata, `require` calls and `__version__`
  __main__.py           `train` command matcher, date parsing and query flow
  config.py             Pydantic `ConfigModel` and shared config instance
  colors.py             Monet dynamic color scheme and CSS variable generation
  data_source.py        RailGo v1/v2 API queries and word generation
  models.py             Pydantic models for RailGo responses and train info
  render.py             Jinja and Playwright rendering of the result image
  utils.py              Shanghai timezone and debug file writer
  res/                  Bundled render resources
    assets/             Page stylesheet and layout script
    templates/          Jinja2 template for the train table
tests_nbp_cnrail/       Pytest suite: one module per source file, or a directory named after it
  utils/                Shared test scaffolding: fake RailGo API, clock pinning, fixture builders
.github/workflows/      CI test matrix and PyPI publish workflows
```

## Rules

- Keep test coverage as high as possible to avoid dead code. Code included in the current runtime's coverage scope should be covered unless it is version-specific, dependency-gated, or an intentional error path that is impractical to trigger safely.

## Gotchas

### Pydantic compatibility

- `models.py` must work on pydantic v1 and v2: v2 uses `populate_by_name` (valid for every 2.x), v1 the equivalent `allow_population_by_field_name`. `validate_by_alias` / `validate_by_name` exist from pydantic 2.11 only, and v1 forwards unknown config keys to `type()` and raises `TypeError` at import.

- `poe check` never sees the v1 branch: the workspace config sets `defineConstant = { PYDANTIC_V2 = true }`, so pyright prunes the `else` branch. Verify pydantic v1 changes by running the suite against `pydantic<2` (as the CI matrix does), not by type checking.

### Testing

- CI installs no Playwright browsers, so `render.py` tests stub `render.get_new_page` with a fake page (`tests_nbp_cnrail/utils/render_fakes.py`) instead of launching Chromium.

- `use_cmd_start=True` makes the command-start prefix mandatory, so only `/train`, `/列车信息` and `/查询列车` trigger the matcher, although `usage` and the README show a bare `train -h`.

- `on_alconna(..., auto_send_output=False)` is deliberate: alconna's default (`alconna_auto_send_output` unset → auto-send on) lets the rule answer parse errors itself and skip the matcher, so the `train -h` hint in the first handler would never reach users.

- `parse_date` parses month/day strings against a placeholder leap year (`NEUTRAL_YEAR`) and then rewrites the year to a candidate, because a year-less `strptime` fills in 1900 and can never parse `02-29` (that parsing is also deprecated since Python 3.14 and changes in 3.15).
