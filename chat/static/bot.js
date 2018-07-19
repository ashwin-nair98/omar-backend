var context = {}
$(document).ready(function(){
    $.get("/api/initialize/", function(data){
        context = data.context;
        var initialHtml = '<div class="card text-white bg-danger mb-3" style="max-width: 40%;margin-left:0; margin-right:auto;"><p class="container card-text"><span>' + data.text + '</span></p></div>';
        $("#chatbox").append(initialHtml);
    });
});
function getBotResponse() {
    var rawText = $("#textInput").val();
    var userHtml = '<div class="card text-white bg-primary mb-3" style="max-width: 40%;margin-left:auto; margin-right:0;"><p class="container card-text"><span>' + rawText + '</span></p></div>';
    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
    console.log("Before:", context);
    var postData = {
        msg: rawText,
        context: JSON.stringify(context)
    };
    $.post("/api/get/", postData).done(function(data) {
    if(data.context.exit == true){
        console.log("Exitframe triggered")
        document.getElementById("textInput").disabled = true;
        document.getElementById("buttonInput").disabled = true;
    }
    if(data.text)
    {   var botHtml ='<div class="card text-white bg-danger mb-3" style="max-width: 40%;margin-left:0; margin-right:auto;"><p class="container card-text"><span>' + data.text + '</span></p></div>';
        context = data.context;
    }
    else {
        var botHtml = '<div class="card text-white bg-danger mb-3" style="max-width: 40%; margin-left:0; margin-right:auto;"><p class="container card-ext"><span>' + 'Looks like something went wrong' + '</span></p></div>';
    }              
    $("#chatbox").append(botHtml);
    console.log("After:", context);    
    
    document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
    });
}
$("#textInput").keypress(function(e) {
    if(e.which == 13) {
        getBotResponse();
    }
});
$("#buttonInput").click(function() {
getBotResponse();
})