

// Save the username

$('#formSubmit').click(function(e){
	localStorage['username'] = $('#username').val();
	//console.log($('#username').val());
	//console.log(localStorage['username']);
})

// Add new channel - prevent space in name

$("#channel_name").keydown(function (e) {
     if (e.keyCode == 32) { 
       $(this).val($(this).val() + "_"); // append '_' to input
       return false; // return false to prevent space from being added
     }
});

// Add new channel name - add channels to local storage

$('#channelSubmit').click(function(){

    let channels = new Array();

    //if user already has channels
    
    if(localStorage['channels']){

        // Collect existing channels from localstorage
        channels.push(localStorage['channels']);
        channels.push($('#channel_name').val());

    }else{
        // just add the new channel into an array
        channels.push($('#channel_name').val());

    }

    // Add array of channels into the user localstorage

    localStorage.setItem("channels", JSON.stringify(channels));

})


// inform server of new upcoming participant in channel

var socket = io();

$(document).ready(function() {
    if ($('.participants-list').length){
        socket.on('connect', function() {
        	socket.emit('enter channel', {data: localStorage['username']});
    	});
    }

});

// $('.channel-card').click(function(){

// 	const username = localStorage['username'];
// 	console.log(localStorage['username']);
//     console.log(username);

//     socket.on('connect', function() {
    	
//         socket.emit('enter channel', {data: localStorage['username']});
//     });
// })

$( document ).ready(function() {
    $('#participants_list:visible').each(function() {

        //console.log("dans id visible");

        const username = localStorage['username'];
        //console.log(localStorage['username']);
        //console.log(username);


        socket.on('connect', function() {
            socket.emit('enter channel', {data: localStorage['username']});
        });
    });
});




socket.on('newParticipant', function(msg){
	//console.log(msg.data);
	//console.log("on socket new participant");
	
    $('.participants-list').append($('<li>').text(msg));

    //let total_chats = new Array();

    if(localStorage['historical_chats']){

        // Collect existing chats from localstorage
        total_chats = localStorage['historical_chats'];

        new_chats = total_chats.replace("</li>,","</li>");

        //console.log(total_chats);


        $('.chat-container').append(new_chats);
  
    }

});



// Send message to the server

$('#sendMessage').click(function(){

    const message = $('#inputMessage').val();
    //console.log(message);

    const username = localStorage['username'];
    var d = new Date();
    const msg_hours = d.getHours();
    const msg_minutes = addZero(d.getMinutes());

    const msg_time = msg_hours + ":" + msg_minutes;

    socket.emit('chatMessage', {data: message, msg_time: msg_time, username: username});
    //console.log("has sent message");
  
})

function addZero(i) {
  if (i < 10) {
    i = "0" + i;
  }
  return i;
}

// Receive chat to spread to all users

socket.on('newUserMessage', function(msg){
	//console.log("on socket newUserMessage");
	//console.log(msg);

    chat_message = "<li><span class='chat-header'>" + msg['username'] + " - " + msg['msg_time'] + "</span> </br> <span class='chat-msg'>" +  msg['message'] + "</span></li>"; 
	
    $('.chat-container').append(chat_message);



    // Add messages into localstorage of chats

    let total_chats = new Array();

    if(localStorage['historical_chats']){

        // Collect existing chats from localstorage
        total_chats.push(localStorage['historical_chats']);
        total_chats.push(chat_message);

    }else{
        // just add the new chat into an array
        total_chats.push(chat_message);

    }

    // Add array of channels into the user localstorage

    localStorage.setItem("historical_chats", total_chats);

});



