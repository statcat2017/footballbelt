
def result(match):
    if match['hgoal'] > match['vgoal']:
        return (1,match['home'],match['visitor'])
    elif match['hgoal'] < match['vgoal']:
        return (-1,match['visitor'],match['home'])
    else:
        return (0,'draw','draw')

class Reign:
    def __init__(self, match_won):
        self.champion = result(match_won)[1]
        self.start_date = match_won['Date']
        self.won_from = result(match_won)[2]
        self.end_date = None
        self.lost_to = None
        self.reign_duration = None
        self.defenses = 0
    
    def defended(self):
        self.defenses += 1

    def lost(self,match_lost):
        self.end_date = match_lost['Date']
        self.lost_to = result(match_lost)[1]
        self.reign_duration = (self.end_date - self.start_date).days

class Club:
    def __init__(self,champion):
        self.club = champion
        self.reigns = 0
        self.reign_duration = 0

    def add_reign(self,reign):
        self.reigns += 1
        self.reign_duration += reign.reign_duration
    
    
def is_defense(champion,match):
    if match['home'] == champion:
        return True
    if match['visitor'] == champion:
        return True
    return False

def defense(champion,match):
    new_champ = 0
    if match['home'] != champion and match['visitor'] != champion:
        raise ValueError("Champion is not in the match")
    opponent = match['home'] if match['home'] != champion else match['visitor'] 
    if result(match)[1] == champion or result(match)[1] == 'draw':
        pass
        #print (f"{champion} retains the belt against {opponent}")
    else:
        #print (f"{champion} loses the belt to {opponent}")
        champion = opponent
        new_champ = 1
    return (champion,new_champ)
    

