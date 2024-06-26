# classe base action che implementa il metodo execute e can execute

class Action:
    def __init__(self, player_id):
        self.player_id = player_id

    def can_execute(self, match):
        raise NotImplementedError

    def execute(self, match):
        raise NotImplementedError