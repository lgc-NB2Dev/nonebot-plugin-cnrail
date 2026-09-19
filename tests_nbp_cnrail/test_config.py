"""Tests for the plugin configuration model."""

import pytest
from pydantic import ValidationError


def test_config_default_acg_image_url_points_at_loliapi(
    cnrail_plugin: object,
) -> None:
    """The ACG image URL defaults to the public loliapi endpoint as a plain string."""
    from nonebot.compat import type_validate_python
    from nonebot_plugin_cnrail.config import ConfigModel

    default = type_validate_python(ConfigModel, {}).CNRAIL_ACG_IMAGE_URL

    assert type(default) is str
    assert default == "https://www.loliapi.com/acg/pe/"


@pytest.mark.parametrize(
    "url",
    ["http://example.test/acg", "https://example.test/acg/pe"],
)
def test_config_accepts_plain_http_urls(cnrail_plugin: object, url: str) -> None:
    """The ACG image URL accepts both http and https values, keeping them strings."""
    from nonebot_plugin_cnrail.config import ConfigModel

    value = ConfigModel(CNRAIL_ACG_IMAGE_URL=url).CNRAIL_ACG_IMAGE_URL

    assert type(value) is str
    assert value == url


@pytest.mark.parametrize(
    "url",
    ["not-a-url", "example.test/acg", "ftp://example.test/acg"],
)
def test_config_rejects_values_that_are_not_urls(
    cnrail_plugin: object,
    url: str,
) -> None:
    """A value that is not an http(s) URL is rejected by the field validator."""
    from nonebot_plugin_cnrail.config import ConfigModel

    with pytest.raises(ValidationError):
        ConfigModel(CNRAIL_ACG_IMAGE_URL=url)


def test_plugin_config_is_resolved_through_nonebot(cnrail_plugin: object) -> None:
    """The module exposes the plugin configuration resolved by NoneBot."""
    from nonebot_plugin_cnrail.config import ConfigModel, config

    assert isinstance(config, ConfigModel)
