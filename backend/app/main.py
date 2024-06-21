import uvicorn
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import (
    SelectTokenActionSchema, SelectCardActionSchema,
    ReserveCardBackActionSchema, GetGameStateActionSchema,
    ReserveCardActionSchema
)
from app.crud import (
    load_cards, refill_visible_cards, refill_visible_passengers,
    get_game_state_by_id, purchase_card, reserve_card,
    select_token
)
import json
import os
import argparse

# Configura il logger
class FlushableFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', *args, **kwargs):
        super().__init__(filename, mode, *args, **kwargs)

    def emit(self, record):
        super().emit(record)
        self.flush()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    FlushableFileHandler("server.log", mode='a'),  # Append mode
    logging.StreamHandler()
])
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    cards_file_path = os.path.join(os.path.dirname(__file__), "cards.json")
    load_cards(cards_file_path)
    refill_visible_cards()
    refill_visible_passengers()
    logger.info("Loaded cards and refilled visible cards")

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Game Server"}

def reset_log():
    #with open("server.log", "w"):
        #pass
    pass

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

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received data from {websocket.client}: {data}")
            message = json.loads(data)
            player_id = message.get("player_id")

            if player_id is None:
                await websocket.send_text(json.dumps({"error": "player_id is required for websocket connection"}))
                continue  # Instead of closing, allow the client to resend the correct message

            manager.connect(websocket, player_id)

            if message["action"] == "select_token":
                action_schema = SelectTokenActionSchema(**message)
                player_id = action_schema.player_id
                token_actions = action_schema.tokens

                try:
                    select_token(player_id, token_actions)
                    logger.info(f"Player {player_id} performed token actions: {token_actions}")
                except ValueError as e:
                    logger.error(f"Error: {e}")
                    await websocket.send_text(json.dumps({"error": str(e)}))

            elif message["action"] == "purchase_card":
                action = SelectCardActionSchema(**message)
                player_id = action.player_id
                card_id = action.card_id

                try:
                    purchase_card(player_id, card_id)
                    logger.info(f"Player {player_id} purchased card {card_id}")
                except ValueError as e:
                    logger.error(f"Error: {e}")
                    await websocket.send_text(json.dumps({"error": str(e)}))

            elif message["action"] == "reserve_card":
                card_id = message.get("card_id", None)
                action = ReserveCardActionSchema(action=message["action"], player_id=message["player_id"], level=message["level"])
                player_id = action.player_id
                level = action.level

                try:
                    reserve_card(player_id, level, card_id)
                    logger.info(f"Player {player_id} reserved a card from level {level}")
                except ValueError as e:
                    logger.error(f"Error: {e}")
                    await websocket.send_text(json.dumps({"error": str(e)}))

            elif message["action"] == "reserve_card_back":
                action = ReserveCardBackActionSchema(**message)
                player_id = action.player_id
                level = action.level

                logger.info(f"Player {player_id} reserved a card back from level {level}")

            elif message["action"] == "get_game_state":
                if player_id is None:
                    logger.error("player_id is missing in the get_game_state action")
                    await websocket.send_text(json.dumps({"error": "player_id is missing"}))
                    continue

            # Broadcast the game state to all clients after handling the action
            await manager.broadcast_game_state()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A client disconnected")
        logger.warning(f"WebSocket disconnected: {websocket.client}")
    except Exception as e:
        logger.error(f"Error: {e}")
        manager.disconnect(websocket)
        await manager.broadcast("A client disconnected")
    finally:
        await websocket.close()
        logger.info(f"WebSocket closed: {websocket.client}")

def start_server(host: str, port: int):
    cards_file_path = os.path.join(os.path.dirname(__file__), "cards.json")
    load_cards(cards_file_path)
    refill_visible_cards()
    refill_visible_passengers()
    logger.info("Loaded cards and refilled visible cards")

    logger.info(f"Starting server at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=3333)
    args = parser.parse_args()

    start_server(args.host, args.port)
