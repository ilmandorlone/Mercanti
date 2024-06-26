from typing import List
from core.actions.action_select_tokens import ActionSelectTokens
from core.actions.action_purchase_card import ActionPurchaseCard
from core.actions.action_reserve_card import ActionReserveCard
from core.models import Player, Card, Token, LevelDeck, CardCount, Passenger
from .schemas import CardSchema, TokenSchema, TokenActionSchema, PassengerSchema
import json
import random
from collections import Counter
import logging
from core.provider import provider_instance
from core.models import Player, Card, Token, Passenger
from core.match import Match

logger = logging.getLogger(__name__)
current_match : Match = None

def init_match(file_path: str):
    global current_match

    players = [ provider_instance.create_player("Player 1", 1),
                provider_instance.create_player("Player 2", 2) ]
    
    current_match = provider_instance.new_match(players)
    current_match.load_cards(file_path)

def get_game_state_by_id(player_id: int):
    global current_match

    main_player = None
    opponents = []

    for player in current_match.players:
        # Se i dati dei giocatori sono inizializzati correttamente, non è necessario questo conteggio
        cards_count = player.cards_count
        
        if player.id == player_id:
            main_player = Player(
                id=player.id,
                name=player.name,
                cards_count=cards_count,
                tokens=player.tokens,
                reserved_cards=player.reserved_cards,
                reserved_cards_count=len(player.reserved_cards),
                points=player.points
            )
        else:
            opponent = Player(
                id=player.id,
                name=player.name,
                cards_count=cards_count,
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
        "tokens": current_match.tokens,
        "remaining_cards": {
            "level1": len(current_match.deck_level1),
            "level2": len(current_match.deck_level2),
            "level3": len(current_match.deck_level3)
        },
        "visible_level1": [Card(**card.dict()) for card in current_match.visible_level1],
        "visible_level2": [Card(**card.dict()) for card in current_match.visible_level2],
        "visible_level3": [Card(**card.dict()) for card in current_match.visible_level3],
        "visible_passengers": [Passenger(**passenger.dict()) for passenger in current_match.visible_passengers],
    }

def purchase_card(player_id: int, card_id: int):
    action = ActionPurchaseCard(current_match, player_id, card_id)
    action.execute()

def reserve_card(player_id: int, level: int, card_id: int):
    # Se non è specificato l'id della carta, recupera l'id della carta dal livello specificato
    if not card_id:
        # Recupera l'id della carta dal livello specificato
        card_id = current_match.get_next_card_id_by_level(level)

    action = ActionReserveCard(current_match, player_id, card_id)
    action.execute()

def select_token(player_id: int, token_actions: List[TokenActionSchema]):
    action = ActionSelectTokens(current_match, player_id, token_actions)
    action.execute()