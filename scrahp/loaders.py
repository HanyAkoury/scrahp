from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader
from unidecode import unidecode


def remove_accents(value: str) -> str:
    return unidecode(value)


class Loader(ItemLoader):
    default_input_processor = MapCompose(remove_accents)
