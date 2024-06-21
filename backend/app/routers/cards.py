# app/routers/cards.py
from fastapi import APIRouter
from typing import List
from ..schemas import CardSchema
from ..crud import get_cards, update_cards

router = APIRouter()

@router.get("/cards", response_model=List[CardSchema])
def read_cards():
    return get_cards()

@router.put("/cards", response_model=List[CardSchema])
def update_cards_state(cards: List[CardSchema]):
    update_cards(cards)
    return get_cards()
