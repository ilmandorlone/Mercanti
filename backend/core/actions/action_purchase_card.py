from collections import Counter

import numpy as np
from core.match import Match
from core.models import ContextMatch, ListCardCount, TokenActionEnum
from core.helpers.player_helper import PlayerHelper
from core.helpers.match_helper import MatchHelper
from core.actions.action import Action

from ai_player.np_array_types import ( dtype_status_before_afterAction, dtype_status_card, dtype_status_game,
                              dtype_status_player, dtype_noble, StatusCardEnum_NP, StatusNobleEnum_NP )

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

    def execute_on_context(self, context_match: ContextMatch):
        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id_in_context(context_match, self.player_id)

        # Trova la carta nei livelli visibili o nelle carte riservate
        card = MatchHelper.get_card_by_id_in_context(context_match, self.card_id)

        # Verifica che la carta sia stata trovata
        if not card:
            raise ValueError(f"Card with id {self.card_id} not found in visible cards or reserved cards")
        
        # Verifica che il giocatore abbia abbastanza gettoni per acquistare la carta (considerando gli sconti) o abbia abbastanza jolly
        if not PlayerHelper.has_enough_tokens(player, card):
            raise ValueError(f"Not enough tokens to purchase the card: {self.card_id}")

        # Paga i gettoni necessari (considerando gli sconti) o jolly per acquistare la carta e restituiscili al tavolo
        PlayerHelper.pay_tokens_in_context(context_match, player, card)

        # Aggiungi la carta al giocatore e assegna i punti
        PlayerHelper.add_card_to_player(player, card)

        # Rimuovi la carta dalle carte riservate o dal livello visibile
        MatchHelper.remove_card_from_visible_or_reserved_in_context(context_match, card)

        # Refill le carte visibili se necessario
        MatchHelper.refill_visible_cards(context_match)
        
        # Verifica e assegna le tessere nobile
        MatchHelper.check_and_assign_noble(context_match, player)
    
    def execute(self):
        return self.execute_on_context(self.context_match)
    

    # Esegue l'azione su un array di dati
    def execute_on_data_array(self, data: np.array):
        data_after = np.copy(data)

        # Trova il giocatore nella partita
        player = MatchHelper.get_player_by_id_in_context(self.context_match, self.player_id)

        # Trova la carta nei livelli visibili o nelle carte riservate
        card = MatchHelper.get_card_by_id_in_context(self.context_match, self.card_id)

        # Verifica che la carta sia stata trovata
        if not card:
            raise ValueError(f"Card with id {self.card_id} not found in visible cards or reserved cards")

        # Gettoni 'gold' necessari
        needed_gold = PlayerHelper.get_gold_tokens_to_use(player, card)

        # Calcola i gettoni che restano al giocatore dopo l'acquisto
        player_violet = max(0, player.tokens.violet - max(0, card.cost.violet - player.cards_count.violet))
        player_blue = max(0, player.tokens.blue - max(0, card.cost.blue - player.cards_count.blue))
        player_green = max(0, player.tokens.green - max(0, card.cost.green - player.cards_count.green))
        player_red = max(0, player.tokens.red - max(0, card.cost.red - player.cards_count.red))
        player_black = max(0, player.tokens.black - max(0, card.cost.black - player.cards_count.black))
        player_gold = max(0, player.tokens.gold - needed_gold)

        # Aggiorna i gettoni del giocatore
        data_after['players'][0]['tokens_violet'][player.id] = player_violet
        data_after['players'][0]['tokens_blue'][player.id] = player_blue
        data_after['players'][0]['tokens_green'][player.id] = player_green
        data_after['players'][0]['tokens_red'][player.id] = player_red
        data_after['players'][0]['tokens_black'][player.id] = player_black
        data_after['players'][0]['tokens_gold'][player.id] = player_gold

        # Calcola i gettoni del tavolo dopo l'acquisto
        data_after['tokens_violet'] = self.context_match.tokens.violet + player.tokens.violet - player_violet
        data_after['tokens_blue'] = self.context_match.tokens.blue + player.tokens.blue - player_blue
        data_after['tokens_green'] = self.context_match.tokens.green + player.tokens.green - player_green
        data_after['tokens_red'] = self.context_match.tokens.red + player.tokens.red - player_red
        data_after['tokens_black'] = self.context_match.tokens.black + player.tokens.black - player_black
        data_after['tokens_gold'] = self.context_match.tokens.gold + player.tokens.gold - player_gold

        # Aggiungi la carta al giocatore
        data_after['players'][0]['cards_' + card.color][player.id] += 1

        # Aggiungi i punti al giocatore
        data_after['players'][0]['points'][player.id] += card.points

        # Aggiorna lo stato della carta
        if card.level == 1:
            data_after['cards_level1'][0]['position'][card.id - 1] = int(StatusCardEnum_NP.PURCHASED_PLAYER1) + player.id
        elif card.level == 2:
            data_after['cards_level2'][0]['position'][card.id - 41] = int(StatusCardEnum_NP.PURCHASED_PLAYER1) + player.id
        elif card.level == 3:
            data_after['cards_level3'][0]['position'][card.id - 71] = int(StatusCardEnum_NP.PURCHASED_PLAYER1) + player.id
        
        # Verifica e assegna le tessere nobile
        for noble in self.context_match.visible_passengers:
            # Verifica ha le carte necessarie per ottenere il nobile
            if data_after['players'][0]['cards_violet'][player.id] >= noble.cost.violet and \
                data_after['players'][0]['cards_blue'][player.id] >= noble.cost.blue and \
                data_after['players'][0]['cards_green'][player.id] >= noble.cost.green and \
                data_after['players'][0]['cards_red'][player.id] >= noble.cost.red and \
                data_after['players'][0]['cards_black'][player.id] >= noble.cost.black:

                # Imposta lo stato del nobile come assegnato
                data_after['nobles'][0]['position'][noble.id - 1] = int(StatusNobleEnum_NP.ASSIGNED_PLAYER1) + player.id

                # Aggiungi i punti al giocatore
                data_after['players'][0]['points'][player.id] += noble.points

                break

        return data_after