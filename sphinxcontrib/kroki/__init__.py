"""
Kroki integration into sphinx

Embed PlantUML, DOT, etc. diagrams in your documentation using Kroki.
"""
# copyright: Copyright 2020 by Martin Hasoň <martin.hason@gmail.com>
# license: MIT, see LICENSE for details.

from typing import Any, Dict
from sphinx.application import Sphinx
from .kroki import Kroki
from .transform import KrokiToImageTransform

__version__ = "1.3.1"


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_directive("kroki", Kroki)
    app.add_transform(KrokiToImageTransform)
    app.add_config_value("kroki_url", "https://kroki.io", "env")
    app.add_config_value("kroki_output_format", "svg", "env")
    app.add_config_value("kroki_inline_svg", False, "env")
    app.add_config_value("kroki_use_placeholder_on_request_error", False, "env")

    return {"version": __version__, "parallel_read_safe": True}
