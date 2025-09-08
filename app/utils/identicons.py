import base64

import pydenticon


def generate_identicon(text, size: int):
    """Generate an identicon as a data URL."""
    foreground = [
        "rgb(45,79,255)",
        "rgb(254,180,44)",
        "rgb(226,121,234)",
        "rgb(30,179,253)",
        "rgb(232,77,65)",
        "rgb(49,203,115)",
        "rgb(141,69,170)",
    ]
    background = "rgb(224,224,224)"
    padding_size = size // 8
    padding = (padding_size, padding_size, padding_size, padding_size)
    block_size = 8

    generator = pydenticon.Generator(
        block_size, block_size, foreground=foreground, background=background
    )

    identicon = generator.generate(text, size, size, padding=padding)

    # returns a data URL for embedding in HTML
    identicon_base64 = base64.b64encode(identicon).decode("ascii")
    return f"data:image/png;base64,{identicon_base64}"
