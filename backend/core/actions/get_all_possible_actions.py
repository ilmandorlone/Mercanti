
from itertools import combinations
from typing import List

from core.utils import Utils
from core.helpers.match_helper import MatchHelper
from core.models import ColorEnum, ContextMatch, Player, TokenActionEnum, TokenAction, Card, Noble

from core.actions.action_purchase_card import ActionPurchaseCard
from core.actions.action_select_tokens import ActionSelectTokens
from core.actions.action_reserve_card import ActionReserveCard
from core.actions.action import Action

# Tutte le combinazioni delle azioni possibili per i gettoni (3 o 2 diversi, 2 uguali, o 1 solo) senza possibilità di restituzione
def _get_all_possible_token_actions_without_return(context_match: ContextMatch, player_id: int):
    actions = []

    # Filtra i colori per escludere "GOLD"
    filtered_colors = [color.value for color in ColorEnum if color != ColorEnum.GOLD]

    # Filtra i colori che hanno almeno un gettone disponibile nel tavolo
    filtered_colors = [color for color in filtered_colors if Utils.get_value_of_object_from_name(context_match.tokens, color) > 0]

    # Tockens del giocatore
    player_tokens = MatchHelper.get_player_by_id_in_context(context_match, player_id).tokens

    # Calcola il numero totale di gettoni del giocatore
    player_tokens_count = Utils.sum_object_attributes(player_tokens)

    # Calcola il numero massimo di gettoni che il giocatore può selezionare senza superare 10 e massimo 3 per volta
    max_tokens_to_buy = min(3, 10 - player_tokens_count)

    # Verifica se il giocatore ha già 10 gettoni
    if max_tokens_to_buy == 0:
        return actions

    # Calcola tutte le combinazioni di 3, 2 e 1 gettoni di colori diversi
    for i in range(1, max_tokens_to_buy + 1):
        # Calcola tutte le combinazioni di colori diversi tra i colori disponibili
        color_combinations = list(combinations(filtered_colors, i))

        # Per ogni combinazione di colori, crea un'azione per selezionare i gettoni
        for combination in color_combinations:
            # Crea la lista di gettoni da acquistare
            token_actions = [TokenAction(action=TokenActionEnum.BUY.value, color=color, count=1) for color in combination]
            
            # Crea l'azione per selezionare i gettoni
            action = ActionSelectTokens(context_match=context_match, player_id=player_id, token_actions=token_actions)

            # Verifica se l'azione può essere eseguita
            actions.append(action)
    
    # Verifica se il giocatore può selezionare 2 gettoni dello stesso colore
    if max_tokens_to_buy < 2:
        return actions
    
    # Calcola tutte le combinazioni di 2 gettoni dello stesso colore
    for color in filtered_colors:
        # Verifica se ci sono almeno 4 gettoni disponibili di quel colore
        if Utils.get_value_of_object_from_name(context_match.tokens, color) < 4:
            continue

        # Crea la lista di gettoni da acquistare
        token_actions = [TokenAction(action=TokenActionEnum.BUY.value, color=color, count=2)]

        # Crea l'azione per selezionare i gettoni
        action = ActionSelectTokens(context_match=context_match, player_id=player_id, token_actions=token_actions)

        # Verifica se l'azione può essere eseguita
        actions.append(action)

    return actions

'''
# Tutte le combinazioni delle azioni possibili per i gettoni (3 o 2 diversi, 2 uguali, o 1 solo) con possibilità di restituzione
def _get_all_possible_token_actions_with_return(match, player_id):
    actions = []

    # Filtra i colori per escludere "GOLD"
    filtered_colors = [color for color in ColorEnum if color != ColorEnum.GOLD]

    # Filtra i colori che hanno almeno un gettone disponibile
    filtered_colors = [color for color in filtered_colors if match.get_token_count_of_color(color) > 0]

    # Calcola tutte le combinazioni di 3, 2 e 1 gettoni di colori diversi
    for i in range(1, 4):
        # Calcola tutte le combinazioni di colori diversi
        color_combinations = list(combinations(filtered_colors, i))

        # Tockens del giocatore
        player_tokens = MatchHelper.get_player_by_id(match, player_id).tokens

        # Calcola il numero totale di gettoni del giocatore dopo l'azione
        total_tokens_after_action = sum(token.count for token in player_tokens) + i

        # Per ogni combinazione di colori, crea un'azione per selezionare i gettoni
        for combination in color_combinations:

            # Calcola il numero di gettoni in eccesso
            total_tokens_diff = max(0, total_tokens_after_action - 10)

            if total_tokens_diff > 0:
                # Lista dei gettoni del giocatore che possono essere restituiti
                # Crea una lista di gettoni da restituire, aggiungi ripetizioni per i gettoni dello stesso colore
                # es. Token(color="violet", count=2) -> return_colors += ["violet", "violet"]
                # limita il numero di gettoni restituiti per colore al massimo di total_tokens_diff
                return_colors = convert_tokens_to_limited_list(player_tokens, max_per_color=total_tokens_diff)

                # Tutte le combinazioni di gettoni da restituire anche più gettoni dello stesso colore
                return_combinations = list(combinations(return_colors, total_tokens_diff))

                for return_combination in return_combinations:
                    token_actions = [TokenAction(action=TokenActionEnum.BUY.value, color=color, count=1) for color in combination]
                    token_actions += [TokenAction(action=TokenActionEnum.RETURN.value, color=color, count=1) for color in return_combination]
                    action = ActionSelectTokens(match=match, player_id=player_id, token_actions=token_actions)

                    # Verifica se l'azione può essere eseguita
                    if action.can_execute():
                        actions.append(action)
            else:
                token_actions = [TokenAction(action=TokenActionEnum.BUY.value, color=color, count=1) for color in combination]
                action = ActionSelectTokens(match=match, player_id=player_id, token_actions=token_actions)

                # Verifica se l'azione può essere eseguita
                if action.can_execute():
                    actions.append(action)
    
    # Calcola tutte le combinazioni di 2 gettoni dello stesso colore
    for color in filtered_colors:
        token_actions = [TokenAction(action=TokenActionEnum.BUY.value, color=color, count=2)]
        action = ActionSelectTokens(match=match, player_id=player_id, token_actions=token_actions)

        # Verifica se l'azione può essere eseguita
        if action.can_execute():
            actions.append(action)

    return actions
'''

# Tutte le azioni acquistabili per le carte
def _get_all_possible_purchase_card_actions(context_match: ContextMatch, player_id: int):
    actions = []

    # Per ogni carta visibile, crea un'azione per acquistarla
    for card in context_match.visible_level1 + context_match.visible_level2 + context_match.visible_level3:
        action = ActionPurchaseCard(context_match=context_match, player_id=player_id, card_id=card.id)

        # Verifica se l'azione può essere eseguita
        if action.can_execute():
            actions.append(action)

    return actions

# Tutte le azioni possibili per riservare carte
def _get_all_possible_reserve_card_actions(context_match: ContextMatch, player_id: int):
    actions = []

    # Per ogni livello di carte, crea un'azione per riservare la prima carta
    for level in range(1, 4):
        # Seleziona il mazzo di carte per il livello specificato
        deck_level = MatchHelper.select_deck_level_by_level(context_match, level)

        # Verifica se c'è almeno una carta disponibile nel livello specificato
        if not deck_level:
            continue

        # Recupera l'id della carta dal livello specificato
        card_id = deck_level[0].id
        action = ActionReserveCard(context_match=context_match, player_id=player_id, card_id=card_id)

        # Verifica se l'azione può essere eseguita
        if action.can_execute():
            actions.append(action)
    
    # Per ogni carta visibile, crea un'azione per riservarla
    for card in context_match.visible_level1 + context_match.visible_level2 + context_match.visible_level3:
        action = ActionReserveCard(context_match=context_match, player_id=player_id, card_id=card.id)

        # Verifica se l'azione può essere eseguita
        if action.can_execute():
            actions.append(action)

    return actions

def get_all_possible_actions(context_metch: ContextMatch, player_id: int, enable_filer_purchase: bool = False) -> List[Action]:
    actions = []

    # Azioni per acquistare carte
    actions += _get_all_possible_purchase_card_actions(context_match=context_metch, player_id=player_id)

    # Se è abilitato il filtro per l'acquisto di carte, restituisci solo le azioni per acquistare carte
    if actions and enable_filer_purchase:
        return actions

    # Azioni per riservare carte
    actions += _get_all_possible_reserve_card_actions(context_match=context_metch, player_id=player_id)

    # Tutte le combinazioni delle azioni possibili per i gettoni (3 o 2 diversi, 2 uguali, o 1 solo) 
    # senza possibilità di restituzione
    actions += _get_all_possible_token_actions_without_return(context_match=context_metch, player_id=player_id)

    return actions
