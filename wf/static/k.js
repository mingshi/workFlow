/**
 * @overview
 *
 * @author 
 * @version 2013/12/04
 */

function tipMessage(message, type) {
    $("#popup-msg").html(message);
    $("#popup-msg").attr("class", "alert alert-" + type);
    var w = document.body.clientWidth / 2;
    $("#popup-msg").attr("style", "left:" + w + "px;");
    $("#popup-msg").show();
}

