import json
import os

IMUNES_PATH = 'data/imunes.json'

def load_imunes():
    if not os.path.exists(IMUNES_PATH):
        return []
        
    with open(IMUNES_PATH, 'r') as f:
        return json.load(f)
    
def save_imunes(imunes):
    with open(IMUNES_PATH, 'w') as f:
        json.dump(imunes, f)