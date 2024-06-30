from typing import List
from core.cpu_player import CPUPlayer
from core.actions.get_all_possible_actions import get_all_possible_actions
from core.actions.action_select_tokens import ActionSelectTokens
from core.actions.action_purchase_card import ActionPurchaseCard
from core.actions.action_reserve_card import ActionReserveCard
from core.models import Player, Card, LevelDeck, ListCardCount, Noble
from .schemas import CardSchema, TokenSchema, TokenActionSchema, NobleSchema
import json
import random
from collections import Counter
import logging
from core.provider import provider_instance
from core.match import Match
from server.connection_manager import connection_manager

logger = logging.getLogger(__name__)

def init_match(file_path: str):

    human_player = provider_instance.create_player(1, "Player 1")
    cpu_player = provider_instance.create_player(id=2, name="Player 2 CPU")

    players = [ human_player, cpu_player ]
    # Filtra i giocatori CPU
    cpu_players = [player for player in players if isinstance(player, CPUPlayer)]

    # Per ogni giocatore CPU, inizializza il callback per l'esecuzione delle mosse
    for cpu_player in cpu_players:
        cpu_player.set_callback_move(move_callback)
    
    provider_instance.current_match = provider_instance.new_match(players)
    provider_instance.current_match.load_cards(file_path)

    def move_callback(player: Player):
        # Ottiene tutte le azioni possibili per il giocatore
        actions = get_all_possible_actions(provider_instance.current_match, player.id)

        if actions:        
            # Esegue un'azione random tra quelle disponibili
            action = random.choice(actions)
            action.execute()
        
        connection_manager.broadcast_game_state()

def purchase_card(player_id: int, card_id: int):
    # Verifica il turno del giocatore
    if provider_instance.current_match.turn_manager.check_turn_id(player_id) is False:
        raise ValueError(f"Player with id {player_id} cannot play now")

    # Esegue l'azione di acquisto della carta
    action = ActionPurchaseCard(provider_instance.current_match, player_id, card_id)
    action.execute()

    # Termina il turno del giocatore
    provider_instance.current_match.turn_manager.end_turn(player_id)

def reserve_card(player_id: int, level: int, card_id: int):
    # Verifica il turno del giocatore
    if provider_instance.current_match.turn_manager.check_turn_id(player_id) is False:
        raise ValueError(f"Player with id {player_id} cannot play now")
    
    # Se non è specificato l'id della carta, recupera l'id della carta dal livello specificato
    if not card_id:
        # Verifica se c'è una carta disponibile nel livello specificato
        if not provider_instance.current_match.select_deck_level_by_level(level):
            raise ValueError(f"No cards available in level {level}")
        
        # Recupera l'id della carta dal livello specificato
        card_id = provider_instance.current_match.get_next_card_id_by_level(level)

    # Esegue l'azione di riserva della carta
    action = ActionReserveCard(provider_instance.current_match, player_id, card_id)
    action.execute()

    # Termina il turno del giocatore
    provider_instance.current_match.turn_manager.end_turn(player_id)

def select_token(player_id: int, token_actions: List[TokenActionSchema]):
    # Verifica il turno del giocatore
    if provider_instance.current_match.turn_manager.check_turn_id(player_id) is False:
        raise ValueError(f"Player with id {player_id} cannot play now")
    
    # Esegue l'azione di selezione dei token
    action = ActionSelectTokens(provider_instance.current_match, player_id, token_actions)
    action.execute()

    # Termina il turno del giocatore
    provider_instance.current_match.turn_manager.end_turn(player_id)