import json
from typing import List
from ai_player.np_array_types import ( dtype_status_before_afterAction, dtype_status_card, dtype_status_game,
                              dtype_status_player, dtype_noble, StatusCardEnum_NP, StatusNobleEnum_NP )
from core.models import ContextMatch, Player

import numpy as np

class AIUtils():

    # Funzione per convertire l'array NumPy in un formato serializzabile in JSON
    def numpy_to_dict(np_array):
        if isinstance(np_array, np.ndarray):
            if np_array.dtype.fields is not None:  # Structured array
                return {name: AIUtils.numpy_to_dict(np_array[name]) for name in np_array.dtype.names}
            else:
                if np_array.size == 1:
                    return np_array.item()
                else:
                    return np_array.tolist()
        elif isinstance(np_array, (np.generic, np.number)):
            return np_array.item()
        else:
            return np_array
        
    @staticmethod
    def numpy_to_readable(np_array):
        if isinstance(np_array, np.ndarray):
            if np_array.dtype.fields is not None:
                result = {}
                for name in np_array.dtype.names:
                    value = np_array[name]
                    if value.dtype.fields is not None:  # Nested structure
                        if value.size > 1:
                            result[name] = [AIUtils.numpy_to_readable(item) for item in value]
                        else:
                            result[name] = AIUtils.numpy_to_readable(value)
                    else:
                        if value.size > 1:
                            result[name] = value.tolist()
                        else:
                            result[name] = value.item()
                return result
            else:
                return np_array.tolist()
        else:
            return np_array


    @staticmethod
    def convert_context_match_to_status_game_for_ai_player(context_match: ContextMatch, player: Player): 
        '''
        Converte lo stato del gioco ContextMatch in uno stato del gioco per l'AI dato un specifico giocatore
        contiene solo i dati che il giocatore di turno può vedere (non contiene i dati degli altri giocatori)
        :param context_match: ContextMatch - il contesto della partita
        :param player_id: int - l'id del giocatore
        :return: np.array - lo stato del gioco per l'AI dtype_status_game
        '''

        # Crea un oggetto dtype_status_game
        game_state = np.zeros(1, dtype=dtype_status_game)

        # Imposta lo stato del gioco generale
        game_state['round'] = context_match.round                   # Round
        game_state['player_id'] = player.id                         # Id del giocatore
        game_state['tokens_violet'] = context_match.tokens.violet   # Gettoni violet
        game_state['tokens_blue'] = context_match.tokens.blue       # Gettoni blue
        game_state['tokens_green'] = context_match.tokens.green     # Gettoni green
        game_state['tokens_red'] = context_match.tokens.red         # Gettoni red
        game_state['tokens_black'] = context_match.tokens.black     # Gettoni black
        game_state['tokens_gold'] = context_match.tokens.gold       # Gettoni gold

        # Imposta le informazioni del giocatore di turno
        np_player = game_state['player']
        np_player['tokens_violet'] = player.tokens.violet           # Gettoni violet del giocatore di turno
        np_player['tokens_blue'] = player.tokens.blue                  # Gettoni blue del giocatore di turno
        np_player['tokens_green'] = player.tokens.green                # Gettoni green del giocatore di turno
        np_player['tokens_red'] = player.tokens.red                    # Gettoni red del giocatore di turno
        np_player['tokens_black'] = player.tokens.black                # Gettoni black del giocatore di turno
        np_player['tokens_gold'] = player.tokens.gold                  # Gettoni gold del giocatore di turno
        np_player['cards_violet'] = player.cards_count.violet          # Carte violet del giocatore di turno
        np_player['cards_blue'] = player.cards_count.blue              # Carte blue del giocatore di turno
        np_player['cards_green'] = player.cards_count.green            # Carte green del giocatore di turno
        np_player['cards_red'] = player.cards_count.red                # Carte red del giocatore di turno
        np_player['cards_black'] = player.cards_count.black            # Carte black del giocatore di turno
        np_player['points'] = player.points                            # Punti del giocatore di turno

        # Imposta le informazioni dei giocatori avversari
        opponents : List[Player] = [player for player in context_match.players if player.id != player.id]

        # Imposta le informazioni dei giocatori avversari
        for opponent in opponents:
            np_opponent = game_state['opponents'][opponent.id - 1]
            np_opponent['tokens_violet'] = opponent.tokens.violet
            np_opponent['tokens_blue'] = opponent.tokens.blue
            np_opponent['tokens_green'] = opponent.tokens.green
            np_opponent['tokens_red'] = opponent.tokens.red
            np_opponent['tokens_black'] = opponent.tokens.black
            np_opponent['tokens_gold'] = opponent.tokens.gold
            np_opponent['cards_violet'] = opponent.cards_count.violet
            np_opponent['cards_blue'] = opponent.cards_count.blue
            np_opponent['cards_green'] = opponent.cards_count.green
            np_opponent['cards_red'] = opponent.cards_count.red
            np_opponent['cards_black'] = opponent.cards_count.black
            np_opponent['points'] = opponent.points

        # Crea le strutture per le carte e i nobili con valori di default
        cards_level1 = np.zeros(40, dtype=dtype_status_card)
        cards_level2 = np.zeros(30, dtype=dtype_status_card)
        cards_level3 = np.zeros(20, dtype=dtype_status_card)
        nobles = np.zeros(10, dtype=dtype_noble)

        # Imposta tutte le 40 carte del primo livello come UNKNOWN_LEVEL1
        cards_level1['position'] = StatusCardEnum_NP.UNKNOWN_LEVEL1
        # Imposta tutte le 30 carte del secondo livello come UNKNOWN_LEVEL2
        cards_level2['position'] = StatusCardEnum_NP.UNKNOWN_LEVEL2
        # Imposta tutte le 20 carte del terzo livello come UNKNOWN_LEVEL3
        cards_level3['position'] = StatusCardEnum_NP.UNKNOWN_LEVEL3
        # Imposta tutti i 10 nobili come UNASSIGNED
        game_state['nobles']['position'] = StatusNobleEnum_NP.NOT_USED

        # Imposta lo stato delle carte visibili del primo livello come VISIBLE_LEVEL1
        for card in context_match.visible_level1:
            cards_level1['position'][card.id - 1] = StatusCardEnum_NP.VISIBLE_LEVEL1
        
        # Imposta lo stato delle carte visibili del secondo livello come VISIBLE_LEVEL2
        for card in context_match.visible_level2:
            cards_level2['position'][card.id - 41] = StatusCardEnum_NP.VISIBLE_LEVEL2

        # Imposta lo stato delle carte visibili del terzo livello come VISIBLE_LEVEL3
        for card in context_match.visible_level3:
            cards_level3['position'][card.id - 71] = StatusCardEnum_NP.VISIBLE_LEVEL3

        # Imposto tutte le carte acquistate e nobili assegnati dai giocatori
        for _player in context_match.players:
                # Imposta lo stato delle carte acquistate dal giocatore
                for card in _player.cards_purchased:
                    if card.level == 1:
                        cards_level1['position'][card.id - 1] = int(StatusCardEnum_NP.PURCHASED_PLAYER1) + _player.id - 1
                    elif card.level == 2:
                        cards_level2['position'][card.id - 41] = int(StatusCardEnum_NP.PURCHASED_PLAYER1) + _player.id - 1
                    elif card.level == 3:
                        cards_level3['position'][card.id - 71] = int(StatusCardEnum_NP.PURCHASED_PLAYER1) + _player.id - 1
                
                # Imposta lo stato dei nobili assegnati ai giocatore
                for noble in _player.passengers:
                    nobles['position'][noble.id - 1] = int(StatusNobleEnum_NP.ASSIGNED_PLAYER1) + _player.id - 1
                
        # Imposto lo stato dei nobili non ancora assegnati
        for noble in context_match.visible_passengers:
            nobles['position'][noble.id - 1] = StatusNobleEnum_NP.UNASSIGNED

        # Variabile che indica se tutte le carte riservate dai giocatori avversari sono visibili
        all_reserved_cards_visible_level1 = True
        all_reserved_cards_visible_level2 = True
        all_reserved_cards_visible_level3 = True

        # Imposta lo stato delle carte riservate dal giocatore avversario
        for opponent in opponents:
            for reserved_card in opponent.reserved_cards:
                if reserved_card.reserved_from_visible == False:
                    if reserved_card.card.level == 1:
                        all_reserved_cards_visible_level1 = False
                    elif reserved_card.card.level == 2:
                        all_reserved_cards_visible_level2 = False
                    elif reserved_card.card.level == 3:
                        all_reserved_cards_visible_level3 = False
                    
                    continue

                if reserved_card.card.level == 1:
                    cards_level1['position'][reserved_card.card.id - 1] = int(StatusCardEnum_NP.RESERVED_PLAYER1) + opponent.id - 1
                elif reserved_card.card.level == 2:
                    cards_level2['position'][reserved_card.card.id - 41] = int(StatusCardEnum_NP.RESERVED_PLAYER1) + opponent.id - 1
                elif reserved_card.card.level == 3:
                    cards_level3['position'][reserved_card.card.id - 71] = int(StatusCardEnum_NP.RESERVED_PLAYER1) + opponent.id - 1

        # Se tutte le carte riservate dai giocatori avversari di livello 1 sono visibili
        if all_reserved_cards_visible_level1:
            # Imposta lo stato delle carte ancora disponibili nel mazzo livello 1
            for card in context_match.deck_level1:
                cards_level1['position'][card.id - 1] = StatusCardEnum_NP.ON_DECK_LEVEL1
        
        # Se tutte le carte riservate dai giocatori avversari di livello 2 sono visibili
        if all_reserved_cards_visible_level2:
            # Imposta lo stato delle carte ancora disponibili nel mazzo livello 2
            for card in context_match.deck_level2:
                cards_level2['position'][card.id - 41] = StatusCardEnum_NP.ON_DECK_LEVEL2
        
        # Se tutte le carte riservate dai giocatori avversari di livello 3 sono visibili
        if all_reserved_cards_visible_level3:
            # Imposta lo stato delle carte ancora disponibili nel mazzo livello 3
            for card in context_match.deck_level3:
                cards_level3['position'][card.id - 71] = StatusCardEnum_NP.ON_DECK_LEVEL3
        
        # Imposta lo stato delle carte riservate dal giocatore
        game_state['cards_level1'] = cards_level1
        game_state['cards_level2'] = cards_level2
        game_state['cards_level3'] = cards_level3
        game_state['nobles'] = nobles

        return game_state

        '''
        prova_readable = AIUtils.numpy_to_readable(game_state)
        pass

        state = np.zeros(1, dtype=dtype_status_game)
        #prova_json = json.dumps(AIUtils.numpy_to_dict(state))
        #prova_readable = AIUtils.numpy_to_readable(game_state)

        pass
        '''
