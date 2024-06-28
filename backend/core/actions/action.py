# classe base action che implementa il metodo execute e can execute

from copy import copy, deepcopy

from core.models import ContextMatch


class Action:
    def __init__(self, context_match: ContextMatch, player_id: int):
        self.context_match = context_match
        self.player_id = player_id

    def can_execute(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
    
    # Metodo per simulare l'azione senza eseguirla
    def simulate(self, match):
        # Clona l'oggetto match
        match = copy(match)

        # Clona l'azione e imposta il match clonato
        sim_action = copy(self)
        sim_action.match = match

        # Verifica se l'azione può essere eseguita e la esegue
        if sim_action.can_execute():
            sim_action.execute()

        # Restituisce il match dopo l'esecuzione dell'azione
        return match