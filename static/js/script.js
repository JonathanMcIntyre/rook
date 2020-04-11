var playerNum;
var gameCode;
var runUpdateFunction = function(data) {updateState();};
var func = function(data) {};

function findGetParameter(parameterName) {
    var result = null, tmp = [];
    var items = location.search.substr(1).split("&");
    for (var index = 0; index < items.length; index++) {
        tmp = items[index].split("=");
        if (tmp[0] === parameterName) {
            result = decodeURIComponent(tmp[1]);
        }
    }
    return result;
}

function startGame() {
    gameCode = findGetParameter("Code");
    playerNum = parseInt(findGetParameter("Player")) - 1;
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
            $("#" + "player" + String(i+1) + "Card").removeClass();
            $("#" + "player" + String(i+1) + "Card").addClass("playedCard")
            if (data.playedCards[i]) {
                let numStr = String(data.playedCards[i].number);
                if (data.playedCards[i].number == 0) {
                    numStr = "Rook"
                }
                $("#" + "player" + String(i+1) + "Card").text(numStr);
                $("#" + "player" + String(i+1) + "Card").addClass(data.playedCards[i].color)
            } else {
                $("#" + "player" + String(i+1) + "Card").text("");
            }
        }
        $("#action").text(data.action);
        let highestBidder = "None";
        if (data.highestBidder != null) {
            highestBidder = "Player " + String(data.highestBidder+1);
        }
        $("#highestBidder").text(highestBidder);
        $("#highestBid").text(String(data.bidAmount));
        $("#points").text(data.points);
        $("#pointsOpponent").text(data.pointsOpponent);

        $("#bidAmount").empty();
        if (data.action === "bid") {
            let bidList = [];
            let bidToAdd = data.bidAmount + 5;
            while (bidToAdd <= 300) {
                bidList.push(bidToAdd);
                bidToAdd += 5;
                if (bidToAdd == 180) {
                    bidToAdd = 300;
                }
            }
            for (let i = 0; i < bidList.length; i++) {
                let bidAmountStr = String(bidList[i]);
                let o = new Option(bidAmountStr, bidAmountStr);
                $(o).html(bidAmountStr);
                $("#bidAmount").append(o);
            }
        }

        for (let i = 0; i < 4; i++) {
            if (i == data.playerTurn) {
                $("#playerLabel" + String(i+1)).css('font-weight', 'bold');
            } else {
                $("#playerLabel" + String(i+1)).css('font-weight', 'normal');
            }
        }
        
        if (data.tricks) {
            displayRoundEnd(data.tricks);
        } else {
            if (data.action === "wait") {
                setTimeout(function () {
                    updateState();
                }, 1000);
            }
        }
    }
    postData("/state/", {code: gameCode, i_player: playerNum}, success, func, func);
}


function bid() {
    if ($("#action").text() === "bid") {
        let bidAmount = $("#bidAmount").val();
        postData("/bid/", {code: gameCode, i_player: playerNum, bidAmount: bidAmount}, runUpdateFunction, func, func);
    }
}

function passBid() {
    if ($("#action").text() === "bid") {
        let bidAmount = 0;
        postData("/bid/", {code: gameCode, i_player: playerNum, bidAmount: bidAmount}, runUpdateFunction, func, func);
    }
}

function chooseTrump() {
    if ($("#action").text() === "choose trump" && $("#trumpSelect").val() !== "Select") {
        postData("/select_trump/", {code: gameCode, color: $("#trumpSelect").val()}, runUpdateFunction, func, func);
    }
}

function playCard(card) {
    if ($("#action").text() === "discard") {
        postData("/discard/", {code: gameCode, i_player: playerNum, card: card}, runUpdateFunction, func, func);
    } else if ($("#action").text() === "play card") {
        postData("/play_card/", {code: gameCode, i_player: playerNum, card: card}, runUpdateFunction, func, func);
    }
}

function resetGame() {
    postData("/reset/", {code: gameCode, i_player: playerNum}, runUpdateFunction, func, func);
}

function displayRoundEnd(tricks) {
    $("#results1").empty();
    $("#results2").empty();
    $("#results3").empty();
    $("#results4").empty();
    $("#roundResults").show();
    for (let i = 0; i < tricks.length; i++) {
        for (let j = 0; j < tricks[i].length; j++) {
            let card = tricks[i][j];
            let numStr = String(card.number);
            if (card.number == 0) {
                numStr = "Rook"
            }
            $("#results" + String(j+1)).append("<button id=" +
                card.color + String(card.number) +
                " class='handCard " + card.color + "'>" +
                numStr +"</button><br>");
        }
    }
}