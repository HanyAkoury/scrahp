from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader
from unidecode import unidecode


def remove_accents(value: str) -> str:
    """
    Remove accents from the input string.

    Args:
        value (str): A string possibly containing accented characters.

    Returns:
        str: The input string with accented characters replaced by their unaccented equivalents.
    """
    return unidecode(value)


class Loader(ItemLoader):
    """
    Custom ItemLoader with a default input processor.

    The default processor removes accents from all fields, ensuring consistent data formatting.
    """
    default_input_processor = MapCompose(remove_accents)
