from typing import Any
from core.models import Player
from pydantic import BaseModel
from typing import List, Optional, Callable

class CPUPlayer(Player):
    callback_move: Optional[Callable[[dict], None]] = None
    
    def set_callback_move(self, callback: Any):
        self.callback_move = callback

    def move_callback(self):
        self.callback_move(self)