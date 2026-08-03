from pathlib import Path

import pytz
from cookit import DebugFileWriter

TZ_SHANGHAI = pytz.timezone("Asia/Shanghai")
debug = DebugFileWriter(Path.cwd() / "debug", "cnrail")
