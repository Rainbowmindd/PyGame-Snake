import json
import os

class Scoreboard:
    def __init__(self):
        self.scores_file="highscores.json"
        self.highscores=self.load_scores()

    def load_scores(self):
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file,"r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    def save_scores(self):
        with open(self.scores_file,"w") as f:
            json.dump(self.highscores,f)
    
    def add_game_result(self,player1,player2):
        game_result={
            "player1": {"name": player1.player_name, "score": player1.score},
            "player2": {"name": player2.player_name, "score": player2.score},
            "winner": player1.player_name if player1.score > player2.score else player2.player_name
        }
        if self.highscores is None:
            self.highscores=[]
        self.highscores.append(game_result)
        self.highscores.sort(key=lambda x: max(x["player1"]["score"], x["player2"]["score"]), reverse=True)
        self.highscores=self.highscores[:5]
        self.save_scores()