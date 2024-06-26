from core.models import Player

class HumanPlayer(Player):
    def __init__(self, player_id: int, player_name: str):
        super().__init__(player_id, player_name)
        self.is_cpu = False

    def play(self):
        print(f"Human Player {self.name} is playing...")