from backend.core.models import Player
import asyncio
import websockets
import json

class AIPlayer:
    def __init__(self, player_model):
        self.player = Player()

    async def connect_websocket(self):
        async with websockets.connect(self.websocket_url) as websocket:
            await self.request_game_state(websocket)
            async for message in websocket:
                await self.handle_message(message)

    async def request_game_state(self, websocket):
        message = {
            "action": "get_game_state",
            "player_id": self.player_id
        }
        await websocket.send(json.dumps(message))

    async def handle_message(self, message):
        data = json.loads(message)
        if "player" in data:
            self.game_state = data

    def get_possible_actions(self, game_state):
        # Implementa la logica per generare una lista di possibili azioni
        possible_actions = []
        # Aggiungi logica per determinare le azioni possibili
        # Ad esempio, considera le mosse legali basate sullo stato del gioco
        # possible_actions.append("some_action")
        return possible_actions

    def make_move(self, game_state):
        pass

    def prepare_inputs(self, game_state, possible_actions):
        # Prepara gli input per il modello AI includendo le azioni possibili
        pass

    def select_action(self, outputs, possible_actions):
        # Seleziona l'azione basata sui risultati del modello e le azioni possibili
        pass
