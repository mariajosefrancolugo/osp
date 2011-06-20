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

    $('#id_contact').click(function() {
        var form_data = $('form#roster-form').serializeArray();
        if (form_data.length > 2) {
            $('#contact-window').dialog(window_options).load(base_url + 'roster/compose/', form_data, function() {
              $('a#notification-submit').button();
              $('a#notification-submit').click(function() {
                  var form_data_2 = $('form#notification-form').serializeArray();
                  $.post(base_url + 'roster/submit/', form_data_2, function(data) {
                      if (data == "success") {
                          $('#contact-window').dialog("close");
                          $('#contact-window').html('');
                      }
                      else if (data == "fail") {
                          if ($('#contact-window input#id_subject').val() == '') {
                              if (!subject_red) {
                                  $('#contact-window label[for=id_subject').append(red_asterisk);
                                  subject_red = true;
                              }
                          }
                          if ($('#contact-window textarea#id_message').val() == '') {
                              if (!message_red) {
                                  $('#contact-window h3').append(red_asterisk);
                                  message_red = true;
                              }
                          }
                          if (reason_red || campus_red || subject_red || message_red) {
                              if (!errored) {
                                  $('#contact-window a#notification-submit').before(error_message);
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
