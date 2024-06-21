from typing import List
from .models import Player, Card, Token, LevelDeck, CardCount, Passenger
from .schemas import CardSchema, TokenSchema, TokenActionSchema, PassengerSchema
import json
import random
from collections import Counter
import logging

# In-memory storage for simplicity
players = [
    Player(
        id=1, 
        name="Player 1", 
        cards_count=[],
        tokens=[ Token(color="violet", count=0), Token(color="blue", count=0),
                Token(color="green", count=0), Token(color="red", count=0),
                Token(color="black", count=0), Token(color="gold", count=0)], 
        reserved_cards=[], 
        reserved_cards_count=0, 
        points=0
    ),
    Player(
        id=2, 
        name="Player 2", 
        cards_count=[],
        tokens=[ Token(color="violet", count=0), Token(color="blue", count=0),
                Token(color="green", count=0), Token(color="red", count=0),
                Token(color="black", count=0), Token(color="gold", count=0)], 
        reserved_cards=[], 
        reserved_cards_count=0, 
        points=0
    ),
]

tokens = [
    Token(color="violet", count=5),
    Token(color="blue", count=5),
    Token(color="green", count=5),
    Token(color="red", count=5),
    Token(color="black", count=5),
    Token(color="gold", count=5),
]

deck_level1 = []
deck_level2 = []
deck_level3 = []

visible_level1 = []
visible_level2 = []
visible_level3 = []

passengers_deck = []
visible_passengers = []

logger = logging.getLogger(__name__)

def load_cards(file_path: str):
    global deck_level1, deck_level2, deck_level3, passengers_deck

    with open(file_path, "r") as file:
        data = json.load(file)

        def transform_card(card):
            return {
                "id": card["id"],
                "level": card["level"],
                "color": card["color"],
                "cost": [{"color": k, "count": v} for k, v in card["cost"].items()],
                "points": card["points"]
            }
        
        def transform_passenger(passenger):
            return {
                "id": passenger["id"],
                "cost": [{"color": k, "count": v} for k, v in passenger["cost"].items()],
                "points": passenger["points"]
            }

        # Contatori per i gettoni
        token_counters = {
            "level_I": Counter(),
            "level_II": Counter(),
            "level_III": Counter()
        }

        deck_level1 = [CardSchema(**transform_card(card)) for card in data.get("level_I", [])]
        deck_level2 = [CardSchema(**transform_card(card)) for card in data.get("level_II", [])]
        deck_level3 = [CardSchema(**transform_card(card)) for card in data.get("level_III", [])]
        passengers_deck = [PassengerSchema(**transform_passenger(passenger)) for passenger in data.get("passengers", [])]

        # Log dei contatori
        logger.info(f"Token counters for level I: {token_counters['level_I']}")
        logger.info(f"Token counters for level II: {token_counters['level_II']}")
        logger.info(f"Token counters for level III: {token_counters['level_III']}")


        # Shuffle the decks
        random.shuffle(deck_level1)
        random.shuffle(deck_level2)
        random.shuffle(deck_level3)
        random.shuffle(passengers_deck)

def refill_visible_passengers():
    global visible_passengers
    while len(visible_passengers) < 4 and passengers_deck:
        visible_passengers.append(passengers_deck.pop(0))

def refill_visible_cards():
    global visible_level1, visible_level2, visible_level3

    def refill(deck, visible):
        while len(visible) < 4 and deck:
            visible.append(deck.pop(0))

    refill(deck_level1, visible_level1)
    refill(deck_level2, visible_level2)
    refill(deck_level3, visible_level3)

def get_game_state_by_id(player_id: int):
    main_player = None
    opponents = []

    for player in players:
        # Se i dati dei giocatori sono inizializzati correttamente, non è necessario questo conteggio
        cards_count = player.cards_count
        
        if player.id == player_id:
            main_player = Player(
                id=player.id,
                name=player.name,
                cards_count=cards_count,
                tokens=player.tokens,
                reserved_cards=player.reserved_cards,
                reserved_cards_count=len(player.reserved_cards),
                points=player.points
            )
        else:
            opponent = Player(
                id=player.id,
                name=player.name,
                cards_count=cards_count,
                tokens=player.tokens,
                reserved_cards=[],
                reserved_cards_count=len(player.reserved_cards),
                points=player.points
            )
            opponents.append(opponent)

    if main_player is None:
        raise ValueError(f"Player with id {player_id} not found")

    return {
        "player": main_player,
        "opponents": opponents,
        "tokens": tokens,
        "remaining_cards": {
            "level1": len(deck_level1),
            "level2": len(deck_level2),
            "level3": len(deck_level3)
        },
        "visible_level1": [Card(**card.dict()) for card in visible_level1],
        "visible_level2": [Card(**card.dict()) for card in visible_level2],
        "visible_level3": [Card(**card.dict()) for card in visible_level3],
        "visible_passengers": [Passenger(**passenger.dict()) for passenger in visible_passengers],
    }

