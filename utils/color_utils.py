from colorthief import ColorThief
from io import BytesIO

def extract_palette(image_bytes: bytes, color_count: int = 5):
    image_stream = BytesIO(image_bytes)
    color_thief = ColorThief(image_stream)
    dominant = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=color_count)

    # Convert RGB to hex
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

    return {
        "dominant": rgb_to_hex(dominant),
        "palette": [rgb_to_hex(c) for c in palette]
    }
