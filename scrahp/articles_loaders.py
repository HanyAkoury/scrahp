from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from unidecode import unidecode
import pdb

def remove_accents(value):
    return unidecode(value)

class ArticleLoader(ItemLoader):
    default_input_processor = MapCompose(remove_accents)
