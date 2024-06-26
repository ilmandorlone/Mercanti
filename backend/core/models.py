# core/models.py

from enum import Enum
from typing import List
from pydantic import BaseModel

class ColorEnum(str, Enum):
    VIOLET = "violet"
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    BLACK = "black"
    GOLD = "gold"

class Token(BaseModel):
    color: str
    count: int

class CardCount(BaseModel):
    color: str
    count: int

class Card(BaseModel):
    id: int
    level: int
    color: str
    cost: List[Token]
    points: int

class Passenger(BaseModel):
    id: int
    cost: List[Token]
    points: int

class Player(BaseModel):
    id: int
    name: str
    cards_count: List[CardCount] = []
    tokens: List[Token] = []
    reserved_cards: List[Card] = []
    reserved_cards_count: int = 0
    points: int
    passengers: List[Passenger] = []

class LevelDeck(BaseModel):
    cards: List[Card]
    available_count: int

class TokenActionEnum(Enum):
    RETURN = "return"
    BUY = "buy"

class TokenAction(BaseModel):
    color: str
    count: int
    action: str  # "buy" o "return"