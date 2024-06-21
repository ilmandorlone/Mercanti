# app/routers/players.py
from fastapi import APIRouter
from typing import List
from ..schemas import PlayerSchema
from ..crud import get_players, update_player

router = APIRouter()

@router.get("/players", response_model=List[PlayerSchema])
def read_players():
    return get_players()

@router.put("/players/{player_id}", response_model=PlayerSchema)
def update_player_state(player_id: int, player: PlayerSchema):
    updated_player = update_player(player_id, player)
    if updated_player:
        return updated_player
    return {"error": "Player not found"}
