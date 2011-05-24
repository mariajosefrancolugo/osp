var red_asterisk = '<em style="color: red;">*</em>';
var error_message = '<em style="color: red;">One or more required fields are invalid</em>';
var reason_red = false;
var campus_red = false;
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

    $('a#compose').button();
    $('a#compose').click(function() {
        var form_data = $('form#roster-form').serializeArray();
        if (form_data.length > 1) {
            $('#ci-window').dialog(window_options).load(base_url + 'intervention/compose/', form_data, function() {
              $('a#intervention-submit').button();
              $('a#intervention-submit').click(function() {
                  var form_data_2 = $('form#intervention-form').serializeArray();
                  $.post(base_url + 'intervention/submit/', form_data_2, function(data) {
                      if (data == "success") {
                          $('#ci-window').dialog("close");
                          $('#ci-window').html('');
                      }
                      else if (data == "fail") {
                          var reasons_unchecked = true;
                          $('input[id^=id_reasons]').each(function(index) {
                              if ($(this).is(":checked")) {
                                  reasons_unchecked = false;
                              }
                          });
                          if (reasons_unchecked) {
                              if (!reason_red) {
                                  $('legend').append(red_asterisk);
                                  reason_red = true;
                              }
                          }
                          if ($('select#id_campus option:selected').val() == '') {
                              if (!campus_red) {
                                  $('label[for=id_campus]').append(red_asterisk);
                                  campus_red = true;
                              }
                          }
                          if ($('input#id_subject').val() == '') {
                              if (!subject_red) {
                                  $('label[for=id_subject').append(red_asterisk);
                                  subject_red = true;
                              }
                          }
                          if ($('textarea#id_message').val() == '') {
                              if (!message_red) {
                                  $('h3').append(red_asterisk);
                                  message_red = true;
                              }
                          }
                          if (reason_red || campus_red || subject_red || message_red) {
                              if (!errored) {
                                  $('a#intervention-submit').before(error_message);
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
