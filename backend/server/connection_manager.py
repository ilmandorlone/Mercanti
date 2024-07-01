from dataclasses import asdict, is_dataclass
import json
import logging
from typing import List
from fastapi import WebSocket

from server.schemas import CardSchema, NobleSchema, PlayerSchema, TokenSchema, CardColorCountSchema
from core.match import Match
from core.models import Card, ContextMatch, ListTokenCount, Noble, Player
from core.provider import provider_instance

logger = logging.getLogger(__name__)


def get_game_state_by_id(player_id: int):
    context: ContextMatch = provider_instance.current_match.context
    main_player = None
    opponents = []

    def convert_tokens_to_schema_list(token_count):
        return [TokenSchema(color=color, count=count) for color, count in vars(token_count).items()]

    def convert_cards_to_schema_list(cards):
        return [CardSchema(
            id=card.id,
            level=card.level,
            color=card.color,
            cost=convert_tokens_to_schema_list(card.cost),
            points=card.points
        ) for card in cards]
    
    def convert_color_count_to_schema_list(color_count):
        return [CardColorCountSchema(color=color, count=count) for color, count in vars(color_count).items()]
    
    def convert_nobles_to_schema_list(nobles):
        return [NobleSchema(
            id=noble.id,
            cost=convert_color_count_to_schema_list(noble.cost),
            points=noble.points
        ) for noble in nobles]

    for player in context.players:
        player_tokens = convert_tokens_to_schema_list(player.tokens)

        if player.id == player_id:
            main_player = PlayerSchema(
                id=player.id,
                name=player.name,
                tokens=player_tokens,
                cards_count=convert_color_count_to_schema_list(player.cards_count),
                reserved_cards=convert_cards_to_schema_list(card.card for card in player.reserved_cards),
                points=player.points,
                reserved_cards_count=len(player.reserved_cards)
            )
        else:
            opponent = PlayerSchema(
                id=player.id,
                name=player.name,
                tokens=player_tokens,
                cards_count=convert_color_count_to_schema_list(player.cards_count),
                points=player.points,
                reserved_cards_count=len(player.reserved_cards)
            )
            opponent.reserved_cards_count=len(player.reserved_cards)
            opponents.append(opponent)

    if main_player is None:
        raise ValueError(f"Player with id {player_id} not found")
    
    tokens = convert_tokens_to_schema_list(context.tokens)
    visible_cards_level1 = convert_cards_to_schema_list(context.visible_level1)
    visible_cards_level2 = convert_cards_to_schema_list(context.visible_level2)
    visible_cards_level3 = convert_cards_to_schema_list(context.visible_level3)
    nobles_visible = convert_nobles_to_schema_list(context.visible_passengers)

    return {
        "player": main_player.dict(),
        "opponents": [opponent.dict() for opponent in opponents],
        "tokens": [token.dict() for token in tokens],
        "remaining_cards": {
            "level1": len(context.deck_level1),
            "level2": len(context.deck_level2),
            "level3": len(context.deck_level3)
        },
        "visible_level1": [card.dict() for card in visible_cards_level1],
        "visible_level2": [card.dict() for card in visible_cards_level2],
        "visible_level3": [card.dict() for card in visible_cards_level3],
        "visible_passengers": [noble.dict() for noble in nobles_visible]

    }

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.player_connections: dict[WebSocket, int] = {}

    def connect(self, websocket: WebSocket, player_id: int):
        self.active_connections.append(websocket)
        self.player_connections[websocket] = player_id
        logger.info(f"Client connected: {websocket.client} as Player {player_id}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if websocket in self.player_connections:
            del self.player_connections[websocket]
        logger.info(f"Client disconnected: {websocket.client}")

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        logger.debug(f"Sent message to {websocket.client}: {message}")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
        logger.debug(f"Broadcast message: {message}")

    async def broadcast_game_state(self):
        for websocket, player_id in self.player_connections.items():
            game_state_dict = get_game_state_by_id(player_id)
            json_game_state = json.dumps(game_state_dict)
            await self.send_message(json_game_state, websocket)

connection_manager = ConnectionManager()