def get_players():
    return players

def get_tokens():
    return tokens

def get_cards(level: int):
    if level == 1:
        return deck_level1
    elif level == 2:
        return deck_level2
    elif level == 3:
        return deck_level3
    return []

def update_player(player_id: int, updated_player: Player):
    for i, player in enumerate(players):
        if player.id == player_id:
            players[i] = updated_player
            return players[i]
    return None

def update_tokens(new_tokens: List[Token]):
    global tokens
    tokens = new_tokens

def update_cards(level: int, new_cards: List[Card]):
    global deck_level1, deck_level2, deck_level3
    if level == 1:
        deck_level1 = new_cards
    elif level == 2:
        deck_level2 = new_cards
    elif level == 3:
        deck_level3 = new_cards


def purchase_card(player_id: int, card_id: int):
    # Trova il giocatore
    player = next((p for p in players if p.id == player_id), None)
    if not player:
        raise ValueError(f"Player with id {player_id} not found")

    # Trova la carta nei livelli visibili o nelle carte riservate
    card = next((c for c in player.reserved_cards if c.id == card_id), None)
    if not card:
        for level in [visible_level1, visible_level2, visible_level3]:
            card = next((c for c in level if c.id == card_id), None)
            if card:
                break
    
    if not card:
        raise ValueError(f"Card with id {card_id} not found in visible cards or reserved cards")

    # Crea un contatore per i gettoni del giocatore
    token_counter = Counter({token.color: token.count for token in player.tokens})
    
    # Crea un contatore per gli sconti basati sulle carte possedute
    discount_counter = Counter({count.color: count.count for count in player.cards_count})
    
    # Calcola i gettoni mancanti considerando gli sconti
    missing_tokens = 0
    for cost in card.cost:
        effective_cost = max(0, cost.count - discount_counter[cost.color])  # Applica lo sconto
        if token_counter[cost.color] < effective_cost:
            missing_tokens += effective_cost - token_counter[cost.color]

    # Verifica se i jolly possono coprire i gettoni mancanti
    if missing_tokens > token_counter['gold']:
        raise ValueError(f"Not enough tokens to purchase the card: {card_id}")

    # Deduce il costo dai gettoni del giocatore e restituirli al tavolo
    for cost in card.cost:
        effective_cost = max(0, cost.count - discount_counter[cost.color])  # Applica lo sconto
        if token_counter[cost.color] >= effective_cost:
            token_counter[cost.color] -= effective_cost
            # Aggiungi i gettoni pagati al tavolo
            for token in tokens:
                if token.color == cost.color:
                    token.count += effective_cost
        else:
            needed = effective_cost - token_counter[cost.color]
            # Assegna i gettoni disponibili e il resto con i gettoni gold
            for token in tokens:
                if token.color == cost.color:
                    token.count += token_counter[cost.color]
                if token.color == 'gold':
                    token.count += needed
            token_counter[cost.color] = 0
            token_counter['gold'] -= needed

    player.tokens = [Token(color=color, count=max(count, 0)) for color, count in token_counter.items()]

    # Aggiungi la carta al giocatore o aggiorna il conteggio
    found = False
    for card_count in player.cards_count:
        if card_count.color == card.color:
            card_count.count += 1
            found = True
            break

    if not found:
        player.cards_count.append(CardCount(color=card.color, count=1))

    player.points += card.points

    # Rimuovi la carta dalle carte riservate o dal livello visibile
    if card in player.reserved_cards:
        player.reserved_cards.remove(card)
        player.reserved_cards_count -= 1
    else:
        for level in [visible_level1, visible_level2, visible_level3]:
            if card in level:
                level.remove(card)
                break

    # Refill le carte visibili se necessario
    refill_visible_cards()
    
    # Verifica e assegna le tessere passeggeri
    check_and_assign_passenger(player)

def check_and_assign_passenger(player):
    global visible_passengers
    for passenger in visible_passengers:
        if all(any(cc.color == cost.color and cc.count >= cost.count for cc in player.cards_count) for cost in passenger.cost):
            player.points += passenger.points
            player.passengers.append(passenger)
            visible_passengers.remove(passenger)
            break

