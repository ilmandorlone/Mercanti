from core.actions.get_all_possible_actions import get_all_possible_actions
from core.cpu_player import CPUPlayer
from core.models import CardCount, Player, Token
from core.match import Match
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class Provider:
    def __init__(self):
        self.matches: Dict[int, Match] = {}
        self.next_match_id = 0
        self.current_match = None

    def new_match(self, players: list[Player]) -> Match:
        match = self.matches[self.next_match_id] = Match(players)
        self.next_match_id += 1
        return match

    def remove_match(self, match_id: int):
        if match_id in self.matches:
            del self.matches[match_id]

    def get_match(self, match_id: int) -> Match:
        return self.matches.get(match_id)

    def list_matches(self) -> Dict[int, Match]:
        return self.matches
    
    def create_player(self, player_id: int, player_name: str) -> Player:
        return Player(
            id=player_id,
            name=player_name,
            cards_count=[CardCount(color="violet", count=0), CardCount(color="blue", count=0),
                         CardCount(color="green", count=0), CardCount(color="red", count=0),
                         CardCount(color="black", count=0)],
            tokens=[Token(color="violet", count=0), Token(color="blue", count=0),
                    Token(color="green", count=0), Token(color="red", count=0),
                    Token(color="black", count=0), Token(color="gold", count=0)],
            reserved_cards=[],
            reserved_cards_count=0,
            points=0)

    def create_cpu_player(self, player_id: int, player_name: str) -> CPUPlayer:
        return CPUPlayer(
            id=player_id,
            name=player_name,
            cards_count=[CardCount(color="violet", count=0), CardCount(color="blue", count=0),
                        CardCount(color="green", count=0), CardCount(color="red", count=0),
                        CardCount(color="black", count=0)],
            tokens=[Token(color="violet", count=0), Token(color="blue", count=0),
                    Token(color="green", count=0), Token(color="red", count=0),
                    Token(color="black", count=0), Token(color="gold", count=0)],
            reserved_cards=[],
            reserved_cards_count=0,
            points=0,
            passengers=[]
        )


# Singleton instance of Provider
provider_instance = Provider()
