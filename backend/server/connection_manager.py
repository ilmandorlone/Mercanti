import json
import logging
from fastapi import WebSocket

from core.match import Match
from core.models import Card, Noble, Player
from core.provider import provider_instance

logger = logging.getLogger(__name__)

def get_game_state_by_id(player_id: int):
    main_player = None
    opponents = []

    for player in provider_instance.current_match.context.deck_level3:        
        if player.id == player_id:
            main_player = Player(
                id=player.id,
                name=player.name,
                cards_count=player.cards_count,
                tokens=player.tokens,
                reserved_cards=player.reserved_cards,
                reserved_cards_count=len(player.reserved_cards),
                points=player.points
            )
        else:
            opponent = Player(
                id=player.id,
                name=player.name,
                cards_count=player.cards_count,
                tokens=player.tokens,
                reserved_cards=[],
                reserved_cards_count=len(player.reserved_cards),
                points=player.points
            )
            opponents.append(opponent)

    if main_player is None:
        raise ValueError(f"Player with id {player_id} not found")

    return {
        "player": main_player,
        "opponents": opponents,
        "tokens": provider_instance.current_match.context.tokens,
        "remaining_cards": {
            "level1": len(provider_instance.current_match.context.deck_level1),
            "level2": len(provider_instance.current_match.context.deck_level2),
            "level3": len(provider_instance.current_match.context.deck_level3)
        },
        "visible_level1": [Card(**card.dict()) for card in provider_instance.current_match.context.visible_level1],
        "visible_level2": [Card(**card.dict()) for card in provider_instance.current_match.context.visible_level2],
        "visible_level3": [Card(**card.dict()) for card in provider_instance.current_match.context.visible_level3],
        "visible_passengers": [Noble(**passenger.dict()) for passenger in provider_instance.current_match.context.visible_passengers],
    }

def generate_game_state_dict(player_id: int):
    game_state = get_game_state_by_id(player_id)
    return {
        "player": game_state["player"].dict(),
        "opponents": [opponent.dict() for opponent in game_state["opponents"]],
        "tokens": [token.dict() for token in game_state["tokens"]],
        "remaining_cards": game_state["remaining_cards"],
        "visible_level1": [card.dict() for card in game_state["visible_level1"]],
        "visible_level2": [card.dict() for card in game_state["visible_level2"]],
        "visible_level3": [card.dict() for card in game_state["visible_level3"]],
        "visible_passengers": [passenger.dict() for passenger in game_state["visible_passengers"]]
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
            game_state_dict = generate_game_state_dict(player_id)
            await self.send_message(json.dumps(game_state_dict), websocket)

connection_manager = ConnectionManager()