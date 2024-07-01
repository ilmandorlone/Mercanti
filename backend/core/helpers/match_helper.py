from core.models import ContextMatch, Player, Card
from core.match import Match

class MatchHelper:

    # Trova il giocatore con l'id specificato nel contesto della partita
    @staticmethod
    def get_player_by_id_in_context(context_metch: ContextMatch, player_id: int) -> Player:
        for player in context_metch.players:
            if player.id == player_id:
                return player
        return None
    
    # Trova il giocatore con l'id specificato nella partita
    @staticmethod
    def get_player_by_id(match: Match, player_id: int) -> Player:
        return MatchHelper.get_player_by_id_in_context(match.context, player_id)

    # Trova la carta nei livelli visibili o nelle carte riservate nel contesto della partita
    @staticmethod
    def get_card_by_id_in_context(context_metch: ContextMatch, card_id: int) -> Card:
        for player in context_metch.players:
            # Verifica se la carta è tra le carte riservate del giocatore
            for card in player.reserved_cards:
                if card.card.id == card_id:
                    return card
            
            # Verifica se la carta è tra le carte visibili
            for level in [context_metch.visible_level1, context_metch.visible_level2, context_metch.visible_level3]:
                for card in level:
                    if card.id == card_id:
                        return card
        return None
    
    # Trova la carta nei livelli visibili o nelle carte riservate
    @staticmethod
    def get_card_by_id(match: Match, card_id: int) -> Card:
        return MatchHelper.get_card_by_id_in_context(match.context, card_id)
    
    # Rimuove la carta dalle carte visibili o dalle carte riservate nel contesto della partita
    @staticmethod
    def remove_card_from_visible_or_reserved_in_context(context_metch: ContextMatch, card: Card):
        for player in context_metch.players:
            if card in player.reserved_cards:
                # Rimuovi la carta dalle carte riservate del giocatore dove reserverd_card.card.id == card.id
                player.reserved_cards.remove(reserved_card for reserved_card in player.reserved_cards if reserved_card.card.id == card.id)
                player.reserved_cards_count -= 1
                return
        for level in [context_metch.visible_level1, context_metch.visible_level2, context_metch.visible_level3]:
            if card in level:
                level.remove(card)
                return
            
        raise ValueError(f"Card with id {card.id} not found in visible cards or reserved cards")
    
    # Rimuove la carta dalle carte visibili o dalle carte riservate
    @staticmethod
    def remove_card_from_visible_or_reserved(match: Match, card: Card):
        MatchHelper.remove_card_from_visible_or_reserved_in_context(match.context, card)
            
    # Rimuove la carta dai livelli visibili nel contesto della partita
    @staticmethod
    def remove_card_from_visible_in_context(context_metch: ContextMatch, card: Card):
        for level in [context_metch.visible_level1, context_metch.visible_level2, context_metch.visible_level3]:
            if card in level:
                level.remove(card)
                return
        
        raise ValueError(f"Card with id {card.id} not found in visible cards")
            
    # Rimuove la carta dai livelli visibili
    @staticmethod
    def remove_card_from_visible(match: Match, card: Card):
        MatchHelper.remove_card_from_visible_in_context(match.context, card)

    # Refill le carte visibili se necessario
    @staticmethod
    def refill_visible_cards(context_match: ContextMatch):
        while len(context_match.visible_level1) < 4 and context_match.deck_level1:
            context_match.visible_level1.append(context_match.deck_level1.pop(0))
        while len(context_match.visible_level2) < 4 and context_match.deck_level2:
            context_match.visible_level2.append(context_match.deck_level2.pop(0))
        while len(context_match.visible_level3) < 4 and context_match.deck_level3:
            context_match.visible_level3.append(context_match.deck_level3.pop(0))

    # Verifica e assegna le tessere nobile al giocatore
    @staticmethod
    def check_and_assign_noble(match_context: ContextMatch, player: Player):
        for passenger in match_context.visible_passengers:
            # Verifica ha le carte necessarie per ottenere il nobile
            if player.cards_count.violet >= passenger.cost.violet and \
                player.cards_count.blue >= passenger.cost.blue and \
                player.cards_count.green >= passenger.cost.green and \
                player.cards_count.red >= passenger.cost.red and \
                player.cards_count.black >= passenger.cost.black:

                player.points += passenger.points
                player.passengers.append(passenger)
                match_context.visible_passengers.remove(passenger)
                break

    # Seleziona il mazzo di carte in base al livello
    @staticmethod
    def select_deck_level_by_level(match_context: ContextMatch, level: int):
        if level == 1:
            return match_context.deck_level1
        elif level == 2:
            return match_context.deck_level2
        elif level == 3:
            return match_context.deck_level3
        else:
            raise ValueError(f"Invalid level {level}")
    
    # Stato della partita per il giocatore con l'id specificato
    @staticmethod
    def get_game_state_by_id(match: Match, player_id: int):
        main_player = None
        opponents = []

        for player in match.context.players:
            
            if player.id == player_id:
                main_player = Player(
                    id=player.id,
                    name=player.name,
                    cards_count=player.cards_count,
                    tokens=player.tokens,
                    reserved_cards=player.reserved_cards,
                    reserved_cards_count=len(player.reserved_cards),
                    points=player.points
                )
            else:
                opponent = Player(
                    id=player.id,
                    name=player.name,
                    cards_count=player.cards_count,
                    tokens=player.tokens,
                    reserved_cards=[],
                    reserved_cards_count=len(player.reserved_cards),
                    points=player.points
                )
                opponents.append(opponent)

        if main_player is None:
            raise ValueError(f"Player with id {player_id} not found")

        return {
            "player": main_player.to_dict(),
            "opponents": [opponent.to_dict() for opponent in opponents],
            "tokens": match.context.tokens,
            "remaining_cards": {
                "level1": len(match.context.deck_level1),
                "level2": len(match.context.deck_level2),
                "level3": len(match.context.deck_level3)
            },
            "visible_level1": match.context.visible_level1,
            "visible_level2": match.context.visible_level2,
            "visible_level3": match.context.visible_level3,
            "visible_passengers": match.context.visible_passengers
        }