def reserve_card(player_id: int, level: int, card_id: int = None):
    # Trova il giocatore
    player = next((p for p in players if p.id == player_id), None)
    if not player:
        raise ValueError(f"Player with id {player_id} not found")

    # Verifica che il giocatore non abbia più di 3 carte riservate
    if len(player.reserved_cards) >= 3:
        raise ValueError("Player cannot reserve more than 3 cards")

    # Seleziona il mazzo e le carte visibili in base al livello
    if level == 1:
        deck = deck_level1
        visible = visible_level1
    elif level == 2:
        deck = deck_level2
        visible = visible_level2
    elif level == 3:
        deck = deck_level3
        visible = visible_level3
    else:
        raise ValueError("Invalid level")

    # Riserva la carta visibile o dal mazzo nascosto
    if card_id:
        card_schema = next((c for c in visible if c.id == card_id), None)
        if not card_schema:
            raise ValueError(f"Card with id {card_id} not found in visible cards")
        visible.remove(card_schema)
    else:
        if not deck:
            raise ValueError(f"No cards available in level {level} deck")
        card_schema = deck.pop(0)

    # Converti CardSchema a Card
    card = Card(**card_schema.dict())

    player.reserved_cards.append(card)
    player.reserved_cards_count += 1

    # Aggiungi un gettone "gold" al giocatore se disponibile
    gold_token = next((t for t in tokens if t.color == 'gold' and t.count > 0), None)
    if gold_token:
        gold_token.count -= 1
        player_gold_token = next((t for t in player.tokens if t.color == 'gold'), None)
        if player_gold_token:
            player_gold_token.count += 1
        else:
            player.tokens.append(Token(color='gold', count=1))

    # Refill le carte visibili se necessario
    refill_visible_cards()

def select_token(player_id: int, token_actions: List[TokenActionSchema]):
    # Trova il giocatore
    player = next((p for p in players if p.id == player_id), None)
    if not player:
        raise ValueError(f"Player with id {player_id} not found")

    # Verifica che non ci siano più di 3 gettoni selezionati per l'acquisto
    buy_actions = [action for action in token_actions if action.action == "buy"]
    if len(buy_actions) > 3:
        raise ValueError("Cannot buy more than 3 tokens at a time")

    # Verifica che i colori dei gettoni selezionati per l'acquisto siano validi
    buy_colors = [action.color for action in buy_actions]
    if len(buy_colors) != len(set(buy_colors)):  # Duplicate colors
        if len(buy_colors) != 2 or buy_colors[0] != buy_colors[1]:
            raise ValueError("If buying 2 tokens, they must be of the same color")
        # Verifica che ci siano almeno 4 gettoni disponibili di quel colore
        available_token = next((t for t in tokens if t.color == buy_colors[0]), None)
        if not available_token or available_token.count < 4:
            raise ValueError("There must be at least 4 tokens available of the selected color to buy 2")
    else:
        # Verifica che i colori siano tutti diversi
        if len(buy_colors) != len(set(buy_colors)):
            raise ValueError("All selected tokens must be of different colors")

    total_tokens_after_action = sum(token.count for token in player.tokens)

    # Processa ogni azione
    for action in token_actions:
        table_token = next((t for t in tokens if t.color == action.color), None)
        player_token = next((t for t in player.tokens if t.color == action.color), None)

        if action.action == "buy":
            if action.color == "gold":
                raise ValueError("Cannot buy gold tokens")
            if table_token and table_token.count >= action.count:
                if action.count == 2 and table_token.count < 4:
                    raise ValueError("There must be at least 4 tokens available to buy 2 of the same color")
                table_token.count -= action.count
                if player_token:
                    player_token.count += action.count
                else:
                    player.tokens.append(Token(color=action.color, count=action.count))
                total_tokens_after_action += action.count
            else:
                raise ValueError(f"Not enough tokens available for color {action.color}")

        elif action.action == "return":
            if player_token and player_token.count >= action.count:
                player_token.count -= action.count
                if table_token:
                    table_token.count += action.count
                else:
                    tokens.append(Token(color=action.color, count=action.count))
                total_tokens_after_action -= action.count
            else:
                raise ValueError(f"Not enough tokens to return for color {action.color}")

        else:
            raise ValueError("Invalid action. Must be 'buy' or 'return'.")

    # Verifica che la somma dei gettoni non superi 10
    if total_tokens_after_action > 10:
        raise ValueError("Cannot have more than 10 tokens in total after the action")

    player.tokens = [Token(color=token.color, count=token.count) for token in player.tokens if token.count > 0]
