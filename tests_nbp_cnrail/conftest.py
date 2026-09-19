import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(PLUGIN_ROOT))


def pytest_configure(config: pytest.Config) -> None:
    """Merge the NoneBug driver configuration with the other test packages' one."""
    from nonebug import NONEBOT_INIT_KWARGS

    init_kwargs = dict(config.stash.get(NONEBOT_INIT_KWARGS, {}))
    init_kwargs.update(
        {
            "driver": "~fastapi+~websockets+~httpx",
            "log_level": "DEBUG",
        },
    )
    config.stash[NONEBOT_INIT_KWARGS] = init_kwargs


@pytest.fixture
def cnrail_plugin(app: object) -> object:
    """Load the plugin so that its matchers and models are importable."""
    import nonebot

    if plugin := nonebot.get_plugin("nonebot_plugin_cnrail"):
        return plugin
    try:
        return nonebot.load_plugin("nonebot_plugin_cnrail")
    except RuntimeError as e:
        if "Plugin already exists" not in str(e):
            raise
    plugin = nonebot.get_plugin("nonebot_plugin_cnrail")
    if plugin is None:
        msg = "Plugin already exists but cannot be found by name"
        raise RuntimeError(msg)
    return plugin
