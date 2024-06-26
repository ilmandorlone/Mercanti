from collections import Counter
from core.match import Match
from core.models import CardCount, Token, TokenActionEnum
from core.helpers.player_helper import PlayerHelper
from core.helpers.match_helper import MatchHelper
from core.actions.action import Action

# Implementazione della classe ActionSelectTokens che eredita da Action
class ActionSelectTokens(Action):
    def __init__(self, match: Match, player_id: int, token_actions):
        super().__init__(player_id)
        self.token_actions = token_actions
        self.match = match


    def _validate_actions(self):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id(self.match, self.player_id)
        
        # Lista di azioni di gettoni "buy" selezionate dal giocatore
        buy_actions = [action for action in self.token_actions if action.action == TokenActionEnum.BUY.value]

        # Lista di azioni di gettoni "return" che il giocatore intende restituire
        return_actions = [action for action in self.token_actions if action.action == TokenActionEnum.RETURN.value]

        # Calcola il numero totale di gettoni che il giocatore intende selezionare "buy"
        total_tokens_to_buy = sum(action.count for action in buy_actions)
        
        # Verifica che il giocatore non abbia selezionato più di 3 gettoni per l'acquisto
        if total_tokens_to_buy > 3:
            raise ValueError("Cannot buy more than 3 tokens at a time")

        # Calcola il numero totale di gettoni che il giocatore intende restituire "return"
        total_tokens_to_return = sum(action.count for action in return_actions)

        # Calcola la differenza tra i gettoni che il giocatore intende selezionare e restituire
        total_tokens_diff = total_tokens_to_buy - total_tokens_to_return

        # Calcola il numero totale di gettoni del giocatore dopo l'azione
        total_tokens_after_action = sum(token.count for token in player.tokens) + total_tokens_diff

        # Verifica che la somma dei gettoni non superi 10
        if total_tokens_after_action > 10:
            raise ValueError("Cannot have more than 10 tokens in total after the action")
        
        # Verifica che i colori dei gettoni selezionati per l'acquisto siano validi
        buy_colors = [action.color for action in buy_actions]
        return_colors = [action.color for action in return_actions]

        # Verifica che non ci siano gettoni "gold" tra quelli selezionati per l'acquisto o tra quelli restituiti
        if "gold" in buy_colors + return_colors:
            raise ValueError("Cannot buy or return gold tokens")

        # Verifica se il giocatore ha selezionato 2 uguali
        if total_tokens_to_buy == 2 and len(buy_colors) == 1:

            # Il giocatore ha selezionato 2 gettoni dello stesso colore
            
            # Verifica che ci siano almeno 4 gettoni disponibili di quel colore
            available_token = next((t for t in self.match.tokens if t.color == buy_colors[0]), None)
            if not available_token or available_token.count < 4:
                raise ValueError("There must be at least 4 tokens available of the selected color to buy 2")
        else:
            # Il giocatore ha selezionato 3 gettoni di colori diversi

            # Verifica che non ci siano più di 1 gettone di un colore selezionato per l'acquisto
            if any(count > 1 for count in Counter(buy_colors).values()):
                raise ValueError("Cannot buy more than 1 token of the same color when buying different colors")

            # Verifica che per ogni colore selezionato ci siano almeno 1 gettone disponibile
            for color in buy_colors:
                available_token = next((t for t in self.match.tokens if t.color == color), None)
                if not available_token or available_token.count < 1:
                    raise ValueError(f"There must be at least 1 token available of color {color} to buy 3")

            # Verifica che i colori siano tutti diversi
            if len(buy_colors) != len(set(buy_colors)):
                raise ValueError("If buying 3 tokens, they must be of different colors")

    def can_execute(self):
        try:
            self._validate_actions()
            return True
        except ValueError:
            return False

    def execute(self):
        # Verifica che le azioni siano valide
        self._validate_actions()

        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id(self.match, self.player_id)

        # Processa ogni azione
        for action in self.token_actions:
            table_token = next((t for t in self.match.tokens if t.color == action.color), None)
            player_token = next((t for t in player.tokens if t.color == action.color), None)

            if action.action == TokenActionEnum.BUY.value:
                if table_token and table_token.count >= action.count:
                    table_token.count -= action.count
                    if player_token:
                        player_token.count += action.count
                    else:
                        player.tokens.append(Token(color=action.color, count=action.count))
                else:
                    raise ValueError(f"Not enough tokens available for color {action.color}")

            elif action.action == TokenActionEnum.RETURN.value:
                if player_token and player_token.count >= action.count:
                    player_token.count -= action.count
                    if table_token:
                        table_token.count += action.count
                    else:
                        self.match.tokens.append(Token(color=action.color, count=action.count))
                else:
                    raise ValueError(f"Not enough tokens to return for color {action.color}")

            else:
                raise ValueError("Invalid action. Must be 'buy' or 'return'.")
        
        # Aggiorna i gettoni del giocatore
        player.tokens = [Token(color=token.color, count=token.count) for token in player.tokens if token.count > 0]