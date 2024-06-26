from typing import List

from core.cpu_player import CPUPlayer
from core.models import Player

class TurnManager:
    def __init__(self, players: List[Player]):
        self.current_player_id = 1
        self.round = 0
        self.players = players
        self.winner = None
        self.temp_winner = None

    def next_turn(self):
        # Player correspondente al turno attuale
        current_player = self.players[self.current_player_id - 1]

        # Se il giocatore è un CPU, esegue la mossa automaticamente
        if isinstance(current_player, CPUPlayer):
            current_player.move_callback()

            # Termina il turno
            self.end_turn(self.current_player_id)
        else:
            # Se il giocatore è un giocatore umano, aspetta l'input
            print(f"Player {current_player.id} turn")
    
    def end_turn(self, player_id):
        # Verifica che sia il turno del giocatore
        if not self.check_turn_id(player_id):
            raise ValueError(f"Player {player_id} is not the current player")

        # Incrementa il round
        if player_id == 1:
            self.round += 1
            print(f"Round: {self.round}")

        # Verifica se il giocatore ha vinto
        if self.players[player_id - 1].points >= 15:
            self.temp_winner = self.players[player_id - 1]
        
        # Verifica se ha giocato l'ultimo giocatore
        if self.temp_winner and self.current_player_id == len(self.players):
            # Trova il giocatore con il punteggio più alto
            max_points = max([player.points for player in self.players])
            self.winner = [player for player in self.players if player.points == max_points]
            print(f"Winner is {self.winner[0].name} with {self.winner[0].points} points")
            return

        # Passa al prossimo turno
        self.current_player_id = ((self.current_player_id) % len(self.players)) + 1

        # Esegue il prossimo turno
        self.next_turn()

    def check_turn_id(self, player_id):
        return self.current_player_id == player_id