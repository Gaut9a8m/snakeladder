from django.shortcuts import render, redirect
from django.http import HttpResponse
from helper.snakeladder_1 import *
from .models import GameMaster, Player, ScoreHistory
from django.views.generic import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here

board = Snakeladder()

def index(request):
    context = {}
    if request.session.get('gameId'):
        redirect('startgame')

    if request.method == 'POST':
        player_list = [name.title() for name in request.POST.getlist("players")]
        board.no_of_player = len(player_list)
        game_obj = GameMaster()
        game_obj.save()
        for name in player_list:
            player_obj = Player(
                game = game_obj,
                name = name
            )
            player_obj.save()
        request.session['gameId'] = game_obj.pk
        return redirect('startgame')
    return render(request,'boardapp/index.html')

def game(request):
    context = {}
    game_id = request.session.get('gameId')
    player_objs = Player.objects.filter(game=game_id).order_by('id')
    context['diceno'] = [int(i) for i in request.POST.getlist('diceno',[0])]
    context['players_stats'] = list(player_objs.values('name','overall_score'))

    if request.session.get('chance',None) and context['diceno'][-1] == 6:
        chance = request.session['chance']
        context['player_turn'] = player_objs[chance-1].name
        context['chance'] = chance
        context['msg'] = f'{context["player_turn"]} turn to roll dice.'
    elif request.session.get('chance',None):
        chance = (request.session['chance'] % len(player_objs)) + 1
        context['player_turn'] = player_objs[chance-1].name
        request.session['chance'] = chance
        context['chance'] = chance
        context['msg'] = f'last turn was of {context["player_turn"]}'
    else:
        request.session['chance'] = 1
        context['player_turn'] = player_objs[0].name
        context['chance'] = 1
        context['msg'] = f'last turn was of {context["player_turn"]}'


    if request.method == 'POST':
        player_turn = context['player_turn']
        player_score_history_obj = ScoreHistory.objects.filter(player__name = player_turn).order_by('-score')
        if not context['diceno']:
            context['diceno'].append(board.throwdice())

        else:
            if int(context['diceno'][-1]) == 6:
                if len(context['diceno']) > 2:
                    context['diceno'] = []
                    messages.error(request, 'Oh no!! 3 six in a row.')
                else:
                    context['diceno'].append(board.throwdice())
            else:
                context['diceno']=[]
                context['diceno'].append(board.throwdice())
        total_dice_val =0
        total_dice_val= sum(context['diceno'])
        player_obj = Player.objects.get(name = player_turn, game=game_id)

        # If user is first time getting 6 and his score history is empty
        if total_dice_val > 6 and player_obj.overall_score==0:
            print(f'first time six {context["player_turn"]}')
            score = total_dice_val - 6
            score_checked = board.check_snake_ladder_player(score, chance, game_id) #checking for snakes and ladder

            if score_checked:
                score = score_checked[0]
                messages.info(request, score_checked[1])
            ScoreHistory.objects.create(player = player_obj, score = score)
            player_obj.overall_score = score
            player_obj.save()
            context['score'] = score
            context['prev_score'] = 'block00'
            if score <= 9:
                context['next_score'] = f'block0{score-1}'
            else:
                context['next_score'] = f'block{score-1}'
        else:               # Update user score and checking for snake and ladder
            final_score = -1
            if player_obj and player_obj.overall_score:
                prev_score = player_obj.overall_score
                final_score = prev_score + total_dice_val

            score_checked = board.check_snake_ladder_player(final_score, chance, game_id)

            if score_checked:
                final_score = score_checked[0]
                messages.info(request, score_checked[1])
            if board.check_winner(final_score):
                messages.success(request, f'{player_turn} Won!!!!')
                del request.session['gameId']
                del request.session['chance']
                # return redirect('index')
            else:
                if final_score > 100:
                    final_score = prev_score
            if final_score != -1:
                ScoreHistory.objects.create(player = player_obj, score = final_score)
                player_obj.overall_score = final_score
                player_obj.save()
                context['score'] = final_score
                if prev_score <= 9:
                    context['prev_score'] = f'block0{prev_score-1}'
                else:
                    context['prev_score'] = f'block{prev_score-1}'
                if final_score <= 9:
                    context['next_score'] = f'block0{final_score-1}'
                else:
                    context['next_score'] = f'block{final_score-1}'
        if context['diceno']:
            context['dicepicno'] = context['diceno'][-1]
        context['players_stats'] = list(player_objs.values('name','overall_score'))
        print('\n\ncontext------------->',context)
        # return HttpResponse(json.dumps(context),content_type="application/json")
    return render(request,'boardapp/snakeladder.html',context)
