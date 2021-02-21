$(function() {
// This function gets cookie with a given name
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
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
// test that a given url is a same-origin URL
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

$.ajaxSetup({
beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
}
});
});

function update_Msg(messages, current_user_id){
  var chat_field = $('.chat_update')
  chat_field.empty()
  if(messages.length>=20){
  for(i = messages.length-20; i < messages.length; i++){
    if (messages[i].author_id==current_user_id){
    chat_field.append("<p class='current-user-message'>" + messages[i]['message'] + '</p>')
  } else {
    chat_field.append("<p class='other-user-message'>" + messages[i]['message'] + '</p>')
  }
      }
    }
  else {
    for(i = 0; i < messages.length; i++){
      if (messages[i].author_id==current_user_id){
      chat_field.append("<p class='current-user-message'>" + messages[i]['message'] + '</p>')
    } else {
      chat_field.append("<p class='other-user-message'>" + messages[i]['message'] + '</p>')
    }
        }
      }
    };


function get_Msg(){
    $.ajax({
      url: "",
      method: "GET",
      data: {},
      success: function(json){
        update_Msg(json['messages'], json['current_user_id'])
      } ,
      error: function(errorData){
      }
    })
}


  $(document).ready(function(){
    var messageForm = $('.form-message-ajax')
    messageForm.submit(function(event){
      event.preventDefault()
      var thisForm = messageForm
      var actionEndPoint = thisForm.attr('action')
      var httpMethod = thisForm.attr('method')
      var formData = thisForm.serializeArray()[1]['value']
      var chatId = actionEndPoint.replace(/\D/g, "")
      messageForm.trigger("reset")
      $.ajax({
        url: "create/",
        method: httpMethod,
        data: {
          "chatId" : chatId,
          "form" : formData},
        success: function(json){
        } ,
        error: function(errorData){
        }
      })

    })

  })
