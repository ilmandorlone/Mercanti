from core.models import ListCardCount, ListTokenCount, Player

class Utils:

    # Restituisce il valore di un attributo di un oggetto dato il nome dell'attributo
    @staticmethod
    def get_value_of_object_from_name(obj, mame_of_attribute):
        return getattr(obj, mame_of_attribute)
    
    # Setta il valore di un attributo di un oggetto dato il nome dell'attributo
    @staticmethod
    def set_value_of_object_from_name(obj, name_of_attribute, value):
        setattr(obj, name_of_attribute, value)

    # Somma tutte le variabili intere di un oggetto se sono intere
    @staticmethod
    def sum_object_attributes(obj):
        return sum(value for value in obj.__dict__.values() if isinstance(value, int))