import base64
import json
import time
from .singleton import Singleton


class ScoreKeeper(metaclass=Singleton):
    def __init__(self):
        self.score_file = "scores.bin"

    def read_scores(self):
        scores = []
        try:
            with open(self.score_file, "rb") as fp:
                for line in fp:
                    decoded_data = base64.b64decode(line.strip()).decode()
                    scores.append(json.loads(decoded_data))
        except FileNotFoundError:
            pass
        return scores

    def write_scores(self, score: int, game_time: int):
        entry = {
            "created_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "game_time": game_time,
            "score": score,
        }
        json_data = json.dumps(entry)
        encoded_data = base64.b64encode(json_data.encode())
        with open(self.score_file, "ab") as fp:
            fp.write(encoded_data + b"\n")
