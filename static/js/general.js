var emptyFunc = function(data) {};
var alertFunc = function(data) {console.log(data)};

function enterGame() {
    let i_player = $("#playerNum").val() - 1;
    let code = $("#gameKey").val();
    var success = function(data) {
        if (data["isEntered"]) {
            window.location.href = '/game?Code=' + code + '&Player=' + String(i_player + 1);
        } else {
            console.log("Incorrect game code")
        }
    }
    postData("/enter_game/", {i_player: i_player, code: code}, success, emptyFunc, emptyFunc);
}

function createGame() {
    let code = $("#gameKey").val();
    let password = $("#gameMasterPassword").val();
    postData("/create_game/", {code: code, password: password}, alertFunc, emptyFunc, emptyFunc);
}

function deleteGame() {
    let code = $("#gameKey").val();
    let password = $("#gameMasterPassword").val();
    postData("/delete_game/", {code: code, password: password}, alertFunc, emptyFunc, emptyFunc);
}

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