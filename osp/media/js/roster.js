/*
 * Function to clear the checkboxes in the roster form.
 */
function clearCheckBoxes() {
    var students = document.forms["roster-form"];
    for(n=0; n<students.elements.length; n++) {
        if(students[n].type === 'checkbox') {
            students[n].checked = false;
        }
    }
}

$(function() {
    $("#roster_menu").tabs({ fx: { opacity: 'toggle', duration: 'fast' } });

    $('#contact-window').dialog(default_window_options);
    $('#contact-window').dialog('option', 'buttons', [
        {
            text: 'Submit',
            click: function() {
                var data = $('#contact-form').serializeArray();
                $.post(base_url + 'notification/contact/',
                       data,
                       function(data) {
                    if(data.status == 'success') {
                        $('#contact-window').dialog('close');
                    } else if(data.status == 'fail') {
                        $('#contact-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
                clearCheckBoxes();
            }
        }
    ]);

    $('#intervention-window').dialog(default_window_options);
    $('#intervention-window').dialog('option', 'buttons', [
        {
            text: 'Submit',
            click: function() {
                var data = $('#intervention-form').serializeArray();
                $.post(base_url + 'notification/intervene/',
                       data,
                       function(data) {
                    if(data.status == 'success') {
                        $('#intervention-window').dialog('close');
                        window.location.reload();
                    } else if(data.status == 'fail') {
                        $('#intervention-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
                clearCheckBoxes();
            }
        }
    ]);
    
    $('#note-window').dialog(default_window_options);
    $('#note-window').dialog('option', 'buttons', [
        {
            text: 'Submit',
            click: function() {
                var data = $('#note-form').serializeArray();
                $.post(base_url + 'note/add/',
                       data,
                       function(data) {
                    if(data.status == 'success') {
                        $('#note-window').dialog('close');
                        window.location.reload();
                    } else if(data.status == 'fail') {
                        $('#note-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
                clearCheckBoxes();
            }
        }
    ]);

    $('#id_contact').click(function() {
        if($('input[name=students]:checked').length > 0) {
            var data = $('#roster-form').serializeArray();
            $.get(base_url + 'notification/contact/', data, function(data) {
                $('#contact-window').html(data);
                $('#contact-window').dialog('open');
            });
        }else{
            alert("Please select at least one student.");
        }
    });

    $('#id_intervene').click(function() {
        if($('input[name=students]:checked').length > 0) {
            var data = $('#roster-form').serializeArray();
            $.get(base_url + 'notification/intervene/', data, function(data) {
                $('#intervention-window').html(data);
                $('#intervention-window').dialog('open');
            });
        }else{
            alert("Please select at least one student.");
        }
    });
    
    $('#id_note').click(function() {
        if($('input[name=students]:checked').length > 0) {
            var data = $('#roster-form').serializeArray();
            $.get(base_url + 'note/add', data, 
            
            function(data) {
                $('#note-window').html(data);
                $('#note-window').dialog('open');
            });
        }else{
            alert("Please select at least one student.");
        }
    });
    
});

if (learning_style_counts.auditory > 0 || learning_style_counts.kinesthetic > 0 || learning_style_counts.visual > 0) {
    google.load('visualization', '1', {packages: ['corechart']});
    google.setOnLoadCallback(drawChart);
}

function drawChart() {
    var learning_style_counts_data = new google.visualization.DataTable();

    learning_style_counts_data.addColumn('string', 'Style');
    learning_style_counts_data.addColumn('number', 'Students');
    
    learning_style_counts_data.addRows(3);
    learning_style_counts_data.setValue(0, 0, 'Auditory');
    learning_style_counts_data.setValue(1, 0, 'Kinesthetic');
    learning_style_counts_data.setValue(2, 0, 'Visual');
    
    learning_style_counts_data.setValue(0, 1, learning_style_counts.auditory);
    learning_style_counts_data.setValue(1, 1, learning_style_counts.kinesthetic);
    learning_style_counts_data.setValue(2, 1, learning_style_counts.visual);
    
    var learning_style_counts_chart = new google.visualization.BarChart(document.getElementById('class-chart'));
    learning_style_counts_chart.draw(learning_style_counts_data, {width: 480, height: 200, legend: 'none', backgroundColor: '#f1f1f1'});
}
