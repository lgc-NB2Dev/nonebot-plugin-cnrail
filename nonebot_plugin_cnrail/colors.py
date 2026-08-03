from io import BytesIO
from re import sub

from materialyoucolor.dynamiccolor.material_dynamic_colors import (
    COLOR_NAMES,
    MaterialDynamicColors,
)
from materialyoucolor.hct.hct import Hct
from materialyoucolor.quantize import QuantizeCelebi
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from materialyoucolor.score.score import Score

BACKGROUND_CSS = '.bg-wrapper {\n  background-image: url("/bg");\n}'
MATERIAL_COLORS = MaterialDynamicColors(spec="2025")


def _quantize_background(background: bytes) -> dict[int, int]:
    from PIL import Image

    with Image.open(BytesIO(background)) as source:
        image = source.convert("RGB")
    try:
        image.thumbnail((128, 128))
        return QuantizeCelebi(list(image.getdata()), 128)
    finally:
        image.close()


def _get_source_color(background: bytes) -> int:
    return Score.score(_quantize_background(background))[0]


def _css_variable_name(color_name: str) -> str:
    kebab_name = sub(r"(?<!^)(?=[A-Z])", "-", color_name).lower()
    return f"--md-sys-color-{kebab_name}"


def generate_theme_css(background: bytes) -> str:
    scheme = SchemeTonalSpot(
        Hct(_get_source_color(background)),
        is_dark=False,
        contrast_level=0.0,
        spec_version="2025",
    )
    variables = "\n".join(
        f"  {_css_variable_name(name)}: {getattr(MATERIAL_COLORS, name).get_hex(scheme)};"
        for name in COLOR_NAMES
    )
    return f"{BACKGROUND_CSS}\n\n:root {{\n{variables}\n}}"
