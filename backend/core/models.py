# core/models.py

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import List

class ColorEnum(str, Enum):
    VIOLET = "violet"
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    BLACK = "black"
    GOLD = "gold"

class TokenActionEnum(Enum):
    RETURN = "return"
    BUY = "buy"

@dataclass
class ListTokenCount():
    violet: int = 0
    blue: int = 0
    green: int = 0
    red: int = 0
    black: int = 0
    gold: int = 0

@dataclass
class Card():
    id: int
    level: int
    color: str
    cost: ListTokenCount
    points: int

@dataclass
class ListCardCount():
    violet: int = 0
    blue: int = 0
    green: int = 0
    red: int = 0
    black: int = 0

@dataclass
class Noble():
    id: int
    cost: ListCardCount
    points: int

class Player():
    def __init__(self, id: int, name: str, cards_count: ListCardCount, tokens: ListTokenCount, reserved_cards: List[Card], reserved_cards_count: int, points: int, passengers: List[Noble] = []):
        self.id: int = id
        self.name: str = name
        self.cards_count: ListCardCount = cards_count
        self.tokens: ListTokenCount = tokens
        self.reserved_cards: List[Card] = reserved_cards
        self.reserved_cards_count: int = reserved_cards_count
        self.points: int = points
        self.passengers: List[Noble] = passengers
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cards_count': asdict(self.cards_count) if is_dataclass(self.cards_count) else self.cards_count,
            'tokens': asdict(self.tokens) if is_dataclass(self.tokens) else self.tokens,
            'reserved_cards': [asdict(card) if is_dataclass(card) else card for card in self.reserved_cards],
            'reserved_cards_count': self.reserved_cards_count,
            'points': self.points,
            'passengers': [asdict(noble) if is_dataclass(noble) else noble for noble in self.passengers]
        }

@dataclass
class ContexMatch():
    players: List[Player]
    tokens: ListTokenCount
    deck_level1: List[Card]
    deck_level2: List[Card]
    deck_level3: List[Card]
    visible_level1: List[Card]
    visible_level2: List[Card]
    visible_level3: List[Card]
    visible_passengers: List[Noble]
    round: int

@dataclass
class LevelDeck():
    cards: List[Card]
    available_count: int

@dataclass
class TokenAction():
    action: TokenActionEnum
    color: str
    count: int

'''
# Metodo per la conversione a stringa della classe Card
def card_str(self: Card):
    return f"Card(id={self.id}, level={self.level}, color={self.color}, cost={self.cost}, points={self.points})"

# Metodo per la conversione a stringa della classe Card
Card.__str__ = card_str
Card.__repr__ = card_str

# Metodo per la conversione a stringa della classe ListCardCount
def list_card_count_str(self: ListCardCount):
    return f"ListCardCount(violet={self.violet}, blue={self.blue}, green={self.green}, red={self.red}, black={self.black})"

# Metodo per la conversione a stringa della classe ListCardCount
ListCardCount.__str__ = list_card_count_str
ListCardCount.__repr__ = list_card_count_str
'''