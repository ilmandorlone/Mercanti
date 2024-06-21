# app/routers/tokens.py
from fastapi import APIRouter
from typing import List
from ..schemas import TokenSchema
from ..crud import get_tokens, update_tokens

router = APIRouter()

@router.get("/tokens", response_model=List[TokenSchema])
def read_tokens():
    return get_tokens()

@router.put("/tokens", response_model=List[TokenSchema])
def update_tokens_state(tokens: List[TokenSchema]):
    update_tokens(tokens)
    return get_tokens()
