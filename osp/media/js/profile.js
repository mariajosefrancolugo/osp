function refreshVisits(page) {
    $.get(base_url + 'profile/' + student_id + '/all/' + page + '/',
          function(data) {
        $('#visits').fadeOut('fast', function() {
            $(this).html(data);
            $(this).fadeIn('fast');
        });
    });
}

function styleTable(){
    if($('#custom-assessments-body tr:even').hasClass("odd")){
    }else{
        $('#custom-assessments-body tr:even').addClass("odd");
    }
    if($('#custom-assessments-body tr:odd').hasClass("even")){
    }else{
        $('#custom-assessments-body tr:odd').addClass("even");
    }
}

$(function() {

    $('a').click(function(){
        if($(this).attr('href') == '#assessment-results') {
            styleTable();
        }

    });

    $("#profile_menu").tabs({ fx: { opacity: 'toggle', duration: 'fast' } });

    $('#visit-paging a').live('click', function() {
        refreshVisits($(this).data('page'));
    });

    $('#view-note-window').dialog(default_window_options);
    $('#view-visit-window').dialog(default_window_options);

    $('#log-visit-window').dialog(default_window_options);
    $('#log-visit-window').dialog('option', 'buttons', [
        {
            text: 'Submit',
            click: function() {
                var data = $('#visit-form').serializeArray();
                $.post(base_url + 'visit/' + student_id + '/log/',
                       data,
                       function(data) {
                    if(data.status == 'success') {
                        refreshVisits(1);
                        $('#log-visit-window').dialog('close');
                        location.reload();
                    } else if(data.status == 'fail') {
                        $('#log-visit-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
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
                        refreshVisits(1);
                        $('#note-window').dialog('close');
                        window.location.reload();
                    } else if(data.status == 'fail') {
                        $('#note-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
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
                        location.reload();
                    } else if(data.status == 'fail') {
                        $('#intervention-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
            }
        }
    ]);

    $('#log-visit').click(function() {
        $.get(base_url + 'visit/' + student_id + '/log/', function(data) {
            $('#log-visit-window').html(data);
            $('#log-visit-window').dialog('open');
        });
    });

    $('#id-note').click(function() {
        var data = $('#visit_note-form').serializeArray();
        $.get(base_url + 'note/add', data, function(data) {
            $('#note-window').html(data);
            $('#note-window').dialog('open');
        });
    });

    $('#id-intervene').click(function() {
        var data = $('#profile_intervention-form').serializeArray();
        $.get(base_url + 'notification/intervene/', data, function(data) {
            $('#intervention-window').html(data);
            $('#intervention-window').dialog('open');
        });
    });

    $('.view-visit').live('click', function() {
        $.get(base_url + 'visit/' + student_id + '/view/' +
              $(this).data('visit') + '/',
              function(data) {
            $('#view-visit-window').html(data);
            applyNotificationStyles();
            $('#view-visit-window').dialog('open');
        });
    });

    $('.view-note').live('click', function() {
        $.get(base_url + 'note/' + student_id + '/view/' +
              $(this).data('note') + '/',
              function(data) {
            $('#view-note-window').html(data);
            applyNotificationStyles();
            $('#view-note-window').dialog('open');
        });
    });

    $('a.modal').click(function() {
        if($(this).attr('ref') == 'survey-window') {
            $('#survey-window').dialog(default_window_options).load(base_url + 'survey/results/' + $(this).data('result-id') + '/');
            $('#survey-window').dialog('open');
        }
    });

});

function showPersonalityCharts(){$('#personality-type-charts').show();};
function showLearningCharts(){$('#Learning-style-container').show();};
function drawRCharts(){
    var r1 = Raphael("personality-type-chart-1"),
    fin = function () {
        var bar_value = this.bar.value*100;
        bar_value = bar_value.toFixed(0);
        var text_value = bar_value + "%";
        this.flag = r1.label((this.bar.x/10)*8.5, this.bar.y,  text_value || "0").insertBefore(this);
    },
    fout = function () {
        this.flag.animate({opacity: 0}, 300, function () {this.remove();});
    };
    if (personality_type_scores[0][0] == 'E') {
            r1.hbarchart(25, 0, 400, 35, [[personality_type_scores[0][2]], [personality_type_scores[0][1]]], {stacked: true, colors:["#6D95F3","#CCDAFB"]}).attr("stroke", "#333333").hover(fin,fout);
            $('#personality-type-chart-label1 span.right').addClass('highlight');
        } else {
            r1.hbarchart(25, 0, 400, 35, [[personality_type_scores[0][1]], [personality_type_scores[0][2]]], {stacked: true, colors:["#6D95F3","#CCDAFB"]}).attr("stroke", "#333333").hover(fin,fout);
            $('#personality-type-chart-label1 span.left').addClass('highlight');
        }
    var r2 = Raphael("personality-type-chart-2");
    if (personality_type_scores[1][0] == 'S') {
            r2.hbarchart(25, 0, 400, 35, [[personality_type_scores[1][2]], [personality_type_scores[1][1]]], {stacked: true, colors:["#6D95F3","#CCDAFB"]}).attr("stroke", "#333333").hover(fin,fout);
            $('#personality-type-chart-label2 span.right').addClass('highlight');
        } else {
            r2.hbarchart(25, 0, 400, 35, [[personality_type_scores[1][1]], [personality_type_scores[1][2]]], {stacked: true, colors:["#6D95F3","#CCDAFB"]}).attr("stroke", "#333333").hover(fin,fout);
            $('#personality-type-chart-label2 span.left').addClass('highlight');
        }
    var r3 = Raphael("personality-type-chart-3");
    if (personality_type_scores[2][0] == 'T') {
            r3.hbarchart(25, 0, 400, 35, [[personality_type_scores[2][2]], [personality_type_scores[2][1]]], {stacked: true, colors:["#6D95F3","#CCDAFB"]}).attr("stroke", "#333333").hover(fin,fout);
            $('#personality-type-chart-label3 span.right').addClass('highlight');
        } else {
            r3.hbarchart(25, 0, 400, 35, [[personality_type_scores[2][1]], [personality_type_scores[2][2]]], {stacked: true, colors:["#6D95F3","#CCDAFB"]}).attr("stroke", "#333333").hover(fin,fout);
            $('#personality-type-chart-label3 span.left').addClass('highlight');
        }
    var r4 = Raphael("personality-type-chart-4");
    if (personality_type_scores[3][0] == 'J') {
            r4.hbarchart(25, 0, 400, 35, [[personality_type_scores[3][2]], [personality_type_scores[3][1]]], {stacked: true, colors:["#6D95F3","#CCDAFB"]}).attr("stroke", "#333333").hover(fin,fout);
            $('#personality-type-chart-label4 span.right').addClass('highlight');
        } else {
            r4.hbarchart(25, 0, 400, 35, [[personality_type_scores[3][1]], [personality_type_scores[3][2]]], {stacked: true, colors:["#6D95F3","#CCDAFB"]}).attr("stroke", "#333333").hover(fin,fout);
            $('#personality-type-chart-label4 span.left').addClass('highlight');
        }
        showPersonalityCharts();

};

function drawLearningChart(){
    var l1 = Raphael("learning-style-chart"),
    fin = function () {
        var bar_value = this.bar.value*100;
        if (bar_value < 10){
            bar_value = bar_value.toFixed(0);
            var text_value = "Score: "+bar_value;
            this.flag = l1.label(50 , this.bar.y,  text_value || "0").insertBefore(this);
        }
    },
    fout = function () {
        if (this.bar.value*100 < 10){
        this.flag.animate({opacity: 0}, 300, function () {this.remove();});
        }
    };
    Raphael.g.axis(3,175,275,null,null,10,0,["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], "-", 0, l1);
    l1.hbarchart(0, 30, 275, 200, [[latest_learning_style_result.auditory_score]/100,[latest_learning_style_result.kinesthetic_score]/100,[latest_learning_style_result.visual_score]/100,[.1]], {type: "soft", "gutter":"40%", colors:['#6D95F3','#6D95F3','#6D95F3']}).hover(fin,fout);
    showLearningCharts();
};

