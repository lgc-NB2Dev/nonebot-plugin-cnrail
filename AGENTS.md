# AGENTS.md

First: This project expects the working root to be github repo `lgc-NB2Dev/workspace` because some recommended workspace-level files is not stored in this plugin project. If you are not working from that root, stop and notify the user.

## Commands

This repo declares no `[tool.poe.tasks]` of its own; run workspace tasks such as `poe test` or `poe lint` from the workspace root. The release workflow builds with `uv build` and publishes with `uv publish` from the plugin repo root.

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
.github/workflows/      CI PyPI publish workflows
```

## Rules

- Keep test coverage as high as possible to avoid dead code. Code included in the current runtime's coverage scope should be covered unless it is version-specific, dependency-gated, or an intentional error path that is impractical to trigger safely.

## Gotchas

Currently empty
