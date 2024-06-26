from core.actions.action_purchase_card import ActionPurchaseCard
from core.actions.action_select_tokens import ActionSelectTokens
from core.actions.action_reserve_card import ActionReserveCard
from core.models import Player
from core.match import Match
from core.models import TokenAction, TokenActionEnum, ColorEnum

players = [Player(id=0, name="Player 1"), 
           Player(id=1, name="Player 2"),
           Player(id=2, name="Player 3")]

match = Match(players)

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
game_state = match.get_game_state_by_id(player_id=0)