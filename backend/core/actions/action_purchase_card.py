from collections import Counter
from core.match import Match
from core.models import ContextMatch, ListCardCount, TokenActionEnum
from core.helpers.player_helper import PlayerHelper
from core.helpers.match_helper import MatchHelper
from core.actions.action import Action

# Implementazione della classe ActionPurchaseCard che eredita da Action
class ActionPurchaseCard(Action):
    def __init__(self, context_match: ContextMatch, player_id: int, card_id: int):
        super().__init__(context_match=context_match, player_id=player_id)
        self.card_id = card_id

    def can_execute(self):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id_in_context(self.context_match, self.player_id)

        # Trova la carta nei livelli visibili o nelle carte riservate
        card = MatchHelper.get_card_by_id_in_context(self.context_match, self.card_id)

        # Verifica che la carta sia stata trovata
        if not card:
            return False

        # Verifica che il giocatore abbia abbastanza gettoni per acquistare la carta (considerando gli sconti) o abbia abbastanza jolly
        if not PlayerHelper.has_enough_tokens(player, card):
            return False

        return True

    def execute(self):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id_in_context(self.context_match, self.player_id)

        # Trova la carta nei livelli visibili o nelle carte riservate
        card = MatchHelper.get_card_by_id_in_context(self.context_match, self.card_id)

        # Verifica che la carta sia stata trovata
        if not card:
            raise ValueError(f"Card with id {self.card_id} not found in visible cards or reserved cards")
        
        # Verifica che il giocatore abbia abbastanza gettoni per acquistare la carta (considerando gli sconti) o abbia abbastanza jolly
        if not PlayerHelper.has_enough_tokens(player, card):
            raise ValueError(f"Not enough tokens to purchase the card: {self.card_id}")

        # Paga i gettoni necessari (considerando gli sconti) o jolly per acquistare la carta e restituiscili al tavolo
        PlayerHelper.pay_tokens_in_context(self.context_match, player, card)

        # Aggiungi la carta al giocatore e assegna i punti
        PlayerHelper.add_card_to_player(player, card)

        # Rimuovi la carta dalle carte riservate o dal livello visibile
        MatchHelper.remove_card_from_visible_or_reserved_in_context(self.context_match, card)

        # Refill le carte visibili se necessario
        MatchHelper.refill_visible_cards(self.context_match)
        
        # Verifica e assegna le tessere nobile
        MatchHelper.check_and_assign_noble(self.context_match, player)