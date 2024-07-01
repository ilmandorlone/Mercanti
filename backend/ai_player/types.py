from dataclasses import dataclass
from enum import Enum
import numpy as np

# Enumerazione dei colori delle carte
class ColorEnum_NP(int, Enum):
    VIOLET = 0
    BLUE = 1
    GREEN = 2
    RED = 3
    BLACK = 4
    GOLD = 5

# Enumerazione per lo stato di dove si trova la carta
class StatusCardEnum_NP(str, Enum):
    UNKNOWN_LEVEL1 = 0          # Sconosciuto Livello 1
    UNKNOWN_LEVEL2 = 1          # Sconosciuto Livello 2
    UNKNOWN_LEVEL3 = 2          # Sconosciuto Livello 3   
    ON_DECK_LEVEL1 = 3          # Nel mazzo di carte di livello 1 nascosto
    ON_DECK_LEVEL2 = 4          # Nel mazzo di carte di livello 2 nascosto
    ON_DECK_LEVEL3 = 5          # Nel mazzo di carte di livello 3 nascosto    
    VISIBLE_LEVEL1 = 6          # Nelle carte visibili di livello 1
    VISIBLE_LEVEL2 = 7          # Nelle carte visibili di livello 2
    VISIBLE_LEVEL3 = 8          # Nelle carte visibili di livello 3   
    RESERVED_PLAYER1 = 9        # Riservata dal giocatore 1
    RESERVED_PLAYER2 = 10       # Riservata dal giocatore 2
    RESERVED_PLAYER3 = 11       # Riservata dal giocatore 3
    RESERVED_PLAYER4 = 12       # Riservata dal giocatore 4   
    PURCHASED_PLAYER1 = 13      # Acquistata dal giocatore 1
    PURCHASED_PLAYER2 = 14      # Acquistata dal giocatore 2
    PURCHASED_PLAYER3 = 15      # Acquistata dal giocatore 3
    PURCHASED_PLAYER4 = 16      # Acquistata dal giocatore 4

# Enumerazione per le azioni possibili
class ActionEnum_NP(str, Enum):
    PURCHASE_CARD = 0           # Azione per acquistare una carta
    PURCHASE_RESERVED_CARD = 1  # Azione per acquistare una carta riservata
    RESERVE_VISIBLE_CARD = 2    # Azione per riservare una carta visibile
    RESERVE_DECK_CARD = 3       # Azione per riservare una carta dal mazzo
    BUY_3_DIFFERENT_TOKENS = 4  # Azione per comprare 3 gettoni diversi
    BUY_2_DIFFERENT_TOKENS = 5  # Azione per comprare 2 gettoni diversi
    BUY_1_TOKEN = 6             # Azione per comprare 1 gettone
    BUY_2_SAME_TOKENS = 7       # Azione per comprare 2 gettoni uguali

# Enumerazione retun gettoni
class ReturnTokensEnum_NP(str, Enum):
    RETURN_NONE = 0             # Non si sta restituendo nessun gettone
    RETURN_1_TOKEN = 1          # Si sta restituendo 1 gettone
    RETURN_2_TOKENS = 2         # Si stanno restituendo 2 gettoni
    RETURN_3_TOKENS = 3         # Si stanno restituendo 3 gettoni

# Enumerazione dello stato dei nobili
class StatusNobleEnum_NP(str, Enum):
    NOT_USED = 0                # Non utilizzato nella partita
    UNASSIGNED = 1              # Non assegnato a nessun giocatore
    ASSIGNED_PLAYER1 = 2        # Assegnato al giocatore 1
    ASSIGNED_PLAYER2 = 3        # Assegnato al giocatore 2
    ASSIGNED_PLAYER3 = 4        # Assegnato al giocatore 3
    ASSIGNED_PLAYER4 = 5        # Assegnato al giocatore 4

# Stato della carta np
dtype_status_card = np.dtype([
    ('position', np.uint8)      # Posizione stato della carta
])

# Stato del nobile np
dtype_noble = np.dtype([
    ('position', np.uint8)      # Posizione stato del nobile
])

# Stato del giocatore
dtype_status_player = np.dtype([
    ('tokens_violet', np.uint8),
    ('tokens_blue', np.uint8),
    ('tokens_green', np.uint8),
    ('tokens_red', np.uint8),
    ('tokens_black', np.uint8),
    ('tokens_gold', np.uint8),
    ('cards_violet', np.uint8),
    ('cards_blue', np.uint8),
    ('cards_green', np.uint8),
    ('cards_red', np.uint8),
    ('cards_black', np.uint8),
    ('points', np.uint8)
])

# Stato del gioco
dtype_status_game = np.dtype([
    ('round', np.uint8),
    ('player_id', np.uint8),
    ('tokens_violet', np.uint8),
    ('tokens_blue', np.uint8),
    ('tokens_green', np.uint8),
    ('tokens_red', np.uint8),
    ('tokens_black', np.uint8),
    ('tokens_gold', np.uint8),
    ('player', dtype_status_player),
    ('opponents', (dtype_status_player, 3)),
    ('cards_level1', (dtype_status_card, 40)),
    ('cards_level2', (dtype_status_card, 30)),
    ('cards_level3', (dtype_status_card, 20)),
    ('nobles', (dtype_noble, 10))
])

# Stato del gioco prima e dopo l'azione
dtype_status_before_afterAction = np.dtype([
    ('before', dtype_status_game),
    ('after', dtype_status_game),
    ('action_type', np.uint8),
    ('return_tokens', np.uint8)
])
