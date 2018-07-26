var context = {}
var initializeData = {}

var i = 0;
var txt = `Welcome.
I am Omar. I can help you find good restaurants of a cuisine of choice. I can also tell you the ones that are closest to where you are now. And provide with the time and distance.
Please help me improve my cognitive skills by talking to me. The more you talk, the better my service gets.`;
var speed = 50;

function typeWriter() {
    if (i < txt.length) {
        document.getElementById("demo").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}
//find the location of the user
function getLocation(){
    document.getElementById("permission").style.display = "none";
    document.getElementById("loaderContainer").style.display = "block";
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(appendPosition, handleError);
    } else {
        initializeData = {
            navigator : 'NOT_FOUND'
        };
        initialize(initializeData);
    }
}
function handleError(error) {
    var initializeData = {
        latitude: "25.096167299999998",
        longitude: "55.158005900000006"
    };
    initialize(initializeData)
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
    $.get("/api/initialize/", data, function(ret_data){
        context = ret_data.context;
        //console.log(ret_data)
        var initialHtml = '<div class="card bg-light mb-3" id="botText" ><p class="container card-text"><span>' + ret_data.text + '</span></p></div>';
        // Hide loader and show chat
        document.getElementById("loaderContainer").style.display = "none";
        document.getElementById("chat").style.display = "block";
        $("#chatbox").append(initialHtml);
        typeWriter();
    })
}

// Bot response: Triggered each time a user sends a message
function getBotResponse() {
    var rawText = $("#textInput").val();
    if(rawText != "") {
        document.getElementById("demo").style.display = "none";
        document.getElementById("indicator").style.display = "block";
        var userHtml = '<div class="card text-white bg-danger mb-3" id="userText"><p class="container card-text"><span>' + rawText + '</span></p></div>';
        $("#textInput").val("");
        $("#chatbox").append(userHtml);
        document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
        //console.log("Before:", context);
        var postData = {
            msg: rawText,
            context: JSON.stringify(context)
        };
        $.post("/api/get/", postData).done(function(data) {
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
        {   //console.log(data.text)
            if(data.text.length < 2) {
                var botHtml ='<div class="card bg-light mb-3" id="botText"><p class="container card-text"><span>' + data.text + '</span></p></div>';
                document.getElementById("indicator").style.display = "none";
                $("#chatbox").append(botHtml);
            }
            else {
                var botHtml ='<div class="card bg-light mb-3" id="botText"><p class="container card-text"><span>' + data.text[0] + '</span></p></div>';
                $("#chatbox").append(botHtml);
                setTimeout(function(){
                    botHtml ='<div class="card bg-light mb-3" id="botText"><p class="container card-text"><span>' + data.text[1] + '</span></p></div>';
                    document.getElementById("indicator").style.display = "none";
                    $("#chatbox").append(botHtml);
                }, 1000);
            }
        }
        else {
            var botHtml = '<div class="card bg-light mb-3" id="botText"><p class="container card-ext"><span>Looks like something went wrong</span></p></div>';
        }
        context = data.context;
        //console.log("After:", context);

        document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
        
        });
    }
    
}

//Each time the user clicks "Return" or "Send" button, call getBotResponse to send message to the server.
$("#textInput").keypress(function(e) {
    if(e.which == 13) {
        getBotResponse();
    }
});
$("#buttonInput").click(function() {
    getBotResponse();
});
$(document).ready(function(){
    // Add smooth scrolling to all links in navbar + footer link
    $(".navbar a, footer a[href='#myPage']").on('click', function(event) {
      // Make sure this.hash has a value before overriding default behavior
      if (this.hash !== "") {
        // Prevent default anchor click behavior
        event.preventDefault();
  
        // Store hash
        var hash = this.hash;
  
        // Using jQuery's animate() method to add smooth page scroll
        // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
        $('html, body').animate({
          scrollTop: $(hash).offset().top
        }, 900, function(){
     
          // Add hash (#) to URL when done scrolling (default click behavior)
          window.location.hash = hash;
        });
      } // End if
    });
    
    $(window).scroll(function() {
      $(".slideanim").each(function(){
        var pos = $(this).offset().top;
  
        var winTop = $(window).scrollTop();
          if (pos < winTop + 600) {
            $(this).addClass("slide");
          }
      });
    })
});