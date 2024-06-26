
from itertools import combinations
from typing import List

from core.helpers.match_helper import MatchHelper
from core.models import ColorEnum, Player, TokenActionEnum, TokenAction, Token, Card, Passenger

from core.actions.action_purchase_card import ActionPurchaseCard
from core.actions.action_select_tokens import ActionSelectTokens
from core.actions.action_reserve_card import ActionReserveCard

def convert_tokens_to_limited_list(tokens: List[Token], max_per_color: int) -> List[str]:
    return [
        token.color
        for token in tokens if token.color != 'gold'
        for _ in range(min(token.count, max_per_color))
    ]

# Tutte le combinazioni delle azioni possibili per i gettoni (3 o 2 diversi, 2 uguali, o 1 solo)
def _get_all_possible_token_actions(match, player_id):
    actions = []

    # Filtra i colori per escludere "GOLD"
    filtered_colors = [color for color in ColorEnum if color != ColorEnum.GOLD]

    # Calcola tutte le combinazioni di 3, 2 e 1 gettoni di colori diversi
    for i in range(1, 4):
        # Calcola tutte le combinazioni di colori diversi
        color_combinations = list(combinations(filtered_colors, i))

        # Per ogni combinazione di colori, crea un'azione per selezionare i gettoni
        for combination in color_combinations:   
            # Tockens del giocatore
            player_tokens = MatchHelper.get_player_by_id(match, player_id).tokens

            # Calcola il numero totale di gettoni del giocatore dopo l'azione
            total_tokens_after_action = sum(token.count for token in player_tokens) + i

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

# Tutte le azioni acquistabili per le carte
def _get_all_possible_purchase_card_actions(match, player_id):
    actions = []

    # Per ogni carta visibile, crea un'azione per acquistarla
    for card in match.visible_level1 + match.visible_level2 + match.visible_level3:
        action = ActionPurchaseCard(match=match, player_id=player_id, card_id=card.id)

        # Verifica se l'azione può essere eseguita
        if action.can_execute():
            actions.append(action)

    return actions

# Tutte le azioni possibili per riservare carte
def _get_all_possible_reserve_card_actions(match, player_id):
    actions = []

    # Per ogni livello di carte, crea un'azione per riservare la prima carta
    for level in range(1, 4):
        # Verifica se c'è una carta disponibile nel livello specificato
        if not match.select_deck_level_by_level(level):
            continue

        # Recupera l'id della carta dal livello specificato
        card_id = match.get_next_card_id_by_level(level)
        action = ActionReserveCard(match=match, player_id=player_id, card_id=card_id)

        # Verifica se l'azione può essere eseguita
        if action.can_execute():
            actions.append(action)
    
    # Per ogni carta visibile, crea un'azione per riservarla
    for card in match.visible_level1 + match.visible_level2 + match.visible_level3:
        action = ActionReserveCard(match=match, player_id=player_id, card_id=card.id)

        # Verifica se l'azione può essere eseguita
        if action.can_execute():
            actions.append(action)

    return actions

def get_all_possible_actions(match, player_id):
    actions = []

    # Azioni per acquistare carte
    actions += _get_all_possible_purchase_card_actions(match, player_id)

    if actions:
        return actions

    # Azioni per riservare carte
    actions += _get_all_possible_reserve_card_actions(match, player_id)

    # Tutte le combinazioni delle azioni possibili per i gettoni (3 o 2 diversi, 2 uguali, o 1 solo)
    actions += _get_all_possible_token_actions(match, player_id)

    return actions
