from dataclasses import dataclass
from enum import Enum
from typing import List
import numpy as np

from ai_player.np_array_types import ( StatusCardEnum_NP, dtype_status_card )
from ai_player.utils import AIUtils
from core.actions.action_purchase_card import ActionPurchaseCard
from core.actions.action_reserve_card import ActionReserveCard
from core.actions.action_select_tokens import ActionSelectTokens
from core.actions.action import Action
from core.actions.get_all_possible_actions import get_all_possible_actions
from core.helpers.match_helper import MatchHelper
from core.helpers.player_helper import PlayerHelper
from core.provider import provider_instance
from core.match import Match

from core.models import Card, ColorEnum, ContextMatch, ListTokenCount, Player

# Test della funzione in utils.py convert_context_match_to_status_game_for_ai_player che converte il contesto della partita in un np.array
def test_convert_context_match_to_status_game_for_ai_player():
    '''
    Test della funzione convert_context_match_to_status_game_for_ai_player che converte il contesto della partita in un np.array
    Viene creato un contesto della partita e un giocatore,
    viene convertito il contesto della partita in un np.array
    successivamente viene riconvertito in un contesto della partita
    e si verifica che il contesto della partita sia uguale a quello iniziale
    '''

    # Crea una lista di giocatori CPU
    players = [provider_instance.create_cpu_player(id=0, name="AI Player 1"),
               provider_instance.create_cpu_player(id=1, name="AI Player 2"),
               provider_instance.create_cpu_player(id=2, name="AI Player 3")]

    # Crea una nuova partita
    match = Match(players)
    match.load_cards("setup.json")

    # Ottiene il giocatore corrente
    player = match.context.players[0]

    # Ottiene lo stato del gioco prima dell'azione
    before = match.context

    # Ottiene lo stato del gioco prima e dopo l'azione per ogni azione possibile
    actions = get_all_possible_actions(match.context, player.id, enable_filer_purchase=True)

    # Converti il contesto della partita in un np.array
    data_converted = AIUtils.convert_context_match_to_status_game_for_ai_player(match.context, player)

    # Inizializza il contesto della partita e i giocatori a partire dal np.array
    after = init_new_context_and_players(data_converted, before)

    # Verifica i gettoni del tavolo prima e dopo la conversione
    test_tokens_table_from_np_array(data_converted, before, after)

    # Verifica i gettoni dei giocatori prima e dopo la conversione
    test_tokens_players_from_np_array(data_converted, before, after)

    # Verifica le carte visibili prima e dopo la conversione
    test_card_visible(data_converted, before, after)
    
def init_new_context_and_players(data: np.array, before_context: ContextMatch) -> ContextMatch:
    '''
    Test della funzione convert_context_match_to_status_game_for_ai_player che converte il dtype_status_game in un contesto della partita
    Viene ricostruito il contesto della partita a partire dal np.array
    '''

    # Array di giocatori
    players = []

    # Crea i giocatori
    for i in range(4):
        if data['players'][0]['points'][i] == -1 or data['players'][0]['points'][i] == 255:
            continue

        player = Player(
            id=i,
            name=f"Player {i+1}",
            cards_count=0,
            points=0,
            tokens= []
        )

        # Aggiungi il giocatore alla lista dei giocatori
        players.append(player)
    
    # Contesto della partita
    after_context = ContextMatch(players)

    # Verifica il numero di giocatori prima e dopo la conversione
    print("numero giocatori prima", len(before_context.players))
    print("numero giocatori dopo", len(after_context.players))
    assert len(before_context.players) == len(after_context.players), "Il numero di giocatori non corrisponde"

    return after_context

