
$(document).ready(function(){
    var context = {}
    var initializeData = {}

    //find the location of the user
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(appendPosition);
    } else {
        initializeData = {
            navigator : 'NOT_FOUND'
        };
        initialize(initializeData);
    }


    // Appends location and requests for initial call
    function appendPosition(position) {
        console.log('Navigator appended');
        initializeData = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        };
        initialize(initializeData);
    }


    // Initialize: Calls the initialize route to get the first message and context details
    function initialize(data){
        $.get("/api/arabic/initialize/", data, function(ret_data){
            context = ret_data.context;
            console.log(ret_data)
            var initialHtml = '<div class="card text-white bg-danger mb-3" style="max-width: 40%;margin-left:0; margin-right:auto;"><p class="container card-text"><span>' + ret_data.text + '</span></p></div>';
            // Hide loader and show chat
            document.getElementById("loaderContainer").style.display = "none";
            document.getElementById("chat").style.display = "block";
            $("#chatbox").append(initialHtml);
        })
    }

    // Bot response: Triggered each time a user sends a message
    function getBotResponse() {
        document.getElementById("indicator").style.display = "block";
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
        $.post("/api/arabic/get/", postData).done(function(data) {
            if(data.context.exit == true){
                document.getElementById("textInput").disabled = true;
                document.getElementById("buttonInput").disabled = true;
            }
            if(data.context.latlong == 'REQUEST'){
                if(navigator.geolocation){
                    navigator.geolocation.getCurrentPosition(appendPosition)
                }
            }
            if(data.text)
            {   console.log(data.text)
                if(data.text.length < 2) {
                    var botHtml ='<div class="card text-white bg-danger mb-3" style="max-width: 40%;margin-left:0; margin-right:auto;"><p class="container card-text"><span>' + data.text + '</span></p></div>';
                    document.getElementById("indicator").style.display = "none";
                    $("#chatbox").append(botHtml);
                }
                else {
                    var botHtml ='<div class="card text-white bg-danger mb-3" style="max-width: 40%;margin-left:0; margin-right:auto;"><p class="container card-text"><span>' + data.text[0] + '</span></p></div>';
                    $("#chatbox").append(botHtml);
                    setTimeout(function(){
                        botHtml ='<div class="card text-white bg-danger mb-3" style="max-width: 40%;margin-left:0; margin-right:auto;"><p class="container card-text"><span>' + data.text[1] + '</span></p></div>';
                        document.getElementById("indicator").style.display = "none";
                        $("#chatbox").append(botHtml);
                    }, 1000);
                }
            }
            else {
                var botHtml = '<div class="card text-white bg-danger mb-3" style="max-width: 40%; margin-left:0; margin-right:auto;"><p class="container card-ext"><span>Looks like something went wrong</span></p></div>';
            }
            context = data.context;
            console.log("After:", context);

            document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
        });
    }

    //Each time the user clicks "Return" or "Send" button, call getBotResponse to send message to the server.
    $("#textInput").keypress(function(e) {
        if(e.which == 13) {
            getBotResponse();
        }
    });
    $("#buttonInput").click(function() {
    getBotResponse();
    })

});
