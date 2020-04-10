from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.conf import settings
from rook.Game import Game

GAME_MASTER_PASSWORD = "JonIsFabulous"
games = {"rook": Game()}

def index(request):
    template = loader.get_template("index.html")
    data = {}
    return HttpResponse(template.render(data, request))

@require_http_methods(["GET"])
def game(request):
    data = {}
    if request.GET["Code"] in games:
        template = loader.get_template("game.html")
        return HttpResponse(template.render(data, request))
    
    template = loader.get_template("index.html")
    return HttpResponse(template.render(data, request))


@require_http_methods(["POST"])
@csrf_exempt
def create_game(request):
    if request.POST["password"] == GAME_MASTER_PASSWORD:
        global games
        gameCode = request.POST["code"]
        if gameCode not in games:
            games[gameCode] = Game()
            return JsonResponse({"Message": "Game created", "Games": list(games.keys())})
        else:
            return JsonResponse({"Message": "Game already exists", "Games": list(games.keys())})
    
    return JsonResponse({"Success": "Incorrect Password"})

@require_http_methods(["POST"])
@csrf_exempt
def delete_game(request):
    if request.POST["password"] == GAME_MASTER_PASSWORD:
        global games
        gameCode = request.POST["code"]
        if gameCode in games:
            games.pop(gameCode)
            return JsonResponse({"Message": "Game deleted", "Games": list(games.keys())})
        else:
            return JsonResponse({"Message": "Game does not exist", "Games": list(games.keys())})
    
    return JsonResponse({"Success": "Incorrect Password"})

@require_http_methods(["POST"])
@csrf_exempt
def enter_game(request):
    global games
    gameCode = request.POST["code"]
    if gameCode in games:
        return JsonResponse({"isEntered": True, "code": gameCode})
    else:
        return JsonResponse({"isEntered": False, "code": gameCode})

@require_http_methods(["POST"])
@csrf_exempt
def bid(request):
    gameCode = request.POST["code"]
    i_player = int(request.POST["i_player"])
    bidAmount = int(request.POST["bidAmount"])
    games[gameCode].bid(i_player, bidAmount)
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def discard(request):
    gameCode = request.POST["code"]
    i_player = int(request.POST["i_player"])
    card = {"number": int(request.POST["card[number]"]), "color": request.POST["card[color]"]}
    games[gameCode].discardCards(i_player, [card])
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def select_trump(request):
    gameCode = request.POST["code"]
    games[gameCode].setTrump(request.POST["color"])
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def play_card(request):
    gameCode = request.POST["code"]
    i_player = int(request.POST["i_player"])
    card = {
        "number": int(request.POST["card[number]"]),
        "color": request.POST["card[color]"],
        "rank": int(request.POST["card[rank]"]),
        "points": int(request.POST["card[points]"]),
    }
    games[gameCode].playCard(i_player, card)
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def reset(request):
    gameCode = request.POST["code"]
    global games
    games[gameCode] = Game()
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def state(request):
    gameCode = request.POST["code"]
    i_player = int(request.POST["i_player"])
    return JsonResponse(games[gameCode].getState(i_player))