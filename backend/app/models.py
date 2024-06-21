# app/models.py
from typing import List
from pydantic import BaseModel

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
