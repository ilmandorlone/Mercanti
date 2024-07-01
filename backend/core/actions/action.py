# classe base action che implementa il metodo execute e can execute

from copy import copy, deepcopy

import numpy as np

from core.models import ContextMatch


class Action:
    def __init__(self, context_match: ContextMatch, player_id: int):
        self.context_match = context_match
        self.player_id = player_id

    def can_execute(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
    
    def execute_on_context(self, context_match : ContextMatch):
        raise NotImplementedError
    
    # Metodo per simulare l'azione senza eseguirla
    def execute_on_data_array(self, data: np.array):
        raise NotImplementedError
        
