"""Tests for the Material You theme CSS generated from a background image."""

import re
from io import BytesIO

import pytest

HEX_COLOR_RE = re.compile(r"#[0-9a-f]{6}(?:[0-9a-f]{2})?", re.IGNORECASE)
DECLARED_VARIABLE_RE = re.compile(
    r"^  (?P<name>--md-sys-color-[a-z0-9-]+): (?P<value>#[0-9a-f]{6}(?:[0-9a-f]{2})?);$",
    re.IGNORECASE | re.MULTILINE,
)


def _solid_png(color: tuple[int, int, int], size: tuple[int, int] = (32, 32)) -> bytes:
    """Encode a solid-color image in memory as PNG bytes."""
    from PIL import Image

    buffer = BytesIO()
    Image.new("RGB", size, color).save(buffer, format="PNG")
    return buffer.getvalue()


def _declared_variables(css: str) -> dict[str, str]:
    """Collect the custom properties declared in the generated stylesheet."""
    return {
        match["name"]: match["value"] for match in DECLARED_VARIABLE_RE.finditer(css)
    }


@pytest.mark.parametrize(
    ("color_name", "expected"),
    [
        ("OnPrimaryContainer", "--md-sys-color-on-primary-container"),
        ("SurfaceContainerHighest", "--md-sys-color-surface-container-highest"),
        ("SurfaceDim", "--md-sys-color-surface-dim"),
        ("Primary", "--md-sys-color-primary"),
        ("primary", "--md-sys-color-primary"),
    ],
)
def test_css_variable_name_kebab_cases_color_names(
    cnrail_plugin: object,
    color_name: str,
    expected: str,
) -> None:
    """Camel case color names become kebab case custom properties without stray dashes."""
    from nonebot_plugin_cnrail import colors

    assert colors._css_variable_name(color_name) == expected


def test_generate_theme_css_keeps_background_rule_and_root_block(
    cnrail_plugin: object,
) -> None:
    """The stylesheet keeps the background rule and declares hex color variables."""
    from nonebot_plugin_cnrail import colors

    css = colors.generate_theme_css(_solid_png((200, 30, 60)))

    assert colors.BACKGROUND_CSS in css
    assert ":root {" in css
    assert css.endswith("}")

    variables = _declared_variables(css)

    assert variables
    assert all(HEX_COLOR_RE.fullmatch(value) for value in variables.values())


def test_generate_theme_css_declares_every_material_color_once(
    cnrail_plugin: object,
) -> None:
    """Every Material You color name is exported exactly once by the shared palette."""
    from materialyoucolor.dynamiccolor.material_dynamic_colors import COLOR_NAMES
    from nonebot_plugin_cnrail import colors

    css = colors.generate_theme_css(_solid_png((200, 30, 60)))

    declared = _declared_variables(css)

    assert set(declared) == {colors._css_variable_name(name) for name in COLOR_NAMES}
    assert len(declared) == len(COLOR_NAMES)
    assert all(
        getattr(colors.MATERIAL_COLORS, name, None) is not None for name in COLOR_NAMES
    )


def test_generate_theme_css_is_deterministic_for_identical_background(
    cnrail_plugin: object,
) -> None:
    """Identical background bytes always produce the very same stylesheet."""
    from nonebot_plugin_cnrail import colors

    background = _solid_png((200, 30, 60))

    assert colors.generate_theme_css(background) == colors.generate_theme_css(
        background
    )


def test_generate_theme_css_follows_the_background_color(
    cnrail_plugin: object,
) -> None:
    """A different background color yields a different palette."""
    from nonebot_plugin_cnrail import colors

    reddish = colors.generate_theme_css(_solid_png((200, 30, 60)))
    bluish = colors.generate_theme_css(_solid_png((20, 60, 200)))

    assert reddish != bluish


def test_quantize_background_reports_population_per_palette_color(
    cnrail_plugin: object,
) -> None:
    """Quantizing a solid image counts all of its pixels under the image color."""
    from nonebot_plugin_cnrail import colors

    palette = colors._quantize_background(_solid_png((200, 30, 60)))

    assert len(palette) == 1

    packed_color, population = next(iter(palette.items()))

    assert isinstance(packed_color, int)
    assert packed_color & 0xFFFFFF == 0xC81E3C
    assert population == 32 * 32


def test_palette_helpers_accept_the_same_raw_bytes_repeatedly(
    cnrail_plugin: object,
) -> None:
    """Both palette helpers decode raw bytes on every call and stay stable."""
    from nonebot_plugin_cnrail import colors

    background = _solid_png((200, 30, 60))

    assert colors._quantize_background(background) == colors._quantize_background(
        background,
    )
    assert colors._get_source_color(background) == colors._get_source_color(background)


def test_get_source_color_returns_a_palette_color_of_the_image(
    cnrail_plugin: object,
) -> None:
    """The source color is one of the quantized colors of the image."""
    from nonebot_plugin_cnrail import colors

    background = _solid_png((200, 30, 60))
    source_color = colors._get_source_color(background)

    assert isinstance(source_color, int)
    assert source_color in colors._quantize_background(background)
    assert source_color & 0xFFFFFF == 0xC81E3C
