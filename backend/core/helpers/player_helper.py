from collections import Counter
from typing import List
from core.models import CardCount, Player, Card, Token
from core.match import Match

class PlayerHelper:
    
    # Verifica che il giocatore abbia abbastanza gettoni per acquistare la carta (considerando gli sconti) o abbia abbastanza jolly
    @staticmethod
    def has_enough_tokens(player: Player, card: Card) -> bool:
        # Crea un contatore per i gettoni del giocatore
        token_counter = Counter({token.color: token.count for token in player.tokens})

        # Crea un contatore per gli sconti basati sulle carte possedute
        discount_counter = Counter({count.color: count.count for count in player.cards_count})
        
        # Calcola i gettoni mancanti considerando gli sconti
        missing_tokens = 0
        for cost in card.cost:
            # Calcola il costo effettivo considerando gli sconti
            effective_cost = max(0, cost.count - discount_counter[cost.color])

            # Verifica se il giocatore ha abbastanza gettoni
            if token_counter[cost.color] < effective_cost:
                missing_tokens += effective_cost - token_counter[cost.color]
        
        # Verifica se i jolly possono coprire i gettoni mancanti
        return missing_tokens <= token_counter['gold']
    
    # Paga i gettoni necessari (considerando gli sconti) o jolly per acquistare la carta e restituiscili al tavolo
    @staticmethod
    def pay_tokens(player: Player, card: Card, match: Match):
        needed_gold = 0

        # Crea un contatore per i gettoni del giocatore
        token_counter = Counter({token.color: token.count for token in player.tokens})
        
        # Crea un contatore per gli sconti basati sulle carte possedute
        discount_counter = Counter({count.color: count.count for count in player.cards_count})

        # Verifica che il giocatore abbia abbastanza gettoni per acquistare la carta (considerando gli sconti) o abbia abbastanza jolly
        if not PlayerHelper.has_enough_tokens(player, card):
            raise ValueError(f"Not enough tokens to purchase the card: {card.id}")
        
        # Lista dei gettoni pagati dal giocatore
        paid_tokens : List[Token] = []
        
        # Deduce il costo dai gettoni del giocatore
        for cost in card.cost:
            # Calcola il costo effettivo considerando gli sconti
            effective_cost = max(0, cost.count - discount_counter[cost.color])

            # Deduce il costo dai gettoni del giocatore
            if token_counter[cost.color] >= effective_cost:
                # Deduce i gettoni necessari
                token_counter[cost.color] -= effective_cost

                # Aggiungi i gettoni pagati alla lista
                paid_tokens.append(Token(color=cost.color, count=effective_cost))
            else:
                # Paga con i gettoni disponibili e il resto con i gettoni gold
                needed_gold = effective_cost - token_counter[cost.color]

                # Aggiungi i gettoni pagati alla lista
                paid_tokens.append(Token(color=cost.color, count=token_counter[cost.color]))

                # Azzera i gettoni del colore
                token_counter[cost.color] = 0

                # Deduce i gettoni gold necessari
                token_counter['gold'] -= needed_gold

                # Aggiungi i gettoni gold pagati alla lista
                # Verifica se è già presente un gettone gold nella lista dei gettoni pagati e aggiorna il conteggio
                gold_token = next((t for t in paid_tokens if t.color == 'gold'), None)
                if gold_token:
                    gold_token.count += needed_gold
                else:
                    paid_tokens.append(Token(color='gold', count=needed_gold))

        # Aggiorna i gettoni del giocatore
        player.tokens = [Token(color=color, count=max(count, 0)) for color, count in token_counter.items()]

        # Aggiungi i gettoni pagati al tavolo
        for paid_token in paid_tokens:
            table_token = next((t for t in match.tokens if t.color == paid_token.color), None)
            
            if table_token:
                table_token.count += paid_token.count
            else:
                match.tokens.append(Token(color=paid_token.color, count=paid_token.count))

    # Aggiungi la carta al giocatore e assegna i punti
    @staticmethod
    def add_card_to_player(player: Player, card: Card):
        # Aggiungi la carta al giocatore
        found = False
        for card_count in player.cards_count:
            if card_count.color == card.color:
                card_count.count += 1
                found = True
                break

        # Aggiungi un nuovo conteggio per la carta se non è già presente
        if not found:
            player.cards_count.append(CardCount(color=card.color, count=1))

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
        if len(player.tokens) >= 10:
            return

        # Verifica se ci sono gettoni "gold" disponibili
        gold_token = next((t for t in match.tokens if t.color == 'gold' and t.count > 0), None)
        
        # Aggiungi il gettone "gold" al giocatore
        if gold_token:
            gold_token.count -= 1
            player_gold_token = next((t for t in player.tokens if t.color == 'gold'), None)
            if player_gold_token:
                player_gold_token.count += 1
            else:
                player.tokens.append(Token(color='gold', count=1))
