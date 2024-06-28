from collections import Counter
from core.match import Match
from core.models import ContextMatch, ListCardCount, TokenActionEnum
from core.helpers.player_helper import PlayerHelper
from core.helpers.match_helper import MatchHelper
from core.actions.action import Action

# Implementazione della classe ActionReserveCard che eredita da Action
class ActionReserveCard(Action):
    def __init__(self, context_match: ContextMatch, player_id, card_id):
        super().__init__(context_match=context_match, player_id=player_id)
        self.card_id = card_id

    def can_execute(self):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id_in_context(self.context_match, self.player_id)

        # Verifica che il giocatore non abbia già riservato il numero massimo di carte
        if len(player.reserved_cards) >= 3:
            return False

        # Trova la carta tra le carte visibili
        card = MatchHelper.get_card_by_id_in_context(self.context_match, self.card_id)

        # Verifica che la carta sia stata trovata
        if not card:
            # Verifica se la carta è la prima tra i mazzi nascosti
            for level in [self.context_match.deck_level1, self.context_match.deck_level2, self.context_match.deck_level3]:
                # Verifica che ci siano carte disponibili nel mazzo
                if level and level[0].id == self.card_id:
                    return True
    
            return False

        return True

    def execute(self):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id_in_context(self.context_match, self.player_id)

        # Verifica che il giocatore non abbia più di 3 carte riservate
        if len(player.reserved_cards) >= 3:
            raise ValueError("Player cannot reserve more than 3 cards")

        # Trova la carta tra le carte visibili
        card = MatchHelper.get_card_by_id_in_context(self.context_match, self.card_id)
       
        if card:
            # Rimuovi la carta dai livelli visibili
            MatchHelper.remove_card_from_visible_in_context(self.context_match, card)

            # Refill le carte visibili se necessario
            MatchHelper.refill_visible_cards(self.context_match)
        else:
            # Verifica se la carta è la prima tra i mazzi nascosti
            for level in [self.context_match.deck_level1, self.context_match.deck_level2, self.context_match.deck_level3]:
                # Verifica che ci siano carte disponibili nel mazzo
                # Verifica se la prima carta del mazzo è quella selezionata
                if level and level[0].id == self.card_id:
                    card = level.pop(0)
                    break
        
        if not card:
            raise ValueError(f"Card with id {self.card_id} not found in visible cards or decks")
        
        # Aggiungi la carta al giocatore e aggiungi un gettone "gold" se disponibile
        PlayerHelper.add_reserved_card_to_player(player, card)

        # Aggiungi un gettone "gold" al giocatore se disponibile e se non ha già 10 gettoni
        PlayerHelper.add_gold_token_to_player_in_context(self.context_match, player)