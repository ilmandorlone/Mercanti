from typing import List
import random
import os
import sys

# Determina il percorso della directory principale del progetto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Aggiungi il percorso al sys.path
sys.path.append(project_root)

from core.actions.action import Action
from core.actions.action_purchase_card import ActionPurchaseCard
from core.actions.action_select_tokens import ActionSelectTokens
from core.actions.action_reserve_card import ActionReserveCard
from core.actions.get_all_possible_actions import get_all_possible_actions
from core.cpu_player import CPUPlayer
from core.models import Player
from core.match import Match
from core.models import TokenAction, TokenActionEnum, ColorEnum

# callback player play
def player_move(match: Match, player: Player):
    # Ottiene tutte le azioni possibili per il giocatore
    actions = get_all_possible_actions(match, player.id)

    # Stampa il round corrente
    print(f"Round: {match.round}")
    # Stampa la lista di gettoni disponibili
    print(f"tokens: {', '.join([f'{t.color} x{t.count}' for t in player.tokens])}")

    # Verifica se ci sono azioni disponibili
    if not actions:
        print(f"Player {player.name} has no available actions")
        return

    # Esegue un'azione random tra quelle disponibili
    action = random.choice(actions)

    # Print dell'azione eseguita
    if isinstance(action, ActionSelectTokens):
        print(f"Player {player.name} selected tokens: {', '.join([f'{a.color} x{a.count}' for a in action.token_actions])}")
    elif isinstance(action, ActionPurchaseCard):
        print(f"Player {player.name} purchased card: {action.card_id}")
    elif isinstance(action, ActionReserveCard):
        print(f"Player {player.name} reserved card: {action.card_id}")
    
    try:
        action.execute()
    except Exception as e:
        print(f"Error: {e}")
        raise e

    # Crea una lista di punti dei giocatori
    players_points = [f"{p.name}: {p.points}" for p in match.players]
    print(f"Players points: {', '.join(players_points)}")

    print("")

    pass

# Crea una lista di giocatori CPU
players = [CPUPlayer(id=0, name="AI Player 1"),
           CPUPlayer(id=1, name="AI Player 2"),
           CPUPlayer(id=2, name="AI Player 3")]

# Crea una nuova partita
match = Match(players)
match.load_cards("backend/core/setup.json")

# Imposta la callback per il turno del giocatore
match.set_player_move_callback(player_move)

players[0].set_callback_move(player_move)
players[1].set_callback_move(player_move)
players[2].set_callback_move(player_move)

# Avvia la partita e determina il vincitore
winner = match.run()

print(f"Winner is {winner.name} with {winner.points} points")





'''

# example of how to select tokens
get_token = [ TokenAction(action=TokenActionEnum.BUY, color=ColorEnum.VIOLET, count=1),
              TokenAction(action=TokenActionEnum.BUY, color=ColorEnum.BLACK, count=1),
              TokenAction(action=TokenActionEnum.BUY, color=ColorEnum.RED, count=1) ]
ActionSelectTokens(match=match, player_id=0, token_actions=get_token).execute()

# example of how to purchase a card
ActionPurchaseCard(match=match, player_id=0, card_id=0).execute()

# example of how to reserve a card
ActionReserveCard(match=match, player_id=0, card_id=0).execute()

# example of how to reserve a card from the back
card_id = match.get_next_card_id_by_level(level=1)
ActionReserveCard(match=match, player_id=0, card_id=card_id).execute()

# example of how to get the game state
game_state = match.get_game_state_by_id(player_id=0)'''