def test_tokens_table_from_np_array(data: np.array, before_context: ContextMatch, after_context: ContextMatch):
    '''
    Test della funzione convert_context_match_to_status_game_for_ai_player che restituisce i gettoni del tavolo a partire da un np.array
    '''

    after_context.tokens = ListTokenCount(
        violet=int(data['tokens_violet']),
        blue=int(data['tokens_blue']),
        green=int(data['tokens_green']),
        red=int(data['tokens_red']),
        black=int(data['tokens_black']),
        gold=int(data['tokens_gold'])
    )
    
    print("gettoni tavolo prima", before_context.tokens)
    print("gettoni tavolo dopo ", after_context.tokens)
    assert before_context.tokens == after_context.tokens, "I gettoni del tavolo non corrispondono"

def test_tokens_players_from_np_array(data: np.array, before_context: ContextMatch, after_context: ContextMatch):
    '''
    Test della funzione convert_context_match_to_status_game_for_ai_player che restituisce i gettoni dei giocatori a partire da un np.array
    '''

    for player in after_context.players:
        player.tokens = ListTokenCount(
            violet=int(data['players'][0]['tokens_violet'][player.id]),
            blue=int(data['players'][0]['tokens_blue'][player.id]),
            green=int(data['players'][0]['tokens_green'][player.id]),
            red=int(data['players'][0]['tokens_red'][player.id]),
            black=int(data['players'][0]['tokens_black'][player.id]),
            gold=int(data['players'][0]['tokens_gold'][player.id])
        )

        print("gettoni giocatore prima id", player.id, "tokens", before_context.players[player.id].tokens)
        print("gettoni giocatore dopo  id", player.id, "tokens", after_context.players[player.id].tokens)
        assert before_context.players[player.id].tokens == player.tokens, "I gettoni del giocatore non corrispondono"

def test_card_visible(data: np.array, before_context: ContextMatch, after_context: ContextMatch):
    '''
    Test della funzione convert_context_match_to_status_game_for_ai_player che restituisce le carte visibili a partire da un np.array
    '''

    # Inizializza le carte visibili
    after_context.visible_level1 = []
    after_context.visible_level2 = []
    after_context.visible_level3 = []

    # Carte visibili livello 1
    for id_card in range(1, 41):
        if data['cards_level1'][0]['position'][id_card - 1] == int(StatusCardEnum_NP.VISIBLE_LEVEL1):
            card = Card(id=id_card)
            after_context.visible_level1.append(card)
        
    # Verifica le carte visibili
    cards_before = sorted([card.id for card in before_context.visible_level1])
    cards_after = [card.id for card in after_context.visible_level1]
    print("carte visibili livello 1 prima", cards_before)
    print("carte visibili livello 1 dopo ", cards_after)
    assert cards_before == cards_after, "Le carte visibili del livello 1 non corrispondono"

    # Carte visibili livello 2
    for id_card in range(41, 71):
        if data['cards_level2'][0]['position'][id_card - 41] == int(StatusCardEnum_NP.VISIBLE_LEVEL2):
            card = Card(id=id_card)
            after_context.visible_level2.append(card)
    
    # Verifica le carte visibili
    cards_before = sorted([card.id for card in before_context.visible_level2])
    cards_after = [card.id for card in after_context.visible_level2]
    print("carte visibili livello 2 prima", cards_before)
    print("carte visibili livello 2 dopo ", cards_after)
    assert cards_before == cards_after, "Le carte visibili del livello 2 non corrispondono"

    # Carte visibili livello 3
    for id_card in range(71, 91):
        if data['cards_level3'][0]['position'][id_card - 71] == int(StatusCardEnum_NP.VISIBLE_LEVEL3):
            card = Card(id=id_card)
            after_context.visible_level3.append(card)
        
    # Verifica le carte visibili
    cards_before = sorted([card.id for card in before_context.visible_level3])
    cards_after = [card.id for card in after_context.visible_level3]
    print("carte visibili livello 3 prima", cards_before)
    print("carte visibili livello 3 dopo ", cards_after)
    assert cards_before == cards_after, "Le carte visibili del livello 3 non corrispondono"


