import json
import time
from typing import List
import random
import os
import sys

# Determina il percorso della directory principale del progetto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Aggiungi il percorso al sys.path
sys.path.append(project_root)

from core.helpers.match_helper import MatchHelper
from core.actions.action import Action
from core.actions.action_purchase_card import ActionPurchaseCard
from core.actions.action_select_tokens import ActionSelectTokens
from core.actions.action_reserve_card import ActionReserveCard
from core.actions.get_all_possible_actions import get_all_possible_actions
from core.cpu_player import CPUPlayer
from core.models import Player
from core.match import Match
from core.models import TokenAction, TokenActionEnum, ColorEnum
from core.provider import Provider, provider_instance

from ai_player.types import ListStatusBeforeAfterAction

# Conteggio volte che non ci sono azioni disponibili
no_actions_count = 0

# File record
record_file = None

# Creo un oggetto random con seed 55
randomizer = random.Random(55)

# callback player play
def player_move(match: Match, player: Player):
    global no_actions_count

    # Ottiene tutte le azioni possibili per il giocatore
    actions = get_all_possible_actions(match.context, player.id, enable_filer_purchase=True)

    # Verifica se ci sono azioni disponibili
    if not actions:
        raise Exception("No actions available")
    
    # Ottiene lo stato attuale del gioco per il giocatore
    #status_player = MatchHelper.get_game_state_by_id(match, player.id)
    # Stampa lo stato del giocatore
    #print(status_player)

    # Creo una lista per salvare lo stato prima e dopo l'azione per ogni azione possibile
    st = ListStatusBeforeAfterAction(len(actions))
    # Ottenere e stampare la dimensione della memoria allocata
    allocated_size = st.get_allocated_size()
    print(f"Memory allocated for cards_array: {allocated_size} bytes")

    '''
    # Stampa il round corrente
    print(f"Round: {match.context.round}")
    # Stampa la lista di gettoni disponibili
    print(f"tokens: {', '.join([f'{t.color} x{t.count}' for t in player.tokens])}")

    # Simula tutte le azioni possibili in match virtuali
    for action in actions:
        # Simula l'azione e ottiene lo stato del gioco
        match_sim = action.simulate(match=match)

        # Ottiene lo stato del gioco simulato per il giocatore
        status_player_sim = MatchHelper.get_game_state_by_id(match_sim, player.id)
    '''


    # Ottiene un azione random tra quelle disponibili
    action = randomizer.choice(actions)
    
    # Esegue l'azione
    action.execute()

# Avvia il cronometro
tart_time = time.perf_counter()

# simula 10 partite
for i in range(100):

    # Crea una lista di giocatori CPU
    players = [provider_instance.create_cpu_player(id=0, name="AI Player 1"),
               provider_instance.create_cpu_player(id=1, name="AI Player 2"),
               provider_instance.create_cpu_player(id=2, name="AI Player 3")]

    # Crea una nuova partita
    match = Match(players)
    match.load_cards("backend/core/setup.json", randomizer=randomizer)

    players[0].set_callback_move(player_move)
    players[1].set_callback_move(player_move)
    players[2].set_callback_move(player_move)

    try:
        # Avvia la partita e determina il vincitore
        winner = match.run()

        # Stampa il vincitore
        #print(f"Winner is {winner.name} with {winner.points} points vs {', '.join([f'{p.name}: {p.points}' for p in match.context.deck_level3 if p != winner])} in round {match.context.round}")
        print(f"Winner is {winner.name} with {winner.points} points in round {match.context.round}")
    except Exception as e:
        # Verifica se è stata sollevata un'eccezione per mancanza di azioni disponibili
        if str(e) == "No actions available":
            print("No actions available")
        else:
            raise e

# Ferma il cronometro
end_time = time.perf_counter()

# Stampa il tempo impiegato
print(f"Time elapsed: {end_time - tart_time} seconds")
