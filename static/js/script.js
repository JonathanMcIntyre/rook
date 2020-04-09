var playerNum;
var runUpdateFunction = function(data) {updateState();};
var func = function(data) {};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function postData(url, data, success, error, complete, async=true) {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({async: async, type: "POST", url: url, data: data, success: success, error: error, complete: complete});
}

function enterGame() {
    let i_player = $("#playerNum").val() - 1;
    var success = function(data) {
        if (data["isEntered"]) {
            window.location.href = '/game?Player=' + String(i_player + 1);
        } else {
            console.log("This player is already entered")
        }
    }
    postData("/enter_game/", {i_player: i_player}, success, func, func);
}

function startGame() {
    playerNum = parseInt(location.href[location.href.length - 1]) - 1;
    $("#playerNumber").text(String(playerNum + 1));
    updateState();
}

function updateState() {
    var success = function(data) {
        console.log(data);
        $("#blackCards").empty();
        $("#greenCards").empty();
        $("#redCards").empty();
        $("#yellowCards").empty();
        $("#rookCards").empty();
        $("#kitty").empty();
        for (const card of data["hand"]) {
            let numStr = String(card.number);
            if (card.number == 0) {
                numStr = "Rook"
            }
            $("#" + card.color + "Cards").append(
                "<button id=" +
                card.color + String(card.number) +
                " class='handCard " + card.color + "'>" +
                numStr +"</button>");

            $("#" + card.color + String(card.number)).on('click', function(e) {
                playCard(card);
            });
        }
        for (const card of data["kitty"]) {
            let numStr = String(card.number);
            if (card.number == 0) {
                numStr = "Rook"
            }
            $("#kitty").append("<button id=" +
                card.color + String(card.number) +
                " class='handCard " + card.color + "'>" +
                numStr +"</button>");
        }
        $("#trumpSelect").val(data.trump);
        for (let i = 0; i < data.playedCards.length; i++) {
            if (data.playedCards[i]) {
                $("#" + "player" + String(i+1) + "Card").text(data.playedCards[i].color + " " + data.playedCards[i].number);
            } else {
                $("#" + "player" + String(i+1) + "Card").text("");
            }
        }
        $("#action").text(data.action);
        $("#highestBidder").text("Player " + String(data.highestBidder+1));
        $("#highestBid").text(String(data.bidAmount));
        $("#points").text(data.points);
        if (data.action === "wait") {
            setTimeout(function () {
                updateState();
            }, 1000);
        }
    }
    postData("/state/", {i_player: playerNum}, success, func, func);
}


function bid() {
    if ($("#action").text() === "bid") {
        let bidAmount = $("#bidAmount").val();
        if (bidAmount <= 300 && bidAmount > parseInt($("#highestBid").text())) {
            postData("/bid/", {i_player: playerNum, bidAmount: bidAmount}, runUpdateFunction, func, func);
        }
    }
}

function passBid() {
    if ($("#action").text() === "bid") {
        let bidAmount = 0;
        postData("/bid/", {i_player: playerNum, bidAmount: bidAmount}, runUpdateFunction, func, func);
    }
}

function chooseTrump() {
    if ($("#action").text() === "choose trump" && $("#trumpSelect").val() !== "Select") {
        postData("/select_trump/", {color: $("#trumpSelect").val()}, runUpdateFunction, func, func);
    }
}

function playCard(card) {
    if ($("#action").text() === "discard") {
        postData("/discard/", {i_player: playerNum, card: card}, runUpdateFunction, func, func);
    } else if ($("#action").text() === "play card") {
        postData("/play_card/", {i_player: playerNum, card: card}, runUpdateFunction, func, func);
    }
}

function resetGame() {
    postData("/reset/", {i_player: playerNum}, runUpdateFunction, func, func);
}