from core.models import Player, Card, Token
from core.match import Match

class MatchHelper:

    # Trova il giocatore con l'id specificato nella partita
    @staticmethod
    def get_player_by_id(match: Match, player_id: int) -> Player:
        for player in match.players:
            if player.id == player_id:
                return player
        return None

    # Trova la carta nei livelli visibili o nelle carte riservate
    @staticmethod
    def get_card_by_id(match: Match, card_id: int) -> Card:
        for player in match.players:
            # Verifica se la carta è tra le carte riservate del giocatore
            for card in player.reserved_cards:
                if card.id == card_id:
                    return card
            
            # Verifica se la carta è tra le carte visibili
            for level in [match.visible_level1, match.visible_level2, match.visible_level3]:
                for card in level:
                    if card.id == card_id:
                        return card
        return None
    
    # Rimuove la carta dalle carte visibili o dalle carte riservate
    @staticmethod
    def remove_card_from_visible_or_reserved(match: Match, card: Card):
        for player in match.players:
            if card in player.reserved_cards:
                player.reserved_cards.remove(card)
                player.reserved_cards_count -= 1
                return
        for level in [match.visible_level1, match.visible_level2, match.visible_level3]:
            if card in level:
                level.remove(card)
                return
            
    # Rimuove la carta dai livelli visibili
    @staticmethod
    def remove_card_from_visible(match: Match, card: Card):
        for level in [match.visible_level1, match.visible_level2, match.visible_level3]:
            if card in level:
                level.remove(card)
                return
        
        raise ValueError(f"Card with id {card.id} not found in visible cards")
    
    # Stato della partita per il giocatore con l'id specificato
    @staticmethod
    def get_game_state_by_id(match: Match, player_id: int):
        main_player = None
        opponents = []

        for player in match.players:
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
            "tokens": match.tokens,
            "remaining_cards": {
                "level1": len(match.deck_level1),
                "level2": len(match.deck_level2),
                "level3": len(match.deck_level3)
            },
            "visible_level1": [Card(**card.dict()) for card in match.visible_level1],
            "visible_level2": [Card(**card.dict()) for card in match.visible_level2],
            "visible_level3": [Card(**card.dict()) for card in match.visible_level3]
        }
