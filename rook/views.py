from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.conf import settings
from rook.Game import Game

g = Game()

def index(request):
    template = loader.get_template("index.html")
    data = {}
    return HttpResponse(template.render(data, request))

def game(request):
    template = loader.get_template("game.html")
    data = {}
    return HttpResponse(template.render(data, request))

@require_http_methods(["POST"])
@csrf_exempt
def enter_game(request):
    return JsonResponse({"isEntered": True})

@require_http_methods(["POST"])
@csrf_exempt
def bid(request):
    i_player = int(request.POST["i_player"])
    bidAmount = int(request.POST["bidAmount"])
    g.bid(i_player, bidAmount)
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def discard(request):
    i_player = int(request.POST["i_player"])
    card = {"number": int(request.POST["card[number]"]), "color": request.POST["card[color]"]}
    g.discardCards(i_player, [card])
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def select_trump(request):
    g.setTrump(request.POST["color"])
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def play_card(request):
    i_player = int(request.POST["i_player"])
    card = {
        "number": int(request.POST["card[number]"]),
        "color": request.POST["card[color]"],
        "rank": int(request.POST["card[rank]"]),
        "points": int(request.POST["card[points]"]),
    }
    g.playCard(i_player, card)
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def reset(request):
    global g
    g = Game()
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def state(request):
    i_player = int(request.POST["i_player"])
    return JsonResponse(g.getState(i_player))