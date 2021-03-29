class Player:
    name = ""
    score = 0
    powerup = ""
    # difficulty could modify how much the words are obscured at the start
    # difficulty  = 1

    def __init__(self, name):
        self.name = name

    def mod_score(self, score_modifier):
        self.score += score_modifier * 100

    def buy_powerup(self, power):
        if power == "A":
            print("USING POWERUP A")
            powerup = "A"
        elif power == "B":
            print("USING POWERUP B")
            powerup = "B"