from itertools import combinations
import json
from typing import List
from collections import Counter
import logging
from core.turn_manager import TurnManager
from core.human_player import HumanPlayer
from core.cpu_player import CPUPlayer
from core.actions.action import Action
from core.models import ColorEnum, ContextMatch, ListCardCount, ListTokenCount, Player, Card, Noble, TokenAction, TokenActionEnum
import random

logger = logging.getLogger(__name__)

class Match:
    def __init__(self, players: List[Player]):
        # ContextMatch
        self.context = ContextMatch(
            players=players,
            tokens=ListTokenCount(),
            deck_level1=[],
            deck_level2=[],
            deck_level3=[],
            visible_level1=[],
            visible_level2=[],
            visible_level3=[],
            visible_passengers=[],
            round=0
        )

        # Inizializza il manager dei turni
        self.turn_manager = TurnManager(players)

        # Inizializza i gettoni in base al numero di giocatori
        token_init_by_players = { 2: 4, 3: 5, 4: 7 }
        token_init = token_init_by_players[len(players)]

        # Inizializza i gettoni disponibili iniziali
        self.context.tokens.violet = token_init
        self.context.tokens.blue = token_init
        self.context.tokens.green = token_init
        self.context.tokens.red = token_init
        self.context.tokens.black = token_init
        self.context.tokens.gold = token_init

    def load_cards(self, file_path: str, randomizer: random.Random = random.Random()):
        with open(file_path, "r") as file:
            data = json.load(file)

            def transform_card(card):
                return Card(
                    id=card["id"],
                    level=card["level"],
                    color=card["color"],
                    cost=ListTokenCount(**card["cost"]),
                    points=card["points"]
                )

            def transform_passenger(passenger):
                return Noble(
                    id=passenger["id"],
                    cost=ListCardCount(**passenger["cost"]),
                    points=passenger["points"]
                )

            #self.deck_level2 = [Card(**transform_card(card)) for card in data.get("level_II", [])]
            self.context.deck_level1 = [transform_card(card) for card in data.get("level_I", [])]
            self.context.deck_level2 = [transform_card(card) for card in data.get("level_II", [])]
            self.context.deck_level3 = [transform_card(card) for card in data.get("level_III", [])]
            passengers_deck = [transform_passenger(passenger) for passenger in data.get("passengers", [])]

            randomizer.shuffle(self.context.deck_level1)
            randomizer.shuffle(self.context.deck_level2)
            randomizer.shuffle(self.context.deck_level3)
            randomizer.shuffle(passengers_deck)

            logger.info("Loaded cards from setup.json")
        
        # Inizializza i Nobili visibili
        while len(self.context.visible_passengers) < len(self.context.players) + 1 and passengers_deck:
            self.context.visible_passengers.append(passengers_deck.pop(0))

        # Inizializza le carte visibili
        self.refill_visible_cards()

    def refill_visible_cards(self):
        while len(self.context.visible_level1) < 4 and self.context.deck_level1:
            self.context.visible_level1.append(self.context.deck_level1.pop(0))
        while len(self.context.visible_level2) < 4 and self.context.deck_level2:
            self.context.visible_level2.append(self.context.deck_level2.pop(0))
        while len(self.context.visible_level3) < 4 and self.context.deck_level3:
            self.context.visible_level3.append(self.context.deck_level3.pop(0))

    def select_deck_level_by_level(self, level: int):
        if level == 1:
            return self.context.deck_level1
        elif level == 2:
            return self.context.deck_level2
        elif level == 3:
            return self.context.deck_level3
        else:
            raise ValueError(f"Invalid level {level}")

    def get_next_card_id_by_level(self, level: int):
        return self.select_deck_level_by_level(level)[0].id
    
    # Avvia la partita eseugendo i turni dei giocatori
    def run(self):
        winner = None
        counter_no_action = 0

        while 1:
            self.context.round += 1

            for player in self.context.players:
                try:
                    # esegui la callback per ottenere l'azione del giocatore
                    player.callback_move(self, player)

                    # Resetta il contatore di no action
                    counter_no_action = 0

                except Exception as e:
                    if str(e) == "No actions available":
                        # Se il giocatore non può eseguire azioni, incrementa il contatore
                        counter_no_action += 1

                        # Se tutti i giocatori non possono eseguire azioni, termina il gioco
                        if counter_no_action == len(self.context.players):
                            raise ValueError("No actions available")
                    else:
                        # Se viene sollevata un'altra eccezione, interrompi la partita
                        raise e

                # Verifica se il giocatore ha vinto
                if player.points >= 15:
                    winner = player
            
            if winner:
                return winner
