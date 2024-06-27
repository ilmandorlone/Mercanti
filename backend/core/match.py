from itertools import combinations
import json
from typing import List
from collections import Counter
import logging
from core.turn_manager import TurnManager
from core.human_player import HumanPlayer
from core.cpu_player import CPUPlayer
from core.actions.action import Action
from core.models import CardCount, ColorEnum, Player, Card, Token, Passenger, TokenAction, TokenActionEnum
import random

logger = logging.getLogger(__name__)

class Match:
    def __init__(self, players: List[Player]):
        self.players = players
        self.round = 0
        self.turn_manager = TurnManager(players)

        # Inizializza i gettoni in base al numero di giocatori
        token_init_by_players = { 2: 4, 3: 5, 4: 7 }
        token_init = token_init_by_players[len(players)]

        self.tokens = [
            Token(color="violet", count=token_init),
            Token(color="blue", count=token_init),
            Token(color="green", count=token_init),
            Token(color="red", count=token_init),
            Token(color="black", count=token_init),
            Token(color="gold", count=token_init),
        ]

        self.deck_level1 : List[Card] = []
        self.deck_level2 : List[Card] = []
        self.deck_level3 : List[Card] = []
        self.visible_level1 : List[Card] = []
        self.visible_level2 : List[Card] = []
        self.visible_level3 : List[Card] = []
        self.passengers_deck : List[Passenger] = []
        self.visible_passengers : List[Passenger] = []

    def load_cards(self, file_path: str):
        with open(file_path, "r") as file:
            data = json.load(file)

            def transform_card(card):
                return Card(
                    id=card["id"],
                    level=card["level"],
                    color=card["color"],
                    cost=[Token(color=k, count=v) for k, v in card["cost"].items()],
                    points=card["points"]
                )

            def transform_passenger(passenger):
                return Passenger(
                    id=passenger["id"],
                    cost=[Token(color=k, count=v) for k, v in passenger["cost"].items()],
                    points=passenger["points"]
                )

            #self.deck_level2 = [Card(**transform_card(card)) for card in data.get("level_II", [])]
            self.deck_level1 = [transform_card(card) for card in data.get("level_I", [])]
            self.deck_level2 = [transform_card(card) for card in data.get("level_II", [])]
            self.deck_level3 = [transform_card(card) for card in data.get("level_III", [])]
            self.passengers_deck = [transform_passenger(passenger) for passenger in data.get("passengers", [])]

            random.shuffle(self.deck_level1)
            random.shuffle(self.deck_level2)
            random.shuffle(self.deck_level3)
            random.shuffle(self.passengers_deck)

            logger.info("Loaded cards from setup.json")
        
        # Inizializza i Nobili visibili
        while len(self.visible_passengers) < len(self.players) + 1 and self.passengers_deck:
            self.visible_passengers.append(self.passengers_deck.pop(0))

        # Inizializza le carte visibili
        self.refill_visible_cards()

    def refill_visible_cards(self):
        while len(self.visible_level1) < 4 and self.deck_level1:
            self.visible_level1.append(self.deck_level1.pop(0))
        while len(self.visible_level2) < 4 and self.deck_level2:
            self.visible_level2.append(self.deck_level2.pop(0))
        while len(self.visible_level3) < 4 and self.deck_level3:
            self.visible_level3.append(self.deck_level3.pop(0))

    def check_and_assign_passenger(self, player):        
        for passenger in self.visible_passengers:
            if all(any(cc.color == cost.color and cc.count >= cost.count for cc in player.cards_count) for cost in passenger.cost):
                player.points += passenger.points
                player.passengers.append(passenger)
                self.visible_passengers.remove(passenger)
                break

    def select_deck_level_by_level(self, level: int):
        if level == 1:
            return self.deck_level1
        elif level == 2:
            return self.deck_level2
        elif level == 3:
            return self.deck_level3
        else:
            raise ValueError(f"Invalid level {level}")

    def get_next_card_id_by_level(self, level: int):
        return self.select_deck_level_by_level(level)[0].id
    
    def run(self):
        winner = None

        while 1:
            self.round += 1

            for player in self.players:
                # esegui la callback per ottenere l'azione del giocatore
                # cast di player a CPUPlayer per chiamare la callback
                player.callback_move(self, player)

                # Verifica se il giocatore ha vinto
                if player.points >= 15:
                    winner = player
            
            if winner:
                return winner
