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
    UNKNOWN = 0                # Non si sa dove si trova la carta

    ON_DECK_LEVEL1 = 1         # Nel mazzo di carte di livello 1 nascosto
    ON_DECK_LEVEL2 = 2         # Nel mazzo di carte di livello 2 nascosto
    ON_DECK_LEVEL3 = 3         # Nel mazzo di carte di livello 3 nascosto
    
    VISIBLE_LEVEL1 = 4         # Nelle carte visibili di livello 1
    VISIBLE_LEVEL2 = 5         # Nelle carte visibili di livello 2
    VISIBLE_LEVEL3 = 6         # Nelle carte visibili di livello 3

    RESERVED_PLAYER1 = 7       # Riservata dal giocatore 1
    RESERVED_PLAYER2 = 8       # Riservata dal giocatore 2
    RESERVED_PLAYER3 = 9       # Riservata dal giocatore 3
    RESERVED_PLAYER4 = 10      # Riservata dal giocatore 4

    PURCHASED_PLAYER1 = 11     # Acquistata dal giocatore 1
    PURCHASED_PLAYER2 = 12     # Acquistata dal giocatore 2
    PURCHASED_PLAYER3 = 13     # Acquistata dal giocatore 3
    PURCHASED_PLAYER4 = 14     # Acquistata dal giocatore 4

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

@dataclass
class StatusCard_NP():
    id: int                      # Id della carta
    level: int                   # Livello della carta (1, 2, 3)
    color: ColorEnum_NP          # Colore della carta (violet, blue, green, red, black)
    points: int                  # Punti della carta
    cost_violet: int             # Costo in gettoni violet
    cost_blue: int               # Costo in gettoni blue
    cost_green: int              # Costo in gettoni green
    cost_red: int                # Costo in gettoni red
    cost_black: int              # Costo in gettoni black
    position: StatusCardEnum_NP  # Posizione della carta (deck, visible ...)

    # Definizione del dtype per NumPy
    dtype = np.dtype([
        ('id', np.uint8),
        ('level', np.uint8),
        ('color', np.uint8),
        ('points', np.uint8),
        ('cost_violet', np.uint8),
        ('cost_blue', np.uint8),
        ('cost_green', np.uint8),
        ('cost_red', np.uint8),
        ('cost_black', np.uint8),
        ('position', np.uint8)
    ])

# Stato del giocatore per l'AI
@dataclass
class StatusPlayerForAI_NP():
    tokens_violet: int                      # Numero di gettoni violet
    tokens_blue: int                        # Numero di gettoni blue
    tokens_green: int                       # Numero di gettoni green
    tokens_red: int                         # Numero di gettoni red
    tokens_black: int                       # Numero di gettoni black
    tokens_gold: int                        # Numero di gettoni gold
    cards_violet: int                       # Numero di carte violet
    cards_blue: int                         # Numero di carte blue
    cards_green: int                        # Numero di carte green
    cards_red: int                          # Numero di carte red
    cards_black: int                        # Numero di carte black
    points: int                             # Punti del giocatore
    reserved_cards_count: int               # Numero di carte riservate
    passengers_count: int                   # Numero di nobili ottenuti
    reserved_cards = np.zeros(3, dtype=StatusCard_NP.dtype) # Carte riservate dal giocatore (massimo 3)

    # Definizione del dtype per NumPy
    dtype = np.dtype([
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
        ('points', np.uint8),
        ('reserved_cards_count', np.uint8),
        ('passengers_count', np.uint8),
        ('reserved_cards', StatusCard_NP.dtype, 3)
    ])

class StatusGameForAI_NP():
    def __init__(self):
        self.round: int = 0                          # Numero del round
        self.player_id: int = 0                      # Id del giocatore che deve fare la mossa (1, 2, 3, 4)
        self.cards_array = np.zeros(90, dtype=StatusCard_NP.dtype)  # Array di carte di tutte le carte del gioco
    
    dtype = np.dtype([
        ('round', np.uint8),
        ('player_id', np.uint8),
        ('cards_array', (StatusCard_NP.dtype, 90))
    ])

# Stato del gioco prima e dopo la mossa
class StatusBeforeAfterAction():
    def __init__(self):
        self.before = StatusGameForAI_NP()          # Stato del gioco prima della mossa
        self.after = StatusGameForAI_NP()           # Stato del gioco dopo la mossa
        self.action_type: ActionEnum_NP             # Tipo di azione eseguita (acquisto, riserva, compra gettoni ...)
        self.return_tokens: ReturnTokensEnum_NP     # Gettoni restituiti al tavolo
    
    dtype = np.dtype([
        ('before', StatusGameForAI_NP.dtype),
        ('after', StatusGameForAI_NP.dtype),
        ('action_type', np.uint8),
        ('return_tokens', np.uint8)
    ])

# Lista di stati prima e dopo la mossa di n elementi per ogni combinazione di azione
class ListStatusBeforeAfterAction():
    def __init__(self, size: int):
        # Inizializza l'array con una dimensione fissa per ogni combinazione di azione
        self.array = np.zeros(size, dtype=StatusBeforeAfterAction.dtype)
        
    # Metodo per ottenere la dimensione della memoria allocata per l'array
    def get_allocated_size(self):
        return self.array.nbytes