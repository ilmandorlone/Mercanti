from core.actions.get_all_possible_actions import get_all_possible_actions
from core.cpu_player import CPUPlayer
from core.models import ListCardCount, ListTokenCount, Player
from core.match import Match
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class Provider:
    def __init__(self):
        self.matches: Dict[int, Match] = {}
        self.next_match_id = 0
        self.current_match: Match = None

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
    
    def create_player(self, id: int, name: str) -> Player:
        return Player(
            id=id,
            name=name,
            cards_count=ListCardCount(),
            tokens=ListTokenCount(),
            points=0)

    def create_cpu_player(self, id: int, name: str) -> CPUPlayer:
        return CPUPlayer(
            id=id,
            name=name,
            cards_count=ListCardCount(),
            tokens=ListTokenCount(),
            points=0,
            passengers=[]
        )


# Singleton instance of Provider
provider_instance = Provider()
