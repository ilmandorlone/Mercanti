from collections import Counter

import numpy as np
from ai_player.utils import AIUtils
from core.match import Match
from core.models import ColorEnum, ContextMatch, ListCardCount, ReservedCard, TokenActionEnum
from core.helpers.player_helper import PlayerHelper
from core.helpers.match_helper import MatchHelper
from core.actions.action import Action

from ai_player.np_array_types import ( ColorEnum_NP, dtype_status_before_afterAction, dtype_status_card, dtype_status_game,
                              dtype_status_player, dtype_noble, StatusCardEnum_NP, StatusNobleEnum_NP )

# Implementazione della classe ActionReserveCard che eredita da Action
class ActionReserveCard(Action):
    def __init__(self, context_match: ContextMatch, player_id, card_id):
        super().__init__(context_match=context_match, player_id=player_id)
        self.card_id = card_id

    def can_execute(self):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id_in_context(self.context_match, self.player_id)

        # Verifica che il giocatore non abbia già riservato il numero massimo di carte
        if player.reserved_cards_count >= 3:
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

    def execute_on_context(self, context_match: ContextMatch):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id_in_context(context_match, self.player_id)

        # Verifica che il giocatore non abbia più di 3 carte riservate
        if player.reserved_cards_count >= 3:
            raise ValueError("Player cannot reserve more than 3 cards")

        # Trova la carta tra le carte visibili
        card = MatchHelper.get_card_by_id_in_context(context_match, self.card_id)
        reserved_card = ReservedCard()
       
        if card:
            # Imposta la carta presa da quelle visibili sul tavolo
            reserved_card.reserved_from_visible = True

            # Rimuovi la carta dai livelli visibili
            MatchHelper.remove_card_from_visible_in_context(context_match, card)

            # Refill le carte visibili se necessario
            MatchHelper.refill_visible_cards(context_match)
        else:
            # Imposta la carta presa dal mazzo nascosto
            reserved_card.reserved_from_visible = False

            # Verifica se la carta è la prima tra i mazzi nascosti
            for level in [context_match.deck_level1, context_match.deck_level2, context_match.deck_level3]:
                # Verifica che ci siano carte disponibili nel mazzo
                # Verifica se la prima carta del mazzo è quella selezionata
                if level and level[0].id == self.card_id:
                    card = level.pop(0)
                    break
        
        if not card:
            raise ValueError(f"Card with id {self.card_id} not found in visible cards or decks")
        
        # Imposta la carta riservata
        reserved_card.card = card

        # Aggiungi la carta al giocatore e aggiungi un gettone "gold" se disponibile
        PlayerHelper.add_reserved_card_to_player(player, reserved_card)

        # Aggiungi un gettone "gold" al giocatore se disponibile e se non ha già 10 gettoni
        PlayerHelper.add_gold_token_to_player_in_context(context_match, player)
    
    def execute(self):
        self.execute_on_context(self.context_match)

    # Esegue l'azione su un array di dati
    def execute_on_data_array(self, data: np.array):
        data_after = np.copy(data)

        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id_in_context(self.context_match, self.player_id)

        # Verifica che il giocatore non abbia più di 3 carte riservate
        if player.reserved_cards_count >= 3:
            raise ValueError("Player cannot reserve more than 3 cards")

        # Trova la carta tra le carte visibili
        card = MatchHelper.get_card_by_id_in_context(self.context_match, self.card_id)
       
        if not card:

            # Verifica se la carta è la prima tra i mazzi nascosti
            for level in [self.context_match.deck_level1, self.context_match.deck_level2, self.context_match.deck_level3]:
                # Verifica che ci siano carte disponibili nel mazzo
                # Verifica se la prima carta del mazzo è quella selezionata
                if level and level[0].id == self.card_id:
                    card = level[0]
                    break
        
        if not card:
            raise ValueError(f"Card with id {self.card_id} not found in visible cards or decks")

        # Aggiungi la carta al giocatore
        data_after['players'][player.id]['cards_' + card.color] += 1

        readable_data = AIUtils.numpy_to_readable(data_after)

        # Aggiungi un gettone "gold" al giocatore se disponibile e se non ha già 10 gettoni
        if self.context_match.tokens.gold > 0 and PlayerHelper.get_sum_tokens(player) < 10:
            data_after['players'][player.id]['tokens_' + ColorEnum_NP.GOLD.name.lower()] += 1
            # Rimuovi un gettone "gold" dal tavolo
            data_after['tokens_' + ColorEnum_NP.GOLD.name.lower()] -= 1

        readable_data_after = AIUtils.numpy_to_readable(data_after)

        # Aggiorna lo stato della carta
        if card.level == 1:
            data_after['cards_level1'][card.id - 1] = int(StatusCardEnum_NP.RESERVED_PLAYER1) + player.id
        elif card.level == 2:
            data_after['cards_level2'][card.id - 41] = int(StatusCardEnum_NP.RESERVED_PLAYER1) + player.id
        else:
            data_after['cards_level3'][card.id - 71] = int(StatusCardEnum_NP.RESERVED_PLAYER1) + player.id
        
        return data_after