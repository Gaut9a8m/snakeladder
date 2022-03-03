import sys, os, django, random

sys.path.extend(['/home/gautam1/Desktop/working/code/snakeladder'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snakeladder.settings")
django.setup()

from boardapp.models import Player, ScoreHistory

class Snakeladder:
    def __init__(self):
        self.snake_dict={'17':'7', '54':'34','62':'19','64':'60', '87':'24', '93':'73', '95':'75', '98':'79'}
        self.ladder_dict={'1':'38','4':'14', '9':'31', '21':'42', '28':'84', '51':'67', '71':'91', '80':'100'}

    def check_snake_ladder_player(self, step, chance, game_id):
        if str(step) in self.snake_dict:
            return [int(self.snake_dict[str(step)]), 'Oh NO!! Snake bites you.']
        elif str(step) in self.ladder_dict:
            return [int(self.ladder_dict[str(step)]),'Hurray!! you got ladder']
        else:
            token_cut =[]
            players_obj = Player.objects.filter(game = game_id)
            for i in range(len(players_obj)):
                if players_obj[i].overall_score == step and chance != i:
                    players_obj[i].overall_score = 0
                    # players_obj.save()
                    token_cut.append(players_obj[i].name)
            if token_cut:
                return [step,'Hurray!! you cut {} token'.format(token_cut)]
        return False

    def check_winner(self, score):
        if score == 100:
            return True
        return False

    def throwdice(self):
        return random.randint(1,6)
