import base64

import pydenticon

BACKGROUND_COLOR = "#f3f4f6"
FOREGROUND_COLORS = [
    "#d56666",
    "#94ace7",
    "#a7d368",
    "#e180d5",
    "#7fe0d0",
    "#d3a268",
    "#a995e7",
    "#6bd566",
    "#d96e92",
    "#8ec5e6",
    "#cad368",
    "#d28ae4",
    "#74dca8",
    "#d47d67",
    "#969de8",
    "#90d467",
    "#de7abd",
    "#85dfe3",
    "#d3b868",
    "#b892e7",
    "#69d77b",
    "#d76876",
    "#92b6e7",
    "#b4d368",
    "#e284e2",
    "#7bdfc1",
    "#d49467",
    "#a096e7",
    "#79d567",
    "#db72a3",
    "#8bcfe5",
    "#d3ce68",
    "#c88de6",
    "#6fda97",
    "#d56f66",
    "#95a7e7",
    "#9ed468",
    "#e07ecc",
    "#82e1d9",
    "#d3aa68",
    "#af94e7",
    "#66d56a",
    "#d86c87",
    "#90bfe6",
    "#c2d368",
    "#d888e4",
    "#76ddb2",
    "#d48667",
    "#9696e8",
    "#88d467",
]
GRID_SIZE = 5

GENERATOR = pydenticon.Generator(
    GRID_SIZE,
    GRID_SIZE,
    foreground=FOREGROUND_COLORS,
    background=BACKGROUND_COLOR,
)


def generate_identicon(username: str, size: int):
    """Generate an identicon as a data URL."""
    padding_size = size // 8
    padding = (padding_size, padding_size, padding_size, padding_size)

    identicon = GENERATOR.generate(username, size, size, padding=padding)

    # returns a data URL for embedding in HTML
    identicon_base64 = base64.b64encode(identicon).decode("ascii")
    return f"data:image/png;base64,{identicon_base64}"
