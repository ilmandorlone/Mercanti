from collections import Counter
from core.match import Match
from core.models import CardCount, Token
from core.helpers.player_helper import PlayerHelper
from core.helpers.match_helper import MatchHelper
from core.actions.action import Action

# Implementazione della classe ActionReserveCard che eredita da Action
class ActionReserveCard(Action):
    def __init__(self, match: Match, player_id, card_id):
        super().__init__(player_id)
        self.card_id = card_id
        self.match = match

    def can_execute(self):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id(self.match, self.player_id)

        # Verifica che il giocatore non abbia già riservato il numero massimo di carte
        if len(player.reserved_cards) >= 3:
            return False

        # Trova la carta tra le carte visibili
        card = MatchHelper.get_card_by_id(self.match, self.card_id)

        # Verifica che la carta sia stata trovata
        if not card:
            # Verifica se la carta è la prima tra i mazzi nascosti
            for level in [self.match.deck_level1, self.match.deck_level2, self.match.deck_level3]:
                if level and level[0].id == self.card_id:
                    return True
    
            return False

        return True

    def execute(self):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id(self.match, self.player_id)

        # Verifica che il giocatore non abbia più di 3 carte riservate
        if len(player.reserved_cards) >= 3:
            raise ValueError("Player cannot reserve more than 3 cards")

        # Trova la carta tra le carte visibili
        card = MatchHelper.get_card_by_id(self.match, self.card_id)
       
        if card:
            # Rimuovi la carta dai livelli visibili
            MatchHelper.remove_card_from_visible(self.match, card)
            self.match.refill_visible_cards()
        else:
            # Verifica se la carta è la prima tra i mazzi nascosti
            for level in [self.match.deck_level1, self.match.deck_level2, self.match.deck_level3]:
                # Verifica che ci siano carte disponibili nel mazzo
                if level and level[0].id == self.card_id:
                    # Riserva la prima carta del mazzo nascosto
                    card = level.pop(0)
                    break
        
        if not card:
            raise ValueError(f"Card with id {self.card_id} not found in visible cards or decks")
        
        # Aggiungi la carta al giocatore e aggiungi un gettone "gold" se disponibile
        PlayerHelper.add_reserved_card_to_player(player, card)

        # Aggiungi un gettone "gold" al giocatore se disponibile e se non ha già 10 gettoni
        PlayerHelper.add_gold_token_to_player(player, self.match)