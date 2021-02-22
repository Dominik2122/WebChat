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

function update_Msg(messages, current_user_id, end){
  var chat_field = $('.chat_update')
  chat_field.empty()
  if(messages.length>=end){
  for(i = messages.length-end; i < messages.length; i++){
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

function update_list(messages, current_user_id, users_id){
  var other_chats = $('.other_chats')
  other_chats.empty()
  var current_user_name = users_id[current_user_id]
  for(var i = 0; i<messages.length; i++){
    var author_name = users_id[messages[i]['author']]
    if(messages[i]['unread'] != true | messages[i]['prev-author'] == current_user_name){
    other_chats.append("<a class = 'old_message' href='/chat/"+messages[i]['chat']+"/'><h2 class = 'list_user'>"+ author_name + "</h2><p class = 'list_messages'>" +messages[i]['message'] + "</p></a>")
  } else{
    other_chats.append("<a class = 'new_message' href='/chat/"+messages[i]['chat']+"/'><h2 class = 'new_list_user'>"+ author_name + "</h2><p class = 'new_list_messages'>" +messages[i]['message'] + "</p></a>")
  }}
};


function get_Msg(){
    $.ajax({
      url: "",
      method: "GET",
      data: {},
      success: function(json){
        update_Msg(json['messages'], json['current_user_id'],16),
        update_list(json['other_messages'], json['current_user_id'], json['users_id'])
      },
      error: function(errorData){
      }
    })
};


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
  });
