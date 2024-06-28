from collections import Counter
from typing import List
from core.utils import Utils
from core.models import Player, Card
from core.match import Match

class PlayerHelper:

    # Ottieni il numero totale di gettoni del giocatore
    @staticmethod
    def get_sum_tokens(player: Player) -> int:
        # Crea un contatore per i gettoni del giocatore {player.tokens.violet, player.tokens.blue, player.tokens.green, player.tokens.red, player.tokens.black, player.tokens.gold}
        return sum(vars(player.tokens).values())
    
    # Calcola quanti gettoni 'gold' deve usare il giocatore per acquistare la carta
    @staticmethod
    def get_gold_tokens_to_use(player: Player, card: Card) -> int:
        missing_tokens = 0

        # Calcola i gettoni mancanti considerando gli sconti
        missing_tokens -= min(0, player.tokens.violet + player.cards_count.violet - card.cost.violet)
        missing_tokens -= min(0, player.tokens.blue + player.cards_count.blue - card.cost.blue)
        missing_tokens -= min(0, player.tokens.green + player.cards_count.green - card.cost.green)
        missing_tokens -= min(0, player.tokens.red + player.cards_count.red - card.cost.red)
        missing_tokens -= min(0, player.tokens.black + player.cards_count.black - card.cost.black)

        return missing_tokens

    # Verifica che il giocatore abbia abbastanza gettoni per acquistare la carta (considerando gli sconti) o abbia abbastanza jolly
    @staticmethod
    def has_enough_tokens(player: Player, card: Card) -> bool:
        # Verifica se i jolly possono coprire i gettoni mancanti
        return player.tokens.gold >= PlayerHelper.get_gold_tokens_to_use(player, card)
    
    # Paga i gettoni necessari (considerando gli sconti) o jolly per acquistare la carta e restituiscili al tavolo
    @staticmethod
    def pay_tokens(player: Player, card: Card, match: Match):

        # Gettoni 'gold' necessari
        needed_gold = PlayerHelper.get_gold_tokens_to_use(player, card)

        # Verifica che il giocatore abbia abbastanza gettoni per acquistare la carta (considerando gli sconti) o abbia abbastanza jolly
        if player.tokens.gold < needed_gold:
            raise ValueError(f"Not enough tokens to purchase the card: {card.id}")
        
        # Calcola i gettoni che restano al giocatore dopo l'acquisto
        violet_after = max(0, player.tokens.violet - max(0, card.cost.violet - player.cards_count.violet))
        blue_after = max(0, player.tokens.blue - max(0, card.cost.blue - player.cards_count.blue))
        green_after = max(0, player.tokens.green - max(0, card.cost.green - player.cards_count.green))
        red_after = max(0, player.tokens.red - max(0, card.cost.red - player.cards_count.red))
        black_after = max(0, player.tokens.black - max(0, card.cost.black - player.cards_count.black))
        gold_after = max(0, player.tokens.gold - needed_gold)

        # Aggiungi i gettoni pagati al tavolo
        match.context.tokens.violet += player.tokens.violet - violet_after
        match.context.tokens.blue += player.tokens.blue - blue_after
        match.context.tokens.green += player.tokens.green - green_after
        match.context.tokens.red += player.tokens.red - red_after
        match.context.tokens.black += player.tokens.black - black_after
        match.context.tokens.gold += player.tokens.gold - gold_after

        # Aggiorna i gettoni del giocatore
        player.tokens.violet = violet_after
        player.tokens.blue = blue_after
        player.tokens.green = green_after
        player.tokens.red = red_after
        player.tokens.black = black_after
        player.tokens.gold = gold_after

    # Aggiungi la carta al giocatore e assegna i punti
    @staticmethod
    def add_card_to_player(player: Player, card: Card):
        # Aggiungi il conteggio delle carte possedute
        current_value = getattr(player.cards_count, card.color)
        setattr(player.cards_count, card.color, current_value + 1)

        # Aggiungi i punti al giocatore
        player.points += card.points
    
    # Aggiungi una carta riservata al giocatore
    @staticmethod
    def add_reserved_card_to_player(player: Player, card: Card):
        # Aggiungi la carta riservata al giocatore
        player.reserved_cards.append(card)
        
        # Aggiorna il conteggio delle carte riservate
        player.reserved_cards_count += 1
    
    # Aggiungi un gettone "gold" al giocatore se disponibile e se non ha già 10 gettoni
    @staticmethod
    def add_gold_token_to_player(player: Player, match: Match):
        # Verifica che il giocatore non abbia più di 10 gettoni
        if Utils.sum_object_attributes(player.tokens) >= 10:
            return

        # Verifica se ci sono gettoni "gold" disponibili
        if match.context.tokens.gold > 0:
            # Aggiungi il gettone "gold" al giocatore
            player.tokens.gold += 1

            # Rimuovi il gettone "gold" dal tavolo
            match.context.tokens.gold -= 1
