# server/schemas.py
from pydantic import BaseModel
from typing import List

class TokenSchema(BaseModel):
    color: str
    count: int

class CardSchema(BaseModel):
    id: int
    level: int
    color: str
    cost: List[TokenSchema]
    points: int

class ListCardCountSchema(BaseModel):
    violet: int = 0
    blue: int = 0
    green: int = 0
    red: int = 0
    black: int = 0

class NobleSchema(BaseModel):
    id: int
    cost: ListCardCountSchema
    points: int

class PlayerSchema(BaseModel):
    id: int
    name: str
    cards_count: ListCardCountSchema = ListCardCountSchema(violet=0, blue=0, green=0, red=0, black=0)
    tokens: List[TokenSchema]
    reserved_cards: List[CardSchema]
    reserved_cards_count: int
    points: int
    passengers: List[NobleSchema] = []

class LevelDeckSchema(BaseModel):
    cards: List[CardSchema]
    available_count: int

class GameStateSchema(BaseModel):
    player: PlayerSchema
    opponents: List[PlayerSchema]
    tokens: List[TokenSchema]
    level1_deck: LevelDeckSchema
    level2_deck: LevelDeckSchema
    level3_deck: LevelDeckSchema
    visible_passengers: List[NobleSchema]

class SelectTokenActionSchema(BaseModel):
    action: str
    player_id: int
    tokens: List[TokenSchema]

class SelectCardActionSchema(BaseModel):
    action: str
    player_id: int
    card_id: int
    operation: str  # "purchase" or "reserve"

class ReserveCardBackActionSchema(BaseModel):
    action: str
    player_id: int
    level: int

class GetGameStateActionSchema(BaseModel):
    action: str
    player_id: int

class SelectCardActionSchema(BaseModel):
    action: str
    player_id: int
    card_id: int

class ReserveCardActionSchema(BaseModel):
    action: str
    player_id: int
    level: int
    card_id: int = None

class TokenActionSchema(BaseModel):
    color: str
    count: int
    action: str  # "buy" o "return"

class SelectTokenActionSchema(BaseModel):
    action: str  # "select_token"
    player_id: int
    tokens: List[TokenActionSchema]
