$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


(function(){
    console.log('Script is loaded');
    console.log($('#newmessage-form'));
    var data = $('#newmessage-form')[0][4].value;
    var csrf = $('#newmessage-form')[0][6].value;
    var subscribe_channels = data.split(',');
    Pusher.logToConsole = true;

    var pusher = new Pusher('48eec20d8ef030076b17', {
      authEndpoint: '/pusher/auth',
      auth: {
        headers: {
          'X-CSRF-Token': csrf
        }
      },
      encrypted: true
    });

    subscribe_channels.forEach(function(channel){
      pusher.subscribe(channel);
    });
    //pusher.subscribe('private-test_channel');


    var eventName = 'sup-hack';

    var callback = function(data) {
      // add comment into page
      var socket = 0;
      if (pusher && pusher.connection){
        socket = pusher.connection.socket_id;
      }
      var para = "<pre>" + data.message + " by  <em>" + data.user + "</em> on - <mark>" + data.channel + "</mark></pre>"
      $(para).appendTo('#messages');
      $.ajax({
        type: "POST",
        url: "/chat/updatemessage/",
        data:	{'message_text':data.message, 'user':data.user, 'channel': data.channel},
        success: function(data, textStatus, request){
          console.log('update message was successful');
        },
        error: function (request, textStatus, errorThrown) {
          console.log('Oops there was some errror while executing updatemessage!')
        }
      });
    };
    pusher.bind(eventName, callback);
})();


function postchat(){
  var data = $('#newmessage-form');
  $.ajax({
    type: "POST",
    url: "/chat/postmessage/",
    data:	{ 'message_text':data[0][0].value, 'channel_name':data[0][1].value,
            'event_name': data[0][2].value },
    success: function(data, textStatus, request){
      document.getElementById("newmessage-form").reset();
    },
    error: function (request, textStatus, errorThrown) {
      console.log('Oops there was some errror while submitting the form!')
    }
  });
  return false;
}
