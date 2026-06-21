import json
import os

THRESHOLD_FILE = os.path.join(os.path.dirname(__file__), '..', 'thresholds.json')

def get_thresholds():
    with open(THRESHOLD_FILE, 'r') as f:
        return json.load(f)

def set_thresholds(data):
    with open(THRESHOLD_FILE, 'w') as f:
        json.dump(data, f)