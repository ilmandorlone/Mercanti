import json
import time
from typing import List
import random
import os
import sys

# Determina il percorso della directory principale del progetto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Aggiungi il percorso al sys.path
sys.path.append(project_root)

from tests.test_converter_context_to_np_array import test_convert_context_match_to_status_game_for_ai_player

test_convert_context_match_to_status_game_for_ai_player()