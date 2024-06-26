from core.models import Player

class CPUPlayer(Player):
    def __init__(self, id: int, name: str):
        super().__init__(
            id=id,
            name=name,
            cards_count=[],
            tokens=[],
            reserved_cards=[],
            reserved_cards_count=0,
            points=0,
            passengers=[]
        )