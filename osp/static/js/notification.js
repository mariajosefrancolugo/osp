var red_asterisk = '<em style="color: red;">*</em>';
var error_message = '<em style="color: red;">One or more required fields are invalid</em>';
var subject_red = false;
var message_red = false;
var errored = false;
$(function() {
    var window_options = {
      autoOpen: false,
      height: 600,
      width: 750,
      modal: true,
      resizable: false
    } 

    $('a#compose-notification').button();
    $('a#compose-notification').click(function() {
        var form_data = $('form#roster-form').serializeArray();
        if (form_data.length > 2) {
            $('#cn-window').dialog(window_options).load(base_url + 'roster/compose/', form_data, function() {
              $('a#notification-submit').button();
              $('a#notification-submit').click(function() {
                  var form_data_2 = $('form#notification-form').serializeArray();
                  $.post(base_url + 'roster/submit/', form_data_2, function(data) {
                      if (data == "success") {
                          $('#cn-window').dialog("close");
                          $('#cn-window').html('');
                      }
                      else if (data == "fail") {
                          if ($('#cn-window input#id_subject').val() == '') {
                              if (!subject_red) {
                                  $('#cn-window label[for=id_subject').append(red_asterisk);
                                  subject_red = true;
                              }
                          }
                          if ($('#cn-window textarea#id_message').val() == '') {
                              if (!message_red) {
                                  $('#cn-window h3').append(red_asterisk);
                                  message_red = true;
                              }
                          }
                          if (reason_red || campus_red || subject_red || message_red) {
                              if (!errored) {
                                  $('#cn-window a#notification-submit').before(error_message);
                                  errored = true;
                              }
                          }
                      }

                  });
              });
            }).dialog('open');
        }
    });
});
