class Scoreboard:
    def __init__(self, score_num: int):
        self.scores = [0]*score_num

    def update(self, score_id):
        self.scores[score_id] += 1

    def get_score(self, score_id):
        return self.scores[score_id